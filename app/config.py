import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MARKDOWN_DIR = Path("data/markdown")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_VECTOR_STORE_ID = os.getenv("OPENAI_VECTOR_STORE_ID")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-4.1-mini"
RUN_SAMPLE_QUESTION = os.getenv("RUN_SAMPLE_QUESTION", "true").lower() not in {
    "false",
    "0",
    "no",
    "off",
}
SAMPLE_QUESTION = os.getenv("SAMPLE_QUESTION") or "How do I use the YouTube Dashboard App in OptiSigns?"
