from app.assistant import create_or_update_assistant, ask_sample_question
from app.config import MARKDOWN_DIR, RUN_SAMPLE_QUESTION
from app.markdowner import save_markdown_files
from app.scraper import fetch_articles
from app.uploader import list_markdown_files, upload_markdown_files_to_vector_store


def main():
    articles = fetch_articles(limit=30)
    files = save_markdown_files(articles)

    print(f"Fetched {len(articles)} articles")
    print(f"Saved {len(files)} markdown files")

    markdown_files = list_markdown_files(MARKDOWN_DIR)
    try:
        vector_store_id = upload_markdown_files_to_vector_store(markdown_files)
        print(f"Vector store ID: {vector_store_id}")

        assistant_id = create_or_update_assistant(vector_store_id)

        if RUN_SAMPLE_QUESTION:
            answer = ask_sample_question(
                assistant_id,
                "How do I add a YouTube video?",
            )
        else:
            answer = "Not applied"
    except RuntimeError as error:
        raise SystemExit(str(error))

    print(answer)


if __name__ == "__main__":
    main()
