import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MARKDOWN_DIR = Path("data/markdown")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID")
