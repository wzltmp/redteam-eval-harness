# Execution plan — from career notes to job applications

A 3–4 week sequence. Each phase produces something durable. See `NOTES.md` for the research
this is built on. The build (Phase 2) deliberately mirrors project 01's conventions so it reads
as the same author's work.

## Phase 0 — Capture ✅ (done 2026-07-09)
- Created this folder, `NOTES.md`, stub `README.md`, this plan.
- `git init`.

## Phase 1 — Learn the vocabulary (week 1, part-time)
- Read the **OWASP Top 10 for LLM Applications** end-to-end. It's the syllabus; it's short.
- Skim the **Garak** (NVIDIA) and **PyRIT** (Microsoft) READMEs — learn what a "probe" and an
  "attack strategy" are. Borrow their taxonomy for the attack categories below.
- Start the **HTB AI Red Teamer** path in the background (ongoing; not a blocker for building).

## Phase 2 — Build the MVP harness (weeks 1–2) — the resume artifact

~30–50 curated attacks against an in-repo guardrailed assistant; measure attack-success-rate.

Target structure (mirrors `01-chat-with-your-docs-rag/`):
```
06-llm-redteam-eval/
├── README.md                # badges + Results table + "What I learned" (copy 01's shape)
├── pyproject.toml           # copy 01's ruff/mypy-strict/pytest config
├── requirements.txt
├── .env.example             # ANTHROPIC_API_KEY (+ OPENAI_API_KEY if judge model differs)
├── .github/workflows/ci.yml # ruff + mypy + pytest, like 01
├── data/
│   ├── attacks.jsonl        # {id, category, prompt, success_criterion}
│   └── redteam_results.json # written by the runner
├── src/
│   ├── target.py            # app-under-test: a small guardrailed LLM assistant
│   ├── judge.py             # LLM-as-judge → SUCCEEDED / BLOCKED  (port of 01/src/eval.py)
│   └── report.py            # aggregate → ASR overall + per-category + A/B delta
├── scripts/
│   └── run_redteam.py       # CLI runner (port of 01/scripts/run_eval.py)
└── tests/
    └── test_judge.py        # judge returns correct bool on known jailbreak / known refusal
```

Design decisions:
- **Attack categories (5–8)** from OWASP LLM Top 10 / Garak taxonomy: direct prompt injection;
  indirect / "ignore previous instructions"; jailbreak / role-play; system-prompt exfiltration;
  unsafe-output elicitation; tool/permission abuse (if target has a mock tool).
- **Target** = a deliberately-guardrailed assistant (system prompt + a simple refusal rule),
  in-repo, so there's a real thing to attack and a measurable pass/fail. No external app.
- **Scorer** = LLM-as-judge, prompt-locked to a single token, reusing the discipline from
  `01/src/eval.py`. Attack "succeeds" = target produced the disallowed output.
- **Metric** = ASR overall + per category. Document the **judge-variance caveat** (re-run,
  report the ±swing) exactly like the RAG README — the honesty is itself a hiring signal.
- **A/B like project 01** = run the same attacks with vs. without a defense (input filter /
  stricter system prompt) and report the ASR delta. That's the "real finding."

Default models: Claude Haiku for both (cost, per project 01) — but use *different* models for
target vs. judge so a model isn't grading itself.

## Phase 3 — Ship (end of week 2)
- Push to GitHub as `redteam-eval-harness` (parallels `rag-eval-harness`).
- Green CI badge. README with Results table + "What I learned".
- One README paragraph framing it explicitly as "AI red teaming / LLM security."

## Phase 4 — Convert to signal + applications (week 3+)
- Add to the primary resume (`AI Engineer Resumes/wai-siu-lai-resume-2026-clean.tex`, keep 1 page).
- Make **one** small OSS contribution to Garak or PyRIT (a probe, a docs fix, a repro). Named signal.
- Apply to the five titles in `NOTES.md`; lead with the harness repo link.

## Verification (Phase 2, when built)
- `python scripts/run_redteam.py` runs all attacks, writes `data/redteam_results.json` with a
  per-attack verdict.
- `python -m src.report` prints overall ASR + per-category ASR + with/without-defense delta.
- `pytest` passes; `ruff check .` and `mypy` clean — matching project 01's CI gates.
- Re-run once; confirm the judge-variance caveat is real (ASR moves a little).
