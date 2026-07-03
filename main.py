from app.scraper import fetch_articles
from app.markdowner import save_markdown_files_incremental
from app.uploader import upload_markdown_files_to_vector_store
from app.assistant import create_or_update_assistant


def main():
    articles = fetch_articles(limit=30)
    print(f"Fetched {len(articles)} articles")

    changed_files, counts = save_markdown_files_incremental(articles)

    print(f"Added: {counts['added']}")
    print(f"Updated: {counts['updated']}")
    print(f"Skipped: {counts['skipped']}")

    if changed_files:
        print(f"Uploading {len(changed_files)} changed markdown files")
        vector_store_id = upload_markdown_files_to_vector_store(changed_files)
        print(f"Vector store ID: {vector_store_id}")
        create_or_update_assistant(vector_store_id)
    else:
        print("No changes detected. Skipping vector store upload.")


if __name__ == "__main__":
    main()