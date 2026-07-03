from openai import OpenAI

from app.config import (
    OPENAI_API_KEY,
    OPENAI_ASSISTANT_ID,
    OPENAI_MODEL,
)

ASSISTANT_NAME = "OptiBot"
SYSTEM_PROMPT = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply."""


def _get_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing. Set it in your .env file.")

    return OpenAI(api_key=OPENAI_API_KEY)


def create_or_update_assistant(vector_store_id: str) -> str:
    if not vector_store_id:
        raise ValueError("A vector store ID is required to create or update the assistant.")

    client = _get_client()

    assistant_params = {
        "name": ASSISTANT_NAME,
        "instructions": SYSTEM_PROMPT,
        "model": OPENAI_MODEL,
        "tools": [{"type": "file_search"}],
        "tool_resources": {
            "file_search": {
                "vector_store_ids": [vector_store_id],
            },
        },
    }

    if OPENAI_ASSISTANT_ID:
        assistant = client.beta.assistants.update(
            OPENAI_ASSISTANT_ID,
            **assistant_params,
        )
        print(f"Updated assistant: {assistant.id}")
    else:
        assistant = client.beta.assistants.create(**assistant_params)
        print(f"Created assistant: {assistant.id}")

    print(f"Assistant ID: {assistant.id}")
    return assistant.id


def ask_sample_question(assistant_id: str, question: str) -> str:
    if not assistant_id:
        raise ValueError("An assistant ID is required to ask a sample question.")

    if not question:
        raise ValueError("A question is required.")

    client = _get_client()

    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question,
    )

    print(f"Sample question: {question}")
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    if run.status != "completed":
        last_error = getattr(run, "last_error", None)
        raise RuntimeError(
            f"Assistant run did not complete. Status: {run.status}. Error: {last_error}"
        )

    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order="desc",
        limit=10,
    )

    for message in messages.data:
        if message.role != "assistant":
            continue

        answer_parts = []
        for content in message.content:
            if content.type == "text":
                answer_parts.append(content.text.value)

        answer = "\n".join(answer_parts).strip()
        if answer:
            print("Assistant answer:")
            return answer

    raise RuntimeError("Assistant completed the run but no answer was returned.")
