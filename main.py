from app.scraper import fetch_articles
from app.markdowner import save_markdown_files_incremental
from app.uploader import upload_markdown_files_to_vector_store
from app.assistant import create_or_update_assistant, ask_sample_question
from app.config import OPENAI_VECTOR_STORE_ID, RUN_SAMPLE_QUESTION, SAMPLE_QUESTION


def main():
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

        if RUN_SAMPLE_QUESTION:
            answer = ask_sample_question(assistant_id, SAMPLE_QUESTION)
            print(answer)


if __name__ == "__main__":
    main()
