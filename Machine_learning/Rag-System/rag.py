"""
Minimal enterprise-style RAG using:

- PostgreSQL
- pgvector
- Ollama
- Python

Commands:

    python rag.py index
    python rag.py ask "How many leave days do employees receive?"
    python rag.py chat
    python rag.py inspect
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import psycopg
import requests
from pgvector.psycopg import register_vector


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATABASE_URL = (
    "postgresql://raguser:ragpassword@localhost:5432/ragdb"
)

OLLAMA_URL = "http://localhost:11434"

EMBEDDING_MODEL = "embeddinggemma"
GENERATION_MODEL = "gemma3:1b"

DOCUMENT_PATH = Path("sample_document.txt")

CHUNK_SIZE_WORDS = 100
CHUNK_OVERLAP_WORDS = 20
RETRIEVAL_LIMIT = 4

REQUEST_TIMEOUT_SECONDS = 180


# ---------------------------------------------------------------------------
# Sample company document
# ---------------------------------------------------------------------------

SAMPLE_DOCUMENT = """
Northstar Technologies Employee Handbook

Annual Leave

Every full-time employee receives 24 days of paid annual leave during each
calendar year. Employees who join during the year receive leave on a
prorated basis.

Employees should normally submit annual leave requests at least seven days
before the planned absence. The employee's manager must approve the request.

Unused annual leave may be carried into the next calendar year, but no more
than five unused days can be carried forward. Any remaining unused days
expire on March 31 of the following year.

Sick Leave

Full-time employees receive 12 days of paid sick leave per calendar year.
A medical certificate is required when an employee is absent for more than
two consecutive working days.

Remote Work

Employees may work remotely for up to three days per week. Remote-working
days must be agreed upon with the employee's manager.

Employees working remotely must remain available during the company's core
working hours, which are 10:00 AM to 4:00 PM Indian Standard Time.

Information Security

Company documents must not be uploaded to personal cloud-storage accounts.
Confidential information may only be stored in systems approved by the
information-security team.

Employees must immediately report a lost company laptop to both their
manager and the information-security team.

Expense Reimbursement

Employees must submit expense claims within 30 days of the original
purchase. Each claim must include a receipt.

A manager may approve an expense claim up to 25,000 Indian rupees. Claims
above that amount require approval from both the department head and the
finance department.

Employee Offboarding

When an employee leaves the company, the manager must notify the IT team
at least three business days before the employee's final working day.

The IT team disables the employee's account at the end of the final working
day. The employee must return laptops, access cards, security keys, and any
other company equipment.
""".strip()


# ---------------------------------------------------------------------------
# Infrastructure checks
# ---------------------------------------------------------------------------

def wait_for_ollama(
    attempts: int = 20,
    delay_seconds: float = 2.0,
) -> None:
    """Wait until the local Ollama API responds."""

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                f"{OLLAMA_URL}/api/tags",
                timeout=5,
            )

            if response.ok:
                return

        except requests.RequestException:
            pass

        print(
            f"Waiting for Ollama "
            f"({attempt}/{attempts})..."
        )
        time.sleep(delay_seconds)

    raise RuntimeError(
        "Ollama is unavailable at http://localhost:11434. "
        "Run: docker compose up -d"
    )


def connect_to_database(
    attempts: int = 20,
    delay_seconds: float = 2.0,
) -> psycopg.Connection:
    """Connect to PostgreSQL and register pgvector types."""

    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            connection = psycopg.connect(
                DATABASE_URL,
                autocommit=True,
            )

            connection.execute(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )

            register_vector(connection)
            return connection

        except Exception as exc:
            last_error = exc

            print(
                f"Waiting for PostgreSQL "
                f"({attempt}/{attempts})..."
            )
            time.sleep(delay_seconds)

    raise RuntimeError(
        f"Could not connect to PostgreSQL: {last_error}"
    )


# ---------------------------------------------------------------------------
# Document preparation
# ---------------------------------------------------------------------------

def create_sample_document() -> None:
    """Create the sample document on the first run."""

    if DOCUMENT_PATH.exists():
        return

    DOCUMENT_PATH.write_text(
        SAMPLE_DOCUMENT,
        encoding="utf-8",
    )

    print(f"Created {DOCUMENT_PATH}")


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE_WORDS,
    overlap: int = CHUNK_OVERLAP_WORDS,
) -> list[str]:
    """
    Break a document into overlapping word-based chunks.

    The overlap prevents context from disappearing when an important
    sentence falls on the boundary between two chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    words = text.split()
    chunks: list[str] = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

    return chunks


