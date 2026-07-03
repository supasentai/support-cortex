from app.markdowner import save_markdown_files
from app.scraper import fetch_articles


def main():
    articles = fetch_articles(limit=30)
    files = save_markdown_files(articles)

    print(f"Fetched {len(articles)} articles")
    print(f"Saved {len(files)} markdown files")


if __name__ == "__main__":
    main()
