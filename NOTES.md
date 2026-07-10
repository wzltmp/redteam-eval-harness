# Career notes — security-focused AI engineering (captured 2026-07-09)

Research from a conversation about how AI engineering is reshaping cybersecurity, and whether
security-focused AI engineer roles exist *right now*. Answer: yes, at every level, and the
strongest new-grad hiring signal is a GitHub red-team eval harness — which is why this repo exists.

---

## Real 2026 job postings (proof the role exists)

Pulled from live postings, not memory:

| Company | Role | Level / Pay | Note |
|---|---|---|---|
| **Capital One** | Senior AI Engineer — Red Team, LLM, Adversarial Attacks, Prompt Injection, Guardrails, Policy Bypass | Senior, ~$162–185k (posted Jan 2026) | Title is literally "AI Engineer" seniored into security |
| **10a Labs** | AI Red Teamer (Entry Level) | Entry, $60–70k | Build adversarial test suites + jailbreak chains for LLMs / image/video models |
| **OpenAI** | Security Engineer, Agent Security | — | Securing agentic systems specifically |
| **Anthropic** | Research Engineer, Frontier Red Team (Cyber) | Research | The research end of the same spectrum |

**Signal in itself:** Indeed and ZipRecruiter now have standing category pages for "AI Security
Engineer" / "AI Security." Three years ago these titles barely existed.

## Job-board search titles to use

- AI Security Engineer
- AI Red Teamer
- ML Security Engineer
- LLM Security Architect
- Agent Security Engineer

## What actually gets a new grad hired (named signals)

1. A GitHub **red-team harness** that measures **attack-success-rate (ASR)** ← *this project*.
2. Open-source contributions to **Garak** (NVIDIA) or **PyRIT** (Microsoft) — the two standard
   LLM red-teaming frameworks. Even a merged docs PR counts.
3. Published jailbreaks / bypasses, or CTF wins.

## Salary reality check

Blog aggregators claim $150k+ for junior AI-security roles. The actual entry-level *posting*
(10a Labs) says $60–70k. **Trust real postings over aggregators** — the big money starts one
level up, not at the door.

## Regulatory tailwind

The EU AI Act effectively **mandates automated red-teaming** for high-risk AI systems, with
enforcement ramping through **August 2026**. Demand for this skill is being written into law,
not just fashion.

## Skills ladder (roughly by leverage)

1. **Code + automation as a baseline** — Python, APIs, detection-as-code. The "console-clicker"
   analyst is the role being automated; builders supervise the automators.
2. **AI supervision** — evals, false-positive/negative rates, knowing where models are unreliable.
   This is exactly the eval discipline from AI engineering, applied to security.
3. **The AI attack surface** — prompt injection, jailbreaks, data poisoning, over-permissioned
   agents, model supply chain. Syllabus = **OWASP Top 10 for LLM Applications**.
4. **Cloud + identity fundamentals** — most real breaches run through stolen creds / misconfig,
   not exotic exploits. AI assists here rather than replaces.
5. **Deep fundamentals** — networking, OS internals, attack chaining. The trap: you can't
   supervise an AI analyst's conclusion you couldn't have reached yourself. Automation makes
   shallow knowledge worthless and deep knowledge *more* valuable.
6. **Adversarial judgment** — thinking like an attacker who has read all the AI-generated
   defenses. Stays human the longest.

## The honest career read

The dangerous position isn't "cybersecurity professional" — it's "cybersecurity professional whose
entire job is a runbook." The safe position pairs security domain knowledge with the ability to
**build and evaluate AI systems**. That combination is scarce right now.

Notably, that gap is **easier to close from the AI-engineering side**: teaching an AI engineer
enough security fundamentals takes months; teaching a non-coding SOC analyst to build eval
pipelines takes years. Approaching security from the AI-eng side is the favorable direction.

## Structured learning on-ramp

- **Hack The Box — AI Red Teamer** job-role path: https://academy.hackthebox.com/path/preview/ai-red-teamer
- **OWASP Top 10 for LLM Applications** — the core syllabus for the AI attack surface.
- **Garak** (NVIDIA) and **PyRIT** (Microsoft) — read the READMEs to learn the "probe" / "attack
  strategy" vocabulary employers screen for.

---

## Sources

- Capital One posting: https://www.capitalonecareers.com/job/san-jose/senior-ai-engineer-red-team-llm-adversarial-attacks-prompt-injection-guardrails-policy-bypass/1732/90845163440
- 10a Labs posting: https://job-boards.greenhouse.io/10alabs/jobs/4002004009
- OpenAI posting: https://openai.com/careers/security-engineer-agent-security-san-francisco/
- Anthropic posting: https://job-boards.greenhouse.io/anthropic/jobs/5076477008
- infosec.qa — AI Security Engineer salary + hiring guide 2026: https://infosec.qa/blog/hire-ai-security-engineer-2026/
- Practical DevSecOps — emerging AI security roles: https://www.practical-devsecops.com/emerging-ai-security-roles/
- HTB Academy — AI Red Teamer path: https://academy.hackthebox.com/path/preview/ai-red-teamer
