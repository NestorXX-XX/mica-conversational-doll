# MICA — Sprint 1 Local LLM Validation

## Objective

Validate the first local/offline AI component for MICA (Muñeca Inteligente Conversacional Artificial) before purchasing embedded hardware.

The goal of this test was to determine whether a small quantized LLM can:

- run locally;
- operate with no Internet connection after the model is downloaded;
- converse in Spanish;
- maintain short-term conversational context;
- follow a MICA personality/system instruction;
- provide a reasonable foundation for the future MICA Python application.

## Development Environment

- **Computer:** MacBook Pro
- **CPU:** Apple M2 Pro
- **RAM:** 16 GB
- **Operating environment:** macOS
- **Project environment:** Python virtual environment named `mica`
- **LLM runtime:** `llama.cpp`
- **Model:** Qwen3 1.7B GGUF
- **Quantization:** Q4_K_M
- **Interface tested:** `llama cli`
- **Network mode:** Offline during validation

`llama.cpp` supports Qwen3 models in GGUF format, and its CLI provides an `--offline` option that forces use of the local cache and prevents network access. Qwen's documentation also describes using `llama-cli` and `llama-server` to run Qwen GGUF models locally.

## Installation / Initial Run

The model was initially downloaded and launched with:

```bash
llama cli -hf ggml-org/Qwen3-1.7B-GGUF:Q4_K_M
```

The model downloaded successfully and loaded as:

```text
model      : ggml-org/Qwen3-1.7B-GGUF:Q4_K_M
ftype      : Q4_K - Medium
modalities : text
```

The initial run confirmed that the model could generate Spanish responses locally.

## Offline Validation

After the model was cached locally, it was launched with:

```bash
llama cli --offline -hf ggml-org/Qwen3-1.7B-GGUF:Q4_K_M
```

The model loaded successfully without downloading anything and generated responses.

This is a successful proof of the core offline LLM requirement:

> Once the model is downloaded and cached, MICA's LLM inference can operate without Internet access.

This does **not** yet prove the entire MICA system is offline. Speech-to-text, text-to-speech, memory, and the final embedded hardware still need to be validated.

## Performance Observations

Observed generation speeds on the M2 Pro varied by prompt:

| Test                      | Prompt processing | Generation |
| ------------------------- | ----------------: | ---------: |
| Initial`hola` test      |         139.9 t/s |   92.1 t/s |
| `Buenas que tal`        |         227.1 t/s |   89.7 t/s |
| Raspberry Pi explanation  |         210.8 t/s |   76.5 t/s |
| Apple/memory test         |         147.4 t/s |   74.0 t/s |
| MICA personality test     |         443.2 t/s |   72.6 t/s |
| Conversation test         |         404.7 t/s |   94.3 t/s |
| Longer follow-up          |         376.3 t/s |   80.2 t/s |
| Identity test             |         815.1 t/s |   82.8 t/s |
| Essay request             |         471.9 t/s |   71.3 t/s |
| Granddaughter memory test |         928.0 t/s |   66.3 t/s |

### Important interpretation

These numbers are **development-machine benchmarks**, not predictions for the eventual embedded MICA hardware.

The M2 Pro is substantially more powerful than the small ARM64 embedded computers being considered for the final device. Hardware selection will therefore require a separate benchmark phase.

The results nevertheless establish a useful baseline for comparing future hardware.

## Functional Tests

### 1. Spanish conversation

Prompt:

```text
Hola MICA, hoy he estado un poco cansado. ¿Qué me recomiendas hacer?
```

Result:

- Correctly responded in Spanish.
- Provided understandable suggestions.
- Response was substantially longer than the desired final MICA style.

**Result: PASS, with personality/style tuning required.**

### 2. Natural Spanish

Prompt:

```text
Háblame como una amiga cercana, usando español natural y sencillo.
Cuéntame algo interesante sobre los gatos.
```

Result:

- Responded in Spanish.
- Attempted a friendly conversational style.
- However, it hallucinated a fictional cat named MICA and produced unnatural/repetitive Spanish.

**Result: PARTIAL PASS.**

This indicates that the 1.7B model can converse, but additional prompting, model configuration, or potentially a stronger model may be required for consistently natural Spanish.

### 3. Short-term memory

Conversation:

```text
Mi nieta se llama Sofía y le encanta pintar.
```

followed by:

```text
¿Qué le gusta hacer a Sofía?
```

Result:

- Correctly retained that Sofía likes painting.

**Result: PASS.**

This demonstrates conversational context retention within the active context window.

### 4. MICA personality instruction

System-style instruction:

```text
Eres MICA, una muñeca conversacional para una persona mayor.
Responde siempre en español, con respuestas cortas, cálidas y fáciles
de entender. Nunca menciones que eres un modelo de lenguaje.
```

Result:

- Responded in Spanish.
- Generally followed the MICA identity.
- However, the answer still contained unnecessary elaboration and emojis.

**Result: PARTIAL PASS.**

### 5. Extended conversation / robustness

The model was tested with several consecutive prompts, including:

- greetings;
- personal information;
- family information;
- identity questions;
- personality instructions;
- requests for explanations;
- a long-form essay request.

The model remained operational throughout, but quality degraded in some conversational turns.

Examples included:

- unnecessary repetition;
- invented information;
- awkward Spanish;
- incorrect identity handling;
- overly verbose responses;
- claims about actions it could not actually perform.

**Result: PARTIAL PASS.**

## Important Problems Discovered

### A. Reasoning text is exposed

The model produced output such as:

```text
[Start thinking]

Okay, the user said...
...
[End thinking]
```

This is **not acceptable for the final MICA user experience**.

The final system should expose only the intended answer, not internal reasoning-style text.

This needs to be addressed through the Qwen/llama.cpp chat-template and reasoning configuration before MICA is integrated into the voice pipeline.

### B. Small model quality limitations

Qwen3 1.7B is fast and lightweight, but testing showed limitations:

- hallucination;
- unnatural Spanish;
- repetitive answers;
- weak identity handling;
- overly verbose responses;
- occasional nonsensical statements;
- confusion between user identity and MICA identity.

This does **not** mean the model is unsuitable for MICA. It means that model quality must be evaluated together with:

1. prompt engineering;
2. context management;
3. memory architecture;
4. generation parameters;
5. potentially larger or different models.

### C. Conversational memory is not persistent memory

The Sofía test proves that the model can use information present in the current conversation context.

It does **not** prove that MICA can remember Sofía after restarting the application.

Persistent memory will therefore be implemented separately, likely using a local database and a retrieval layer.

## Current Architecture

The intended architecture is:

```text
                    MICA
                     |
              Python application
                     |
              +------+------+
              |             |
        Conversation     Memory
           manager       database
              |
              v
        llama-server
              |
              v
        Qwen GGUF model
```

Later, voice components will be added:

```text
Microphone
    |
    v
Speech-to-Text
    |
    v
Python MICA
    |
    +----> Memory
    |
    v
llama.cpp / Qwen
    |
    v
Text-to-Speech
    |
    v
Speaker
```

The final target is that all of these components operate locally without requiring Internet connectivity.

## References

- llama.cpp CLI documentation: https://github.com/ggml-org/llama.cpp
- Qwen3 local llama.cpp documentation: https://github.com/QwenLM/Qwen3/blob/main/docs/source/run_locally/llama.cpp.md
- llama.cpp model documentation: https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md
