from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LLM_BASE_URL = "http://localhost:8080/v1"
LLM_MODEL = "ggml-org/Qwen3-1.7B-GGUF:Q4_K_M"

TEMPERATURE = 0.7
MAX_TOKENS = 60

MEMORY_FILE = PROJECT_ROOT / "data" / "memory.json"
PERSONA_FILE = PROJECT_ROOT / "prompts" / "mica_system.txt"