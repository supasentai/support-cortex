import requests

BASE_URL = "https://support.optisigns.com/api/v2/help_center/articles.json"


def fetch_articles(limit: int = 30):
    articles = []
    url = BASE_URL

    while url and len(articles) < limit:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        data = response.json()

        for article in data.get("articles", []):
            articles.append(article)
            if len(articles) >= limit:
                break

        url = data.get("next_page")

    return articles