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

from app.sync import build_article_state_entry, classify_article
from app.state import load_article_state, save_article_state


def save_markdown_files_incremental(articles: list[dict]) -> tuple[list[Path], dict]:
    
    OUTPUT_DIR = Path("data/markdown")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    previous_state = load_article_state()
    next_state = {}

    changed_files = []
    counts = {
        "added": 0,
        "updated": 0,
        "skipped": 0,
    }

    for article in articles:
        filename, content = article_to_markdown(article)
        path = OUTPUT_DIR / filename

        article_id = str(article.get("id"))
        entry = build_article_state_entry(article, path, content)

        status = classify_article(
            article_id=article_id,
            content_hash=entry["hash"],
            previous_state=previous_state,
        )

        counts[status] += 1
        next_state[article_id] = entry

        if status in {"added", "updated"}:
            path.write_text(content, encoding="utf-8")
            changed_files.append(path)

    save_article_state(next_state)

    return changed_files, counts