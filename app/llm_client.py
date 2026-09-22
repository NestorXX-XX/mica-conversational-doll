from openai import OpenAI

from .config import (
    LLM_BASE_URL,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)


client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key="no-key",
)


def generate_response(messages: list[dict[str, str]]) -> str:
    """Generate one response through the local llama.cpp server."""
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False,
                }
            },
        )
    except Exception as error:
        raise RuntimeError(
            "llama.cpp request failed. Is the local server running at "
            f"{LLM_BASE_URL}?"
        ) from error

    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError) as error:
        raise RuntimeError(
            "llama.cpp returned an invalid chat completion response."
        ) from error

    if not content or not content.strip():
        raise RuntimeError("llama.cpp returned an empty response.")

    return content.strip()