# ---------------------------------------------------------------------------
# Ollama
# ---------------------------------------------------------------------------

def create_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """Convert one or more texts into embedding vectors."""

    if not texts:
        return []

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/embed",
            json={
                "model": EMBEDDING_MODEL,
                "input": texts,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Embedding request failed: {exc}\n"
            f"Pull the model with:\n"
            f"docker compose exec ollama "
            f"ollama pull {EMBEDDING_MODEL}"
        ) from exc

    response_body = response.json()
    embeddings = response_body.get("embeddings")

    if not embeddings:
        raise RuntimeError(
            f"Ollama returned no embeddings: {response_body}"
        )

    return embeddings


def generate_answer(
    question: str,
    retrieved_chunks: list[dict],
) -> str:
    """Generate an answer using only retrieved document chunks."""

    context_sections: list[str] = []

    for result in retrieved_chunks:
        context_sections.append(
            f"[Source: {result['source']}, "
            f"Chunk: {result['chunk_number']}]\n"
            f"{result['content']}"
        )

    context = "\n\n".join(context_sections)

    prompt = f"""
You are an assistant answering questions about an employee handbook.

Answer using only the retrieved context below.

Rules:
1. Do not use outside knowledge.
2. If the answer is missing, say:
   "I could not find that information in the document."
3. Give a concise answer.
4. Mention the source chunk numbers used.
5. Do not invent policies, numbers, or dates.

RETRIEVED CONTEXT:

{context}

EMPLOYEE QUESTION:

{question}

ANSWER:
""".strip()

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": GENERATION_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                },
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Generation request failed: {exc}\n"
            f"Pull the model with:\n"
            f"docker compose exec ollama "
            f"ollama pull {GENERATION_MODEL}"
        ) from exc

    answer = response.json().get("response", "").strip()

    if not answer:
        raise RuntimeError("Ollama returned an empty answer")

    return answer


# ---------------------------------------------------------------------------
# Database schema and indexing
# ---------------------------------------------------------------------------

def create_chunks_table(
    connection: psycopg.Connection,
    embedding_dimension: int,
) -> None:
    """
    Create the chunks table.

    The vector dimension must match the embedding model's output.
    """

    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id BIGSERIAL PRIMARY KEY,
            document_id TEXT NOT NULL,
            source TEXT NOT NULL,
            chunk_number INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding VECTOR({embedding_dimension}) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

            UNIQUE(document_id, chunk_number)
        )
        """
    )


def create_vector_index(
    connection: psycopg.Connection,
) -> None:
    """
    Create an HNSW index for approximate cosine search.

    For our tiny sample, PostgreSQL could scan every row. We create the
    index now so the project resembles a scalable production design.
    """

    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS
            document_chunks_embedding_hnsw_idx
        ON document_chunks
        USING hnsw (embedding vector_cosine_ops)
        """
    )


def index_document(
    connection: psycopg.Connection,
) -> None:
    """Read, chunk, embed, and store the sample document."""

    create_sample_document()

    document_text = DOCUMENT_PATH.read_text(
        encoding="utf-8"
    )

    chunks = chunk_text(document_text)

    print(f"Created {len(chunks)} chunks")
    print("Creating embeddings...")

    embeddings = create_embeddings(chunks)
    embedding_dimension = len(embeddings[0])

    print(
        f"Embedding dimension: {embedding_dimension}"
    )

    create_chunks_table(
        connection,
        embedding_dimension,
    )

    document_id = DOCUMENT_PATH.stem

    # Re-indexing the same document should replace old chunks rather
    # than silently duplicate them.
    connection.execute(
        """
        DELETE FROM document_chunks
        WHERE document_id = %s
        """,
        (document_id,),
    )

    for chunk_number, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        vector = np.array(
            embedding,
            dtype=np.float32,
        )

        connection.execute(
            """
            INSERT INTO document_chunks (
                document_id,
                source,
                chunk_number,
                content,
                embedding
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                document_id,
                str(DOCUMENT_PATH),
                chunk_number,
                chunk,
                vector,
            ),
        )

    create_vector_index(connection)

    count = connection.execute(
        """
        SELECT COUNT(*)
        FROM document_chunks
        WHERE document_id = %s
        """,
        (document_id,),
    ).fetchone()[0]

    print(
        f"Indexed {count} chunks into PostgreSQL"
    )


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve_chunks(
    connection: psycopg.Connection,
    question: str,
    limit: int = RETRIEVAL_LIMIT,
) -> list[dict]:
    """
    Find chunks with the smallest cosine distance to the question.

    In pgvector:
        <=> means cosine distance

    Smaller distance means greater similarity.
    """

    question_embedding = create_embeddings(
        [question]
    )[0]

    query_vector = np.array(
        question_embedding,
        dtype=np.float32,
    )

    rows = connection.execute(
        """
        SELECT
            id,
            source,
            chunk_number,
            content,
            embedding <=> %s AS cosine_distance
        FROM document_chunks
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (
            query_vector,
            query_vector,
            limit,
        ),
    ).fetchall()

    results: list[dict] = []

    for row in rows:
        cosine_distance = float(row[4])

        results.append(
            {
                "id": row[0],
                "source": row[1],
                "chunk_number": row[2],
                "content": row[3],
                "distance": cosine_distance,
                "similarity": 1.0 - cosine_distance,
            }
        )

    return results


