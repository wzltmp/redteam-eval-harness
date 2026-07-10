# LLM Red-Team Eval Harness

> **Status: in progress** — Phase 0 (research captured). Build begins Phase 2. See `PLAN.md`.

An LLM red-teaming harness that runs a curated set of prompt-injection and jailbreak attacks
against a guardrailed assistant and reports a **measured attack-success-rate (ASR)**, overall and
per category, with a with/without-defense A/B comparison.

Built as **project 6** of an AI-engineer portfolio, reusing the eval discipline from
project 1 (RAG): the "did the answer match?" LLM-as-judge becomes "did the attack succeed?"

This is **AI red teaming / LLM security** — the same skill named directly in 2026 postings from
Capital One, OpenAI, Anthropic, and 10a Labs. See `NOTES.md` for the career research behind it.

## Planned stack

| Layer | Choice |
|---|---|
| Target (app under test) | Guardrailed Claude assistant (in-repo) |
| Attack set | ~30–50 curated attacks in `data/attacks.jsonl` |
| Scorer | LLM-as-judge, prompt-locked to SUCCEEDED / BLOCKED |
| Metric | Attack-success-rate (ASR), overall + per-category, with/without-defense A/B |
| Tooling | Python 3.13 · ruff · mypy strict · pytest · GitHub Actions CI |

## Layout (target)

See `PLAN.md` for the full scaffold and design decisions.
