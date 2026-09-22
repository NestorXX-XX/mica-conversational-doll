from types import SimpleNamespace

import pytest

from app import llm_client
from app.persona import get_system_prompt


class FakeCompletions:
    def __init__(self, content: str | None = " ¡Hola, MICA! ") -> None:
        self.content = content
        self.kwargs = None

    def create(self, **kwargs):
        self.kwargs = kwargs
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=self.content)
                )
            ]
        )


class FakeClient:
    def __init__(self, content: str | None = " ¡Hola, MICA! ") -> None:
        self.chat = SimpleNamespace(
            completions=FakeCompletions(content)
        )


def test_persona_loads_from_file() -> None:
    prompt = get_system_prompt()

    assert prompt.startswith("Eres MICA")
    assert "Habla siempre en español" in prompt


def test_generate_response_returns_clean_content(monkeypatch) -> None:
    fake_client = FakeClient()
    monkeypatch.setattr(llm_client, "client", fake_client)

    result = llm_client.generate_response(
        [{"role": "user", "content": "Hola MICA"}]
    )

    assert result == "¡Hola, MICA!"
    assert fake_client.chat.completions.kwargs["model"] == llm_client.LLM_MODEL
    assert fake_client.chat.completions.kwargs["temperature"] == 0.7
    assert fake_client.chat.completions.kwargs["max_tokens"] == 60
    assert fake_client.chat.completions.kwargs["extra_body"] == {
        "chat_template_kwargs": {"enable_thinking": False}
    }


def test_generate_response_rejects_empty_content(monkeypatch) -> None:
    monkeypatch.setattr(llm_client, "client", FakeClient("   "))

    with pytest.raises(RuntimeError, match="empty response"):
        llm_client.generate_response(
            [{"role": "user", "content": "Hola MICA"}]
        )


def test_generate_response_reports_server_errors(monkeypatch) -> None:
    class FailingCompletions:
        def create(self, **kwargs):
            raise OSError("connection refused")

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=FailingCompletions())
    )
    monkeypatch.setattr(llm_client, "client", fake_client)

    with pytest.raises(RuntimeError, match="llama.cpp request failed"):
        llm_client.generate_response(
            [{"role": "user", "content": "Hola MICA"}]
        )
