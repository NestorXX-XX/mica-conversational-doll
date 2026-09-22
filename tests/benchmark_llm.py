#!/usr/bin/env python3

"""
MICA LLM Benchmark

Benchmarks the local llama.cpp server using realistic MICA conversations.

Server:
    http://localhost:8080

Model:
    Qwen3 1.7B Q4_K_M

The benchmark records:
    - prompt tokens
    - completion tokens
    - total tokens
    - prompt processing time
    - generation time
    - prompt tokens/second
    - generation tokens/second
    - total request latency
    - generated response

Usage:
    python tests/benchmark_llm.py
"""

import json
import statistics
import time
import urllib.request
import urllib.error


# ============================================================
# Configuration
# ============================================================

SERVER_URL = "http://localhost:8080/v1/chat/completions"

MODEL = "ggml-org/Qwen3-1.7B-GGUF:Q4_K_M"

SYSTEM_PROMPT = (
    "Eres MICA, una muñeca conversacional amable y natural. "
    "Habla siempre en español. "
    "Responde de forma breve, cálida y sencilla."
)

TEMPERATURE = 0.7
MAX_TOKENS = 60


# ============================================================
# Test cases
# ============================================================

TESTS = [
    {
        "name": "Greeting",
        "prompt": "Hola MICA, ¿cómo estás?",
    },
    {
        "name": "Tiredness",
        "prompt": "Hoy he tenido un día bastante cansado.",
    },
    {
        "name": "SimpleQuestion",
        "prompt": "¿Qué podemos hacer hoy?",
    },
    {
        "name": "InterestingFact",
        "prompt": "Cuéntame algo interesante sobre los gatos.",
    },
    {
        "name": "MemoryCreation",
        "prompt": "Mi nieta se llama Sofía y le encanta pintar.",
    },
    {
        "name": "MemoryRecall",
        "messages": [
            {
                "role": "user",
                "content": "Mi nieta se llama Sofía y le encanta pintar.",
            },
            {
                "role": "assistant",
                "content": "Qué bonito. Sofía debe ser una chica muy creativa.",
            },
            {
                "role": "user",
                "content": "¿Qué le gusta hacer a Sofía?",
            },
        ],
    },
    {
        "name": "PersonalConversation",
        "prompt": "Me gusta sentarme a escuchar música por las tardes.",
    },
    {
        "name": "Story",
        "prompt": "Cuéntame una historia corta y bonita.",
    },
    {
        "name": "Joke",
        "prompt": "Cuéntame un chiste sencillo.",
    },
    {
        "name": "Companion",
        "prompt": "Hola MICA, hoy me siento un poco solo.",
    },
]


# ============================================================
# HTTP request
# ============================================================

def send_request(messages):
    payload = {
        "model": MODEL,
        "messages": messages,

        # Important for Qwen3:
        # prevent reasoning tokens from consuming the response budget.
        "chat_template_kwargs": {
            "enable_thinking": False
        },

        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        SERVER_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST",
    )

    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_data = response.read()

        end_time = time.perf_counter()

    except urllib.error.URLError as error:
        print(f"\nERROR connecting to llama.cpp:")
        print(error)
        return None

    total_latency_ms = (end_time - start_time) * 1000

    result = json.loads(response_data.decode("utf-8"))

    return result, total_latency_ms


# ============================================================
# Run one benchmark
# ============================================================

def run_test(test):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    if "messages" in test:
        messages.extend(test["messages"])
    else:
        messages.append(
            {
                "role": "user",
                "content": test["prompt"],
            }
        )

    result = send_request(messages)

    if result is None:
        return None

    response, total_latency_ms = result

    choice = response["choices"][0]
    message = choice["message"]

    content = message.get("content", "")

    usage = response.get("usage", {})
    timings = response.get("timings", {})

    return {
        "name": test["name"],
        "response": content,

        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),

        "prompt_ms": timings.get("prompt_ms", 0),
        "generation_ms": timings.get("predicted_ms", 0),

        "prompt_tokens_per_second": timings.get(
            "prompt_per_second", 0
        ),

        "generation_tokens_per_second": timings.get(
            "predicted_per_second", 0
        ),

        "total_latency_ms": total_latency_ms,
    }


# ============================================================
# Main benchmark
# ============================================================

def main():

    print("=" * 70)
    print("MICA LLM BENCHMARK")
    print("=" * 70)

    print(f"Server: {SERVER_URL}")
    print(f"Model:  {MODEL}")
    print()

    print("Testing server connection...")

    test_result = send_request(
        [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": "Hola MICA.",
            },
        ]
    )

    if test_result is None:
        print("\nCould not connect to llama.cpp.")
        print("Make sure your server is running on port 8080.")
        return

    print("Server connection: OK")
    print()

    results = []

    for index, test in enumerate(TESTS, start=1):

        print("-" * 70)
        print(f"TEST {index}/{len(TESTS)}: {test['name']}")

        if "prompt" in test:
            print(f"Prompt: {test['prompt']}")
        else:
            print(f"Conversation: {len(test['messages'])} messages")

        result = run_test(test)

        if result is None:
            continue

        results.append(result)

        print(f"Response: {result['response']}")

        print()
        print(
            f"Latency:       {result['total_latency_ms']:.1f} ms"
        )

        print(
            f"Prompt:        {result['prompt_ms']:.1f} ms"
        )

        print(
            f"Generation:    {result['generation_ms']:.1f} ms"
        )

        print(
            f"Prompt tokens: {result['prompt_tokens']}"
        )

        print(
            f"Output tokens: {result['completion_tokens']}"
        )

        print(
            f"Generation:    "
            f"{result['generation_tokens_per_second']:.1f} tok/s"
        )

    # ========================================================
    # Summary
    # ========================================================

    if not results:
        print("\nNo benchmark results.")
        return

    latencies = [
        r["total_latency_ms"]
        for r in results
    ]

    generation_speeds = [
        r["generation_tokens_per_second"]
        for r in results
        if r["generation_tokens_per_second"] > 0
    ]

    generation_times = [
        r["generation_ms"]
        for r in results
        if r["generation_ms"] > 0
    ]

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"Tests completed:        {len(results)}")

    print(
        f"Average latency:        "
        f"{statistics.mean(latencies):.1f} ms"
    )

    print(
        f"Median latency:         "
        f"{statistics.median(latencies):.1f} ms"
    )

    print(
        f"Min latency:            "
        f"{min(latencies):.1f} ms"
    )

    print(
        f"Max latency:            "
        f"{max(latencies):.1f} ms"
    )

    if generation_times:
        print(
            f"Average generation:     "
            f"{statistics.mean(generation_times):.1f} ms"
        )

    if generation_speeds:
        print(
            f"Average generation:     "
            f"{statistics.mean(generation_speeds):.1f} tok/s"
        )

    print()
    print("=" * 70)
    print("DETAILED RESULTS")
    print("=" * 70)

    print(
        f"{'Test':<22}"
        f"{'Latency':>12}"
        f"{'Output':>10}"
        f"{'Tok/s':>10}"
    )

    print("-" * 54)

    for result in results:

        print(
            f"{result['name']:<22}"
            f"{result['total_latency_ms']:>10.1f} ms"
            f"{result['completion_tokens']:>10}"
            f"{result['generation_tokens_per_second']:>10.1f}"
        )

    # ========================================================
    # Save raw results
    # ========================================================

    output_file = "benchmark_results.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            {
                "model": MODEL,
                "server": SERVER_URL,
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
                "thinking_enabled": False,
                "results": results,
            },
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print(f"Raw results saved to: {output_file}")


if __name__ == "__main__":
    main()