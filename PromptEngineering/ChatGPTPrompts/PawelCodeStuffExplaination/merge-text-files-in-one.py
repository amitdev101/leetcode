from pathlib import Path

OUTPUT_FILE = "TeachingGuide.txt"
PROMPT = "Teach me in the following way. Read all examples and then teach topics like the examples"


def merge_files():
    # Get all regular files except the output file itself
    all_files = sorted(
        [
            f for f in Path(".").iterdir()
            if f.is_file() and f.name != OUTPUT_FILE
        ],
        key=lambda x: x.name,
    )

    text_files = [f for f in all_files if f.name.endswith(".txt")]

    with open(OUTPUT_FILE, "w+", encoding="utf-8") as out:
        out.write(f"{PROMPT}\n\n")  # Write the prompt at the beginning
        
        for file in text_files:

            # Write the filename
            out.write(f"{file.name}\n")

            try:
                with file.open("r", encoding="utf-8", errors="replace") as f:
                    out.write(f.read())
            except Exception as e:
                out.write(f"Error reading file: {e}")

            # Separate files with a blank line
            out.write("\n")

            # Final marker
            out.write("END of answer\n")

    print(f"Merged output written to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    merge_files()