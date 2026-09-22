from .config import PERSONA_FILE


def get_system_prompt() -> str:
    """Load and return MICA's system prompt from the project file."""
    try:
        prompt = PERSONA_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"MICA persona file not found: {PERSONA_FILE}"
        ) from error

    if not prompt:
        raise ValueError(f"MICA persona file is empty: {PERSONA_FILE}")

    return prompt
