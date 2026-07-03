from app.scraper import fetch_articles


def main():
    articles = fetch_articles(limit=30)

    print(f"Fetched {len(articles)} articles")

    for article in articles[:5]:
        print("-", article.get("title"))
        print(" ", article.get("html_url"))


if __name__ == "__main__":
    main()