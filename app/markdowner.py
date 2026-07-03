from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from slugify import slugify

MARKDOWN_DIR = Path("data") / "markdown"


def article_to_markdown(article: dict) -> tuple[str, str]:
    title = article.get("title") or "Untitled Article"
    html_url = article.get("html_url") or ""
    body = article.get("body") or ""

    soup = BeautifulSoup(body, "html.parser")

    for tag in soup.find_all(["script", "style", "nav", "footer"]):
        tag.decompose()

    markdown_body = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
        code_language="",
    ).strip()

    slug = article.get("slug") or slugify(title)
    filename = f"{slug}.md"

    markdown_content = (
        f"# {title}\n\n"
        f"Article URL: {html_url}\n\n"
        "---\n\n"
        f"{markdown_body}\n"
    )

    return filename, markdown_content


def save_markdown_files(articles: list[dict]) -> list[Path]:
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for article in articles:
        filename, markdown_content = article_to_markdown(article)
        path = MARKDOWN_DIR / filename
        path.write_text(markdown_content, encoding="utf-8")
        saved_paths.append(path)

    return saved_paths
