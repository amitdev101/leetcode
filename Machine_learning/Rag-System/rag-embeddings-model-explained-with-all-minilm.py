"""
Retrieval-only RAG using:

- Ollama
- all-minilm embedding model
- PostgreSQL
- pgvector
- Python

This version intentionally does not use a generation model.

Its purpose is to show the most important part of RAG clearly:

    Document
        ↓
    Split into chunks
        ↓
    Convert chunks into embeddings
        ↓
    Store vectors in PostgreSQL
        ↓
    Convert the user's question into an embedding
        ↓
    Compare the question vector with document vectors
        ↓
    Return the most relevant chunks

Commands:

    python rag-embeddings-model-explained-with-all-minilm.py index

    python rag-embeddings-model-explained-with-all-minilm.py inspect

    python rag-embeddings-model-explained-with-all-minilm.py ask \
        "How much vacation does an employee receive?"

    python rag-embeddings-model-explained-with-all-minilm.py chat
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import psycopg
import requests
from pgvector.psycopg import register_vector


# =============================================================================
# Configuration
# =============================================================================

DATABASE_URL = (
    "postgresql://raguser:ragpassword@localhost:5432/ragdb"
)

OLLAMA_URL = "http://localhost:11434"

# This model creates embeddings only.
#
# It receives text and returns a list of numbers.
# It does not generate natural-language answers.
EMBEDDING_MODEL = "all-minilm"
GENERATION_MODEL = "gemma3:1b"

DOCUMENT_PATH = Path("sample_document.txt")

# We use a separate table so this example does not conflict with an earlier
# table created using embeddinggemma.
#
# Different embedding models can produce vectors with different dimensions.
TABLE_NAME = "document_chunks_all_minilm"

CHUNK_SIZE_WORDS = 100
CHUNK_OVERLAP_WORDS = 20

RETRIEVAL_LIMIT = 3
REQUEST_TIMEOUT_SECONDS = 120


# =============================================================================
# Sample document
# =============================================================================

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


# =============================================================================
# Infrastructure checks
# =============================================================================

def wait_for_ollama(
    attempts: int = 20,
    delay_seconds: float = 2.0,
) -> None:
    """
    Wait until Ollama responds.

    Docker may report that a container is running before the service inside
    that container is ready to receive requests.
    """

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                f"{OLLAMA_URL}/api/tags",
                timeout=5,
            )

            if response.ok:
                print("✅ Ollama is available.")
                return

        except requests.RequestException:
            pass

        print(
            f"Waiting for Ollama "
            f"({attempt}/{attempts})..."
        )

        time.sleep(delay_seconds)

    raise RuntimeError(
        "Ollama is not available at "
        f"{OLLAMA_URL}.\n"
        "Check Docker with:\n"
        "docker compose ps"
    )


def connect_to_database(
    attempts: int = 20,
    delay_seconds: float = 2.0,
) -> psycopg.Connection:
    """
    Connect to PostgreSQL and enable pgvector.

    PostgreSQL normally understands numbers, text, dates, and other standard
    types. The pgvector extension adds a vector type that can store embeddings.
    """

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

            print("✅ PostgreSQL is available.")
            return connection

        except Exception as exc:
            last_error = exc

            print(
                f"Waiting for PostgreSQL "
                f"({attempt}/{attempts})..."
            )

            time.sleep(delay_seconds)

    raise RuntimeError(
        f"Could not connect to PostgreSQL.\n"
        f"Last error: {last_error}"
    )


# =============================================================================
# Document creation and chunking
# =============================================================================

def create_sample_document() -> None:
    """
    Create the sample file only when it does not already exist.

    This means you can later replace its contents with your own document
    without the script overwriting it.
    """

    if DOCUMENT_PATH.exists():
        print(
            f"Using existing document: "
            f"{DOCUMENT_PATH}"
        )
        return

    DOCUMENT_PATH.write_text(
        SAMPLE_DOCUMENT,
        encoding="utf-8",
    )

    print(
        f"Created sample document: "
        f"{DOCUMENT_PATH}"
    )


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE_WORDS,
    overlap: int = CHUNK_OVERLAP_WORDS,
) -> list[str]:
    """
    Split a large document into smaller overlapping passages.

    Why not embed the whole document?

    Imagine a 100-page handbook. One question may only relate to two
    sentences. If the whole document becomes one vector, unrelated topics
    become mixed together.

    Smaller chunks give the search system more precise pieces to compare.

    Why overlap chunks?

    An important sentence may begin at the end of one chunk and continue
    into the next. Overlap preserves some context around boundaries.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero"
        )

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be zero or greater and "
            "smaller than chunk_size"
        )

    words = text.split()

    chunks: list[str] = []

    # If each chunk contains 100 words and overlap is 20,
    # the next chunk starts 80 words later.
    step = chunk_size - overlap

    for start in range(0, len(words), step):
        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        ).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

    return chunks


