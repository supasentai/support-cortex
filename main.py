import argparse
import os

from app.scraper import fetch_articles
from app.markdowner import save_markdown_files_incremental
from app.uploader import upload_markdown_files_to_vector_store
from app.assistant import create_or_update_assistant, ask_sample_question
from app.config import OPENAI_VECTOR_STORE_ID


def is_cron_mode() -> bool:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cron", action="store_true")
    args = parser.parse_args()

    env_cron_mode = os.getenv("CRON_MODE", "false").lower() in {
        "true",
        "1",
        "yes",
        "on",
    }

    return args.cron or env_cron_mode


def run_interactive_questions(assistant_id: str) -> None:
    while True:
        print("Enter your question for OptiBot:")
        question = input("> ").strip()

        if not question or question.lower() in {"exit", "quit"}:
            print("Exiting OptiBot question mode.")
            return

        answer = ask_sample_question(assistant_id, question)

        print(f"Question: {question}")
        print(answer)


def main():
    cron_mode = is_cron_mode()
    print("[MODE] Cron" if cron_mode else "[MODE] Interactive")

    articles = fetch_articles(limit=30)
    print(f"Fetched {len(articles)} articles")

    changed_files, counts = save_markdown_files_incremental(articles)

    print(f"Added: {counts['added']}")
    print(f"Updated: {counts['updated']}")
    print(f"Skipped: {counts['skipped']}")

    vector_store_id = None

    if changed_files:
        print(f"Uploading {len(changed_files)} changed markdown files")
        vector_store_id = upload_markdown_files_to_vector_store(changed_files)
        print(f"Vector store ID: {vector_store_id}")
    elif OPENAI_VECTOR_STORE_ID:
        vector_store_id = OPENAI_VECTOR_STORE_ID
        print("No changes detected. Reusing existing vector store.")
        print(f"Vector store ID: {vector_store_id}")
    else:
        print("No changes detected. Skipping vector store upload.")
        print("Set OPENAI_VECTOR_STORE_ID to update the assistant without new files.")

    if vector_store_id:
        assistant_id = create_or_update_assistant(vector_store_id)

        if cron_mode:
            print("Cron mode enabled. Skipping interactive questions.")
        else:
            run_interactive_questions(assistant_id)


if __name__ == "__main__":
    main()
