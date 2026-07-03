from pathlib import Path

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_VECTOR_STORE_ID

VECTOR_STORE_NAME = "support-cortex-knowledge-base"


def list_markdown_files(markdown_dir: Path) -> list[Path]:
    if not markdown_dir.exists():
        raise FileNotFoundError(f"Markdown directory does not exist: {markdown_dir}")

    if not markdown_dir.is_dir():
        raise NotADirectoryError(f"Markdown path is not a directory: {markdown_dir}")

    markdown_files = sorted(markdown_dir.glob("*.md"))
    if not markdown_files:
        raise FileNotFoundError(f"No markdown files found in: {markdown_dir}")

    return markdown_files


def upload_markdown_files_to_vector_store(markdown_files: list[Path]) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your .env file.")

    if not markdown_files:
        raise ValueError("No markdown files were provided for upload.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    if OPENAI_VECTOR_STORE_ID:
        vector_store_id = OPENAI_VECTOR_STORE_ID
    else:
        vector_store = client.vector_stores.create(name=VECTOR_STORE_NAME)
        vector_store_id = vector_store.id
        print(f"Created vector store: {vector_store_id}")

    print(f"Found {len(markdown_files)} markdown files")
    print(f"Using vector store: {vector_store_id}")

    file_streams = []
    try:
        file_streams = [path.open("rb") for path in markdown_files]
        batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store_id,
            files=file_streams,
        )
    finally:
        for stream in file_streams:
            stream.close()

    print(f"Upload status: {getattr(batch, 'status', 'unknown')}")

    file_counts = getattr(batch, "file_counts", None)
    if file_counts:
        completed = getattr(file_counts, "completed", None)
        if completed is not None:
            print(f"Uploaded file count: {completed}")
        else:
            print(f"File counts: {file_counts}")

    return vector_store_id