# =============================================================================
# Embedding generation
# =============================================================================

def create_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Send text to all-minilm through Ollama.

    The model returns one vector for each input string.

    Example conceptually:

        "Employees receive annual leave"

    may become:

        [0.018, -0.042, 0.091, ...]

    The actual vector contains hundreds of numbers.

    We do not assign meaning to individual numbers. The useful property is
    that text with similar meaning tends to produce vectors near each other.
    """

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
            f"Could not create embeddings using "
            f"'{EMBEDDING_MODEL}'.\n\n"
            "Make sure the model is installed:\n"
            "docker compose exec ollama "
            "ollama pull all-minilm\n\n"
            f"Original error: {exc}"
        ) from exc

    response_body = response.json()
    embeddings = response_body.get("embeddings")

    if not embeddings:
        raise RuntimeError(
            "Ollama returned no embeddings.\n"
            f"Response: {response_body}"
        )

    return embeddings


# =============================================================================
# Database schema
# =============================================================================

def recreate_chunks_table(
    connection: psycopg.Connection,
    embedding_dimension: int,
) -> None:
    """
    Recreate the table using the exact vector dimension returned by all-minilm.

    We recreate the table during indexing because a PostgreSQL vector column
    has a fixed dimension.

    For example:

        VECTOR(384)

    can store vectors containing exactly 384 numbers.
    """

    connection.execute(
        f"DROP TABLE IF EXISTS {TABLE_NAME}"
    )

    connection.execute(
        f"""
        CREATE TABLE {TABLE_NAME} (
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
    Create an HNSW vector index.

    With five chunks, PostgreSQL could compare the question against every row.

    That approach becomes expensive with millions of chunks. HNSW builds a
    navigable graph that helps PostgreSQL find nearby vectors without checking
    every vector individually.

    This is approximate search: it trades a small possibility of missing the
    mathematically perfect result for much faster retrieval at scale.
    """

    index_name = (
        f"{TABLE_NAME}_embedding_hnsw_idx"
    )

    connection.execute(
        f"""
        CREATE INDEX {index_name}
        ON {TABLE_NAME}
        USING hnsw (
            embedding vector_cosine_ops
        )
        """
    )


# =============================================================================
# Document indexing
# =============================================================================

def index_document(
    connection: psycopg.Connection,
) -> None:
    """
    Convert the document into searchable database records.

    This is the ingestion side of RAG:

        file
          ↓
        chunks
          ↓
        embeddings
          ↓
        PostgreSQL rows
    """

    create_sample_document()

    document_text = DOCUMENT_PATH.read_text(
        encoding="utf-8"
    )

    print("\n1. Reading the document")
    print(
        f"   Characters: {len(document_text)}"
    )

    chunks = chunk_text(document_text)

    print("\n2. Splitting the document")
    print(
        f"   Created {len(chunks)} chunks"
    )

    for chunk_number, chunk in enumerate(chunks):
        preview = chunk[:90]

        print(
            f"   Chunk {chunk_number}: "
            f"{preview}..."
        )

    print("\n3. Creating embeddings")
    print(
        f"   Model: {EMBEDDING_MODEL}"
    )

    embeddings = create_embeddings(chunks)

    embedding_dimension = len(
        embeddings[0]
    )

    print(
        f"   Embedding dimension: "
        f"{embedding_dimension}"
    )

    print("\n4. Creating PostgreSQL table")

    recreate_chunks_table(
        connection,
        embedding_dimension,
    )

    document_id = DOCUMENT_PATH.stem

    print("\n5. Storing chunks and vectors")

    for chunk_number, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        # pgvector's Psycopg integration accepts NumPy arrays.
        vector = np.array(
            embedding,
            dtype=np.float32,
        )

        connection.execute(
            f"""
            INSERT INTO {TABLE_NAME} (
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

        print(
            f"   Stored chunk {chunk_number}"
        )

    print("\n6. Creating HNSW vector index")

    create_vector_index(connection)

    row_count = connection.execute(
        f"""
        SELECT COUNT(*)
        FROM {TABLE_NAME}
        """
    ).fetchone()[0]

    print("\n✅ Indexing complete")
    print(
        f"   PostgreSQL rows: {row_count}"
    )
    print(
        f"   Vector dimensions: "
        f"{embedding_dimension}"
    )


# =============================================================================
# Retrieval
# =============================================================================

def table_exists(
    connection: psycopg.Connection,
) -> bool:
    """Check whether the indexing table exists."""

    result = connection.execute(
        """
        SELECT TO_REGCLASS(%s)
        """,
        (TABLE_NAME,),
    ).fetchone()

    return result[0] is not None


def retrieve_chunks(
    connection: psycopg.Connection,
    question: str,
    limit: int = RETRIEVAL_LIMIT,
) -> list[dict[str, Any]]:
    """
    Find document chunks closest to the question.

    The question must pass through the same embedding model used for the
    document chunks.

    Document vector:

        all-minilm(document chunk)

    Question vector:

        all-minilm(question)

    PostgreSQL then compares those vectors.

    The pgvector operator:

        <=>

    calculates cosine distance.

    Smaller distance means the vectors are closer.

    Similarity can be represented as:

        similarity = 1 - cosine_distance

    Larger similarity means a stronger match.
    """

    print("\n1. Converting the question into a vector")

    question_embedding = create_embeddings(
        [question]
    )[0]

    query_vector = np.array(
        question_embedding,
        dtype=np.float32,
    )

    print(
        f"   Question vector dimensions: "
        f"{len(question_embedding)}"
    )

    print("\n2. Asking PostgreSQL for nearby vectors")

    rows = connection.execute(
        f"""
        SELECT
            id,
            source,
            chunk_number,
            content,
            embedding <=> %s AS cosine_distance
        FROM {TABLE_NAME}
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (
            query_vector,
            query_vector,
            limit,
        ),
    ).fetchall()

    results: list[dict[str, Any]] = []

    for row in rows:
        cosine_distance = float(row[4])

        results.append(
            {
                "id": row[0],
                "source": row[1],
                "chunk_number": row[2],
                "content": row[3],
                "distance": cosine_distance,
                "similarity": (
                    1.0 - cosine_distance
                ),
            }
        )

    return results


def answer_question(
    connection: psycopg.Connection,
    question: str,
) -> None:
    """
    Retrieve relevant document chunks and ask Gemma to write the final answer.
    """

    if not table_exists(connection):
        raise RuntimeError(
            "The document has not been indexed.\n\n"
            "Run the index operation first."
        )

    print("\n" + "=" * 76)
    print(f"QUESTION: {question}")
    print("=" * 76)

    print("\nRetrieving relevant document passages...")

    results = retrieve_chunks(
        connection,
        question,
    )

    if not results:
        print(
            "\nI could not find relevant information "
            "in the document."
        )
        return

    print(
        f"\nRetrieved {len(results)} passages."
    )

    print(
        f"Generating answer with {GENERATION_MODEL}..."
    )

    answer = generate_answer(
        question,
        results,
    )

    print("\n" + "-" * 76)
    print("ANSWER")
    print("-" * 76)
    print(answer)

    print("\n" + "-" * 76)
    print("RETRIEVED EVIDENCE")
    print("-" * 76)

    for position, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\nResult {position}"
            f"\nChunk: {result['chunk_number']}"
            f"\nSimilarity: {result['similarity']:.4f}"
            f"\nText: {result['content']}"
        )

# =============================================================================
# Database inspection
# =============================================================================

def inspect_database(
    connection: psycopg.Connection,
) -> None:
    """
    Display stored chunks without printing hundreds of vector numbers.
    """

    if not table_exists(connection):
        print(
            "The table does not exist yet.\n\n"
            "Run:\n"
            "python "
            "rag-embeddings-model-explained-with-all-minilm.py "
            "index"
        )
        return

    rows = connection.execute(
        f"""
        SELECT
            id,
            document_id,
            source,
            chunk_number,
            LEFT(content, 100),
            vector_dims(embedding),
            created_at
        FROM {TABLE_NAME}
        ORDER BY chunk_number
        """
    ).fetchall()

    if not rows:
        print(
            "The table exists but contains no chunks."
        )
        return

    print(
        f"\nStored rows in {TABLE_NAME}:"
    )

    for row in rows:
        print("\n" + "-" * 76)

        print(f"Database ID: {row[0]}")
        print(f"Document ID: {row[1]}")
        print(f"Source: {row[2]}")
        print(f"Chunk number: {row[3]}")
        print(f"Vector dimensions: {row[5]}")
        print(f"Created at: {row[6]}")
        print(f"Preview: {row[4]}...")


# =============================================================================
# Interactive chat
# =============================================================================

def interactive_search(
    connection: psycopg.Connection,
) -> None:
    """
    Repeatedly accept questions and show matching document chunks.
    """

    if not table_exists(connection):
        raise RuntimeError(
            "The document has not been indexed.\n\n"
            "Run the index command first."
        )

    print(
        "\nRetrieval-only RAG is ready."
    )

    print(
        "Ask questions about the employee handbook."
    )

    print(
        "Type 'exit' to stop.\n"
    )

    while True:
        try:
            question = input("Question: ").strip()

        except (EOFError, KeyboardInterrupt):
            print("\nStopped.")
            break

        if question.lower() in {
            "exit",
            "quit",
        }:
            print("Stopped.")
            break

        if not question:
            continue

        answer_question(
            connection,
            question,
        )

        print()


def generate_answer(
    question: str,
    retrieved_chunks: list[dict[str, Any]],
) -> str:
    """
    Send the retrieved text and the user's question to Gemma.

    The vectors are not sent to Gemma.

    Gemma receives only:
    - the original text from the matching chunks
    - the user's question
    - instructions describing how it should answer
    """

    if not retrieved_chunks:
        return "I could not find relevant information in the document."

    context_parts: list[str] = []

    for position, result in enumerate(
        retrieved_chunks,
        start=1,
    ):
        context_parts.append(
            f"Source {position}:\n"
            f"{result['content']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are answering questions about an employee handbook.

Use only the context provided below.

Rules:
1. Do not use outside knowledge.
2. If the answer is not present in the context, say:
   "I could not find that information in the document."
3. Give a concise and direct answer.
4. Do not mention embeddings, vectors, retrieval, or source chunks.

Context:
{context}

Question:
{question}

Answer:
""".strip()

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": GENERATION_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                },
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        response.raise_for_status()

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not generate an answer using "
            f"'{GENERATION_MODEL}'.\n\n"
            "Make sure the model is installed:\n"
            "docker compose exec ollama "
            f"ollama pull {GENERATION_MODEL}\n\n"
            f"Original error: {exc}"
        ) from exc

    response_body = response.json()
    answer = response_body.get("response", "").strip()

    if not answer:
        raise RuntimeError(
            "Gemma returned an empty answer."
        )

    return answer


# =============================================================================
# Command-line interface
# =============================================================================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Retrieval-only RAG using "
            "all-minilm, PostgreSQL, and pgvector"
        )
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=False,
    )

    subparsers.add_parser(
        "index",
        help=(
            "Chunk the document, create embeddings, "
            "and store them in PostgreSQL"
        ),
    )

    ask_parser = subparsers.add_parser(
        "ask",
        help=(
            "Embed a question and retrieve "
            "the most relevant document chunks"
        ),
    )

    ask_parser.add_argument(
        "question",
        help="Question about the sample document",
    )

    subparsers.add_parser(
        "inspect",
        help="Inspect chunks stored in PostgreSQL",
    )

    subparsers.add_parser(
        "chat",
        help="Start an interactive retrieval loop",
    )

    return parser.parse_args()