def answer_question(
    connection: psycopg.Connection,
    question: str,
) -> None:
    """Run retrieval followed by answer generation."""

    collection_exists = connection.execute(
        """
        SELECT TO_REGCLASS('document_chunks')
        """
    ).fetchone()[0]

    if collection_exists is None:
        raise RuntimeError(
            "The document has not been indexed.\n"
            "Run: python rag.py index"
        )

    results = retrieve_chunks(
        connection,
        question,
    )

    if not results:
        print("No document chunks were found")
        return

    print("\n🔎 Retrieved evidence")

    for result in results:
        preview = result["content"][:110].replace(
            "\n",
            " ",
        )

        print(
            f"\nChunk {result['chunk_number']} "
            f"| similarity={result['similarity']:.4f}"
        )
        print(f"{preview}...")

    answer = generate_answer(
        question,
        results,
    )

    print("\n🤖 Answer\n")
    print(answer)


# ---------------------------------------------------------------------------
# Inspection
# ---------------------------------------------------------------------------

def inspect_database(
    connection: psycopg.Connection,
) -> None:
    """Display stored chunks without showing full vectors."""

    table_exists = connection.execute(
        """
        SELECT TO_REGCLASS('document_chunks')
        """
    ).fetchone()[0]

    if table_exists is None:
        print(
            "No chunks table exists. "
            "Run: python rag.py index"
        )
        return

    rows = connection.execute(
        """
        SELECT
            id,
            document_id,
            chunk_number,
            LEFT(content, 90),
            vector_dims(embedding)
        FROM document_chunks
        ORDER BY document_id, chunk_number
        """
    ).fetchall()

    if not rows:
        print("The chunks table is empty")
        return

    for row in rows:
        print(
            f"ID={row[0]} | "
            f"document={row[1]} | "
            f"chunk={row[2]} | "
            f"dimensions={row[4]}"
        )
        print(f"  {row[3]}...")


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Local RAG with PostgreSQL, "
            "pgvector, and Ollama"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "index",
        help="Chunk and index the sample document",
    )

    ask_parser = subparsers.add_parser(
        "ask",
        help="Ask one question",
    )

    ask_parser.add_argument(
        "question",
        help="Question about the document",
    )

    subparsers.add_parser(
        "chat",
        help="Start an interactive question loop",
    )

    subparsers.add_parser(
        "inspect",
        help="Inspect stored document chunks",
    )

    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()

    try:
        wait_for_ollama()

        with connect_to_database() as connection:
            if arguments.command == "index":
                index_document(connection)

            elif arguments.command == "ask":
                answer_question(
                    connection,
                    arguments.question,
                )

            elif arguments.command == "inspect":
                inspect_database(connection)

            elif arguments.command == "chat":
                print(
                    "Ask questions about the handbook."
                )
                print("Type 'exit' to stop.\n")

                while True:
                    question = input("Question: ").strip()

                    if question.lower() in {
                        "exit",
                        "quit",
                    }:
                        break

                    if not question:
                        continue

                    answer_question(
                        connection,
                        question,
                    )
                    print()

        return 0

    except KeyboardInterrupt:
        print("\nStopped")
        return 0

    except Exception as exc:
        print(
            f"\nError: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())