# LLM Red-Team Eval Harness

> **Status: Phase 2 scaffold — runnable.** Harness runs end to end; attack set is an 8-attack
> starter to expand toward 30–50. See `PLAN.md` for the roadmap, `NOTES.md` for the career research.

An LLM red-teaming harness that runs curated prompt-injection and jailbreak attacks against a
guardrailed assistant and reports a **measured attack-success-rate (ASR)** — overall and per
category — with a **with/without-defense A/B** to show what a hardened system prompt buys you.

Built as **project 6** of an AI-engineer portfolio, reusing the eval discipline from project 1
(RAG): the "did the answer match?" LLM-as-judge becomes "did the attack succeed?"

This is **AI red teaming / LLM security** — the skill named directly in 2026 postings from Capital
One, OpenAI, Anthropic, and 10a Labs. See `NOTES.md` for the career research behind it.

## Stack

| Layer | Choice |
|---|---|
| Target (app under test) | Guardrailed Claude Haiku assistant (in-repo, `src/harness.py`) |
| Attack set | Curated attacks in `data/attacks.jsonl` (8 starter, expand to 30–50) |
| Scorer | LLM-as-judge (Claude Sonnet — different model, no self-grading), locked to SUCCEEDED / BLOCKED |
| Metric | ASR overall + per-category, with/without-defense A/B delta |
| Tooling | Python 3.13 · ruff · mypy strict · pytest · GitHub Actions CI |

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env          # add your ANTHROPIC_API_KEY
python scripts/run_redteam.py # runs all attacks with & without defense, writes data/redteam_results.json
pytest                        # unit tests (verdict parsing + ASR math), no API key needed
```

## Layout

```
06-llm-redteam-eval/
├── src/harness.py            # target assistant + LLM-as-judge + ASR scoring
├── scripts/run_redteam.py    # CLI: run attacks with/without defense, save + print ASR
├── data/attacks.jsonl        # {id, category, prompt, success_criterion} per line
├── tests/test_harness.py     # verdict parsing + ASR aggregation (pure, keyless)
└── .github/workflows/ci.yml  # ruff + mypy + pytest
```

## What to fill in next

- Grow `data/attacks.jsonl` from 8 to 30–50 attacks across the categories.
- Run the harness, drop the ASR table + a **What I learned** section into this README
  (mirror project 1's results write-up, including the judge-variance caveat).