def show_menu() -> str:
    """
    Display an interactive command-line menu and return the selected operation.
    """

    print("\n" + "=" * 60)
    print("RAG Embeddings Application")
    print("=" * 60)

    print("1. Index the document")
    print("2. Ask a question")
    print("3. Inspect stored chunks")
    print("4. Start interactive search")
    print("5. Exit")

    print("=" * 60)

    while True:
        selection = input("Select an operation [1-5]: ").strip()

        menu_options = {
            "1": "index",
            "2": "ask",
            "3": "inspect",
            "4": "chat",
            "5": "exit",
        }

        command = menu_options.get(selection)

        if command:
            return command

        print("Invalid selection. Enter a number from 1 to 5.")


def run_command(
    connection: psycopg.Connection,
    command: str,
    question: str | None = None,
) -> None:
    """
    Execute one RAG operation.

    Keeping command execution in one function avoids duplicating the same
    if/elif logic between direct CLI commands and the numbered menu.
    """

    if command == "index":
        index_document(connection)

    elif command == "ask":
        if not question:
            question = input(
                "\nEnter your question: "
            ).strip()

        if not question:
            print("A question is required.")
            return

        answer_question(
            connection,
            question,
        )

    elif command == "inspect":
        inspect_database(connection)

    elif command == "chat":
        interactive_search(connection)

    else:
        raise ValueError(
            f"Unsupported command: {command}"
        )


def interactive_menu(
    connection: psycopg.Connection,
) -> None:
    """
    Keep showing the menu until the user selects Exit.
    """

    while True:
        command = show_menu()

        if command == "exit":
            print("\nGoodbye.")
            return

        try:
            run_command(
                connection,
                command,
            )

        except Exception as exc:
            print(
                f"\n❌ Operation failed: {exc}",
                file=sys.stderr,
            )

        input(
            "\nPress Enter to return to the menu..."
        )


def main() -> int:
    arguments = parse_arguments()

    try:
        wait_for_ollama()

        with connect_to_database() as connection:
            # When the user starts the script without a command,
            # open the numbered menu.
            if arguments.command is None:
                interactive_menu(connection)

            else:
                question = getattr(
                    arguments,
                    "question",
                    None,
                )

                run_command(
                    connection,
                    arguments.command,
                    question,
                )

        return 0

    except KeyboardInterrupt:
        print("\nStopped.")
        return 0

    except Exception as exc:
        print(
            f"\n❌ Error: {exc}",
            file=sys.stderr,
        )

        return 1

if __name__ == "__main__":
    raise SystemExit(main())