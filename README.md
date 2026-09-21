# MICA — Muñeca Inteligente Conversacional Artificial

MICA is an offline conversational doll designed to listen when activated, understand speech, retrieve personalized memories, respond with a local language model, and speak aloud.

## Project status

Repository scaffolding started September 21, 2026. The first milestone is a text-only local prototype on a MacBook Pro before purchasing hardware.

## Target architecture

```text
Push button → Microphone → Whisper STT → Memory (SQLite + retrieval)
                                      ↓
                                  Local LLM
                                      ↓
                              Piper TTS → Speaker
```

The system is intended to operate without an internet connection. Hardware selection will be based on measured software requirements, not guesses.

## Repository layout

```text
docs/       Requirements, architecture, research, decisions, and plans
src/mica/   Application code organized by pipeline stage
tests/      Automated and integration tests
benchmarks/ Reproducible performance measurements
hardware/   Hardware notes, wiring, and integration plans
data/       Local runtime data; contents are ignored by Git
```

## Development principles

- Prove the software pipeline before buying hardware.
- Keep the core interaction offline-capable.
- Measure latency, memory, model size, and reliability at every stage.
- Keep personal audio and memory data out of version control.
- Prefer small, testable modules over one large application file.

## Getting started

The implementation environment will be documented in `docs/development-setup.md` during Sprint 1. Until then, the intended entry point is:

```bash
python -m mica
```

## Project plan

See [docs/plan.md](docs/plan.md) for the sprint schedule, deliverables, acceptance criteria, and initial issue breakdown.

