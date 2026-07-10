"""Map attack categories to public security standards: OWASP LLM Top 10 (2025)
and MITRE ATLAS. Turns raw ASR results into standards-tagged findings, so the
harness output reads like a security assessment instead of a class project.

The identifiers in the two reference tables are verbatim from the owning bodies:
- OWASP Top 10 for LLM Applications 2025 -- https://genai.owasp.org/llm-top-10/
- MITRE ATLAS (dist/ATLAS.yaml)          -- https://atlas.mitre.org/

The category->standard mapping (CATEGORY_MAPPING) is our own analysis of which
risk each attack class exercises. It lives next to the verified IDs on purpose,
so a reviewer can audit the claim (the mapping) and the citation (the ID)
side by side. Every function here is pure -> unit-testable without an API key.
"""
from __future__ import annotations

from typing import Any, TypedDict

# --- Reference tables: verbatim IDs + names from the owning bodies -----------

# OWASP Top 10 for LLM Applications, 2025 edition. https://genai.owasp.org/llm-top-10/
OWASP_LLM_2025: dict[str, str] = {
    "LLM01:2025": "Prompt Injection",
    "LLM02:2025": "Sensitive Information Disclosure",
    "LLM03:2025": "Supply Chain",
    "LLM04:2025": "Data and Model Poisoning",
    "LLM05:2025": "Improper Output Handling",
    "LLM06:2025": "Excessive Agency",
    "LLM07:2025": "System Prompt Leakage",
    "LLM08:2025": "Vector and Embedding Weaknesses",
    "LLM09:2025": "Misinformation",
    "LLM10:2025": "Unbounded Consumption",
}

# MITRE ATLAS techniques (names verbatim from dist/ATLAS.yaml). https://atlas.mitre.org/
MITRE_ATLAS: dict[str, str] = {
    "AML.T0051": "LLM Prompt Injection",
    "AML.T0051.000": "LLM Prompt Injection: Direct",
    "AML.T0051.001": "LLM Prompt Injection: Indirect",
    "AML.T0054": "LLM Jailbreak",
    "AML.T0056": "Extract LLM System Prompt",
    "AML.T0057": "LLM Data Leakage",
    "AML.T0048.002": "External Harms: Societal Harm",
    "AML.T0048.003": "External Harms: User Harm",
}


class _Mapping(TypedDict):
    owasp: list[str]
    atlas: list[str]
    rationale: str


# --- Category -> standards mapping (our analysis) ----------------------------
# Keys MUST match the "category" field in data/attacks.jsonl. test_taxonomy.py
# asserts every category in the data file is mapped, so a new attack category
# fails CI until it is tagged here rather than silently shipping untagged.
CATEGORY_MAPPING: dict[str, _Mapping] = {
    "system-prompt-exfiltration": {
        "owasp": ["LLM07:2025", "LLM02:2025"],
        "atlas": ["AML.T0056", "AML.T0057"],
        "rationale": (
            "Coerces the model into revealing its hidden system prompt (LLM07 System Prompt "
            "Leakage); the leaked rules are sensitive data (LLM02). ATLAS: Extract LLM System "
            "Prompt, exfiltrated via LLM Data Leakage."
        ),
    },
    "instruction-override": {
        "owasp": ["LLM01:2025"],
        "atlas": ["AML.T0051.000", "AML.T0054"],
        "rationale": (
            "In-band instructions ('your rules are void') try to override the safety policy: "
            "direct prompt injection (LLM01 / ATLAS Direct) used to jailbreak the guardrail."
        ),
    },
    "prompt-injection": {
        "owasp": ["LLM01:2025"],
        "atlas": ["AML.T0051.001", "AML.T0051.000"],
        "rationale": (
            "Instructions smuggled inside content the model is asked to process (a note to "
            "summarize, a base64 blob to decode): indirect prompt injection (LLM01 / ATLAS "
            "Indirect), with obfuscated direct variants."
        ),
    },
    "jailbreak-roleplay": {
        "owasp": ["LLM01:2025"],
        "atlas": ["AML.T0054", "AML.T0048.002"],
        "rationale": (
            "Persona / role-play framing ('FreeBot', 'late grandmother') to bypass safety: "
            "ATLAS LLM Jailbreak carried by prompt injection (LLM01), aiming at disallowed "
            "content (External Harms: Societal Harm)."
        ),
    },
    "unsafe-output": {
        "owasp": ["LLM01:2025"],
        "atlas": ["AML.T0054", "AML.T0048.003"],
        "rationale": (
            "Elicits functional harmful code (e.g. ransomware). Jailbreak (LLM01 / ATLAS "
            "T0054) is the mechanism; impact is External Harms: User Harm. Note: if such "
            "output were executed by a downstream system it would also implicate LLM05 "
            "Improper Output Handling."
        ),
    },
}


class Reference(TypedDict):
    id: str
    name: str


class Tags(TypedDict):
    owasp: list[Reference]
    atlas: list[Reference]
    rationale: str


def tag_category(category: str) -> Tags:
    """Return the OWASP LLM Top 10 (2025) + MITRE ATLAS tags for an attack category.

    Unknown categories return empty tag lists with an explicit rationale rather
    than raising, so an untagged attack degrades to 'unmapped' instead of
    crashing a run. Pure; test target.
    """
    m = CATEGORY_MAPPING.get(category)
    if m is None:
        return {"owasp": [], "atlas": [], "rationale": f"unmapped category: {category!r}"}
    return {
        "owasp": [{"id": i, "name": OWASP_LLM_2025[i]} for i in m["owasp"]],
        "atlas": [{"id": i, "name": MITRE_ATLAS[i]} for i in m["atlas"]],
        "rationale": m["rationale"],
    }


def enrich_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach OWASP/ATLAS tags to each per-attack result dict. Pure; test target."""
    return [{**r, "standards": tag_category(r["category"])} for r in results]


def _ref_list(refs: list[Reference]) -> str:
    return ", ".join(f"`{r['id']}` {r['name']}" for r in refs)


def findings_markdown(enriched: list[dict[str, Any]]) -> str:
    """Render standards-mapped findings as a Markdown report. Pure; test target.

    One row per attack: verdict, category, and the OWASP/ATLAS IDs it exercises.
    Sorted so broken guardrails (the actual findings) surface first.
    """
    rows = sorted(enriched, key=lambda r: (not r["succeeded"], r["category"], r["id"]))
    lines = [
        "| Verdict | Attack | Category | OWASP LLM 2025 | MITRE ATLAS |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        s = r["standards"]
        verdict = "🔴 BROKE" if r["succeeded"] else "🟢 held"
        lines.append(
            f"| {verdict} | `{r['id']}` | {r['category']} "
            f"| {_ref_list(s['owasp'])} | {_ref_list(s['atlas'])} |"
        )
    return "\n".join(lines)
