# MICA Project Plan

**Project:** MICA — Muñeca Inteligente Conversacional Artificial  
**Course:** CSE 399R  
**Start date:** September 21, 2026  
**Final presentation:** December 9, 2026  
**Notebook defense:** December 15, 2026

## Objective

Build and document an offline conversational doll that can be activated by a button, listen through a microphone, convert speech to text, use short- and long-term memory, generate a locally-run response with a defined personality, and speak through a speaker.

## Engineering strategy

The project will progress in this order:

```text
Software → benchmarks → requirements → hardware decision → physical integration
```

The MacBook Pro is the development platform for Sprints 1–3. Hardware will not be purchased until Sprint 4 benchmarks establish the compute, memory, audio, power, thermal, and storage requirements.

## Initial requirements

### Functional

- Button-activated interaction
- Microphone input and speech-to-text
- Conversational context
- Local language-model response generation
- Text-to-speech and speaker output
- Persistent memory with relevant-memory retrieval
- Defined MICA personality
- Operation without internet access

### Initial non-functional targets

| Requirement | Initial target |
|---|---|
| Internet | Not required during operation |
| LLM | Local, target 1–3B parameters |
| Persistent memory | SQLite plus retrieval/embeddings |
| Desired response time | Under 5 seconds initially |
| RAM target | 4 GB or less for the eventual constrained system |
| Battery | Evaluate after hardware decision |
| Physical doll | Defer until software MVP |

These are starting engineering targets. They must be validated with measurements.

## Sprint schedule

### Sprint 1 — Define MICA and prove the basic AI pipeline

**Dates:** September 21–29  
**Deliverable:** MICA v0.1, text-only local conversation

Tasks:

- Define functional and non-functional requirements.
- Research UNO Q 4GB, Raspberry Pi 5 8GB, Raspberry Pi CM5, and Jetson Orin Nano Super.
- Document the initial software architecture.
- Set up Python, Git, a local LLM runtime, Whisper/faster-whisper, Piper, and SQLite.
- Run a local text-only prompt/response loop.
- Record an initial model benchmark.

Acceptance criteria:

- `python -m mica` has a documented way to run.
- A local model responds to a basic Spanish prompt without a network request.
- Requirements, architecture, hardware comparison, and first benchmark are documented.

### Sprint 2 — Give MICA a voice

**Dates:** September 30–October 13  
**Deliverable:** MICA v0.2, complete voice loop on the Mac

Tasks:

- Implement speech-to-text with short Spanish and English test phrases.
- Test background noise and different speaking speeds.
- Implement Piper text-to-speech with a standard voice.
- Connect microphone → STT → LLM → TTS → speaker.
- Measure STT, LLM time-to-first-token, generation, TTS, and total latency.

Acceptance criteria:

- MICA can hear a spoken prompt and respond verbally.
- Tests include Spanish, English, noise, and speaking-speed cases.
- A reproducible latency benchmark is saved under `benchmarks/`.

### Sprint 3 — Memory and personality

**Dates:** October 14–27  
**Deliverable:** MICA v0.3, software MVP

Tasks:

- Add short-term conversation history.
- Add SQLite-backed long-term memory.
- Add embeddings and top-k relevant-memory retrieval.
- Compare full-context memory against retrieved-context memory.
- Test memory scales of 10, 100, 1,000, and 10,000 records.
- Define name, language, tone, family relationships, behavioral rules, and conversation style.

Acceptance criteria:

- MICA remembers a fact during a conversation and retrieves it later.
- Retrieval latency and relevance are measured as memory grows.
- Personality configuration is separate from orchestration code.

### Mid-semester check-in — October 29

Prepare a concise demonstration and evidence package containing the objective, requirements, architecture, research, working software MVP, latency numbers, hardware candidates, problems encountered, and next steps.

### Sprint 4 — Hardware simulation and selection

**Dates:** October 28–November 10  
**Deliverable:** Hardware Selection Report

Tasks:

- Create `MICA-SIM` with an ARM64 Linux environment and a 4 GB RAM constraint where practical.
- Benchmark 1–1.5B, approximately 3B, and approximately 7B models.
- Measure model loading, TTFT, tokens/second, total response time, RAM, and model size.
- Compare compute, RAM, accelerator, storage, power, thermal, and audio requirements against candidate boards.
- Select hardware only after reviewing the evidence.

Acceptance criteria:

- The hardware decision includes requirements, measurements, cost, performance, power, physical constraints, and rationale.
- The selected hardware is sufficient for the measured MVP requirements.

### Sprint 5 — Physical MICA prototype

**Dates:** November 11–24  
**Deliverable:** MICA v0.5 physical prototype

Tasks:

- Acquire and assemble the selected compute board, microphone, button, speaker, amplifier if needed, power, and cooling.
- Validate the system externally before modifying the doll permanently.
- Test idle, active, continuous-conversation, and peak temperatures.
- Disconnect the internet and verify the complete interaction still works.
- Integrate the electronics into the doll after external validation.

Acceptance criteria:

- Press button → speak → MICA listens → responds → speaks.
- The offline test passes.
- Thermal behavior and assembly decisions are documented.

### Sprint 6 — Finalize, test, and document

**Dates:** November 25–December 8  
**Deliverable:** Reliable final prototype and complete documentation

Tasks:

- Run 20–50 conversations and record success, failure, latency, crashes, temperature, memory, and power behavior.
- Repeat memory tests at 10, 100, 1,000, and 10,000 memories.
- Optimize STT, retrieval, LLM, TTS, and perceived waiting time.
- Add listening, processing, and speaking feedback where practical.
- Complete README, architecture, requirements, hardware, software, testing, benchmarks, problems, solutions, and future work.

Acceptance criteria:

- The final demo works reliably from button press through spoken response.
- Offline operation is demonstrated.
- Benchmarks and limitations are honest, reproducible, and included in the final documentation.

## Final presentation — December 9

Demo sequence:

1. Introduce MICA and the offline design goal.
2. Press the activation button.
3. Tell MICA a new fact, such as a favorite color.
4. Ask a different question.
5. Retrieve and demonstrate the stored fact.
6. Disconnect or visibly disable internet access.
7. Explain the architecture: microphone → Whisper → memory → local LLM → Piper → speaker.
8. Show latency, RAM, model-size, reliability, and thermal benchmarks.

## Notebook defense — December 15

Tell the engineering story in order:

```text
Problem → requirements → research → architecture → prototype
       → testing → problems → iterations → hardware selection → final MICA
```

The decision log and benchmark history should explain why each major engineering decision was made.

## First issue backlog

1. Define MICA requirements.
2. Research hardware candidates.
3. Design system architecture.
4. Set up the Python development environment.
5. Install and validate a local LLM.
6. Create the first MICA text prototype.
7. Benchmark the first model.

## Definition of done for the repository foundation

- Repository structure exists and is understandable to a new contributor.
- Project goals and schedule are documented.
- Personal runtime data and model files are ignored.
- The package has a runnable placeholder entry point.
- The first implementation tasks are ready to transfer into GitHub Issues/Projects.

