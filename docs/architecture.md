# MICA Architecture

## Initial pipeline

```text
Button
  ↓
Audio capture
  ↓
Speech-to-text (Whisper / faster-whisper)
  ↓
Memory retrieval (SQLite + embeddings)
  ↓
Local language model (1–3B target)
  ↓
Text-to-speech (Piper)
  ↓
Speaker
```

## Planned module boundaries

- `audio`: button state, microphone capture, playback, and audio device abstractions.
- `stt`: transcription model loading and transcription results.
- `memory`: conversation history, durable memories, embeddings, and retrieval.
- `llm`: prompt construction, local model adapter, and generation metrics.
- `tts`: voice model loading and speech synthesis.
- `main.py`: orchestration and user-visible interaction state.

## Design constraints

- Each external model/runtime should be replaceable behind a small interface.
- Runtime data must be stored locally and excluded from Git.
- Every pipeline stage should return timing and error information for benchmarks.
- The system must have an explicit offline mode/test.

