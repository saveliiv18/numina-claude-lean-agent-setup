#!/usr/bin/env python3
"""Discuss proof strategies, math problems, or Lean code with Gemini/GPT."""
import argparse
import os
import sys


def discuss(question: str, backend: str = "gemini", model: str | None = None) -> None:
    if not question.strip():
        print("Error: No question provided.", file=sys.stderr)
        sys.exit(1)

    if backend == "gemini":
        model = model or "gemini-3-pro-preview"
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("Error: Please set GEMINI_API_KEY", file=sys.stderr)
            sys.exit(1)
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model,
                contents=question,
                config=types.GenerateContentConfig(temperature=0.7),
            )
            if response.text:
                print(response.text)
            else:
                print("Error: Gemini returned empty response.", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif backend == "gpt":
        model = model or "gpt-5.2-pro"
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("Error: Please set OPENAI_API_KEY", file=sys.stderr)
            sys.exit(1)
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=model,
                input=question,
                reasoning={"effort": "high"},
                text={"verbosity": "high"},
            )
            if response.output:
                print(response.output[-1].content[0].text)
            else:
                print("Error: GPT returned empty response.", file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Error: backend must be 'gemini' or 'gpt', got '{backend}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Discuss with Gemini/GPT")
    parser.add_argument("question", help="Question text (or - for stdin)")
    parser.add_argument("--backend", choices=["gemini", "gpt"], default="gemini", help="LLM backend")
    parser.add_argument("--model", default=None, help="Override model name")
    args = parser.parse_args()

    question = sys.stdin.read() if args.question == "-" else args.question
    discuss(question, args.backend, args.model)
