import hashlib
from pathlib import Path
from typing import Literal


SyncStatus = Literal["added", "updated", "skipped"]


def compute_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def classify_article(
    article_id: str,
    content_hash: str,
    previous_state: dict,
) -> SyncStatus:
    if article_id not in previous_state:
        return "added"

    previous_hash = previous_state[article_id].get("hash")

    if previous_hash != content_hash:
        return "updated"

    return "skipped"


def build_article_state_entry(article: dict, markdown_path: Path, content: str) -> dict:
    return {
        "id": str(article.get("id")),
        "title": article.get("title"),
        "url": article.get("html_url"),
        "slug": article.get("slug"),
        "updated_at": article.get("updated_at"),
        "markdown_path": str(markdown_path),
        "hash": compute_hash(content),
    }