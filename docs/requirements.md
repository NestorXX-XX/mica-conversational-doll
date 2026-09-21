# MICA Requirements

This document is the living requirements baseline. Update targets when benchmarks or hardware tests provide better evidence.

## Functional requirements

| ID | Requirement | Verification |
|---|---|---|
| FR-01 | Activate with a physical button | Button integration test |
| FR-02 | Capture microphone input | Audio capture test |
| FR-03 | Convert speech to text locally | STT accuracy and offline test |
| FR-04 | Maintain current conversation context | Short-term memory test |
| FR-05 | Store and retrieve long-term memories | Retrieval test at multiple scales |
| FR-06 | Generate responses with a local LLM | Network-disabled integration test |
| FR-07 | Convert responses to speech locally | TTS playback test |
| FR-08 | Play audio through a speaker | Audio output test |
| FR-09 | Use a defined personality | Personality behavior test |
| FR-10 | Work without internet access | Full offline demonstration |

## Non-functional requirements

| ID | Requirement | Initial target |
|---|---|---|
| NFR-01 | End-to-end response latency | < 5 seconds initially |
| NFR-02 | Event-level observability | Record STT, TTFT, generation, TTS, total |
| NFR-03 | Constrained memory use | Target ≤ 4 GB on eventual constrained platform |
| NFR-04 | Reliability | Measure 20–50 complete conversations |
| NFR-05 | Maintainability | Modular pipeline with automated tests |
| NFR-06 | Privacy | Personal audio and memories remain local and untracked |

