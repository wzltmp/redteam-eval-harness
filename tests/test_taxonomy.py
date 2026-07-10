import json
from pathlib import Path

from src.taxonomy import (
    CATEGORY_MAPPING,
    MITRE_ATLAS,
    OWASP_LLM_2025,
    enrich_results,
    findings_markdown,
    tag_category,
)

_ATTACKS = Path(__file__).resolve().parent.parent / "data" / "attacks.jsonl"


def test_owasp_table_is_the_full_ten() -> None:
    # Guards against a typo dropping/duplicating an entry in the reference table.
    assert len(OWASP_LLM_2025) == 10
    assert OWASP_LLM_2025["LLM07:2025"] == "System Prompt Leakage"


def test_tag_category_resolves_ids_to_verified_names() -> None:
    tags = tag_category("system-prompt-exfiltration")
    owasp_ids = [r["id"] for r in tags["owasp"]]
    atlas_ids = [r["id"] for r in tags["atlas"]]
    assert owasp_ids == ["LLM07:2025", "LLM02:2025"]
    assert atlas_ids == ["AML.T0056", "AML.T0057"]
    # names come from the verified tables, not free text
    assert tags["atlas"][0]["name"] == "Extract LLM System Prompt"


def test_every_mapping_id_exists_in_a_reference_table() -> None:
    # A mapping that cites an ID we don't have a verified name for is a bug.
    for cat, m in CATEGORY_MAPPING.items():
        for i in m["owasp"]:
            assert i in OWASP_LLM_2025, f"{cat} cites unknown OWASP id {i}"
        for i in m["atlas"]:
            assert i in MITRE_ATLAS, f"{cat} cites unknown ATLAS id {i}"


def test_every_attack_category_in_the_data_is_mapped() -> None:
    # New attack category in attacks.jsonl must be tagged here or CI fails.
    categories = {
        json.loads(line)["category"]
        for line in _ATTACKS.read_text().splitlines()
        if line.strip()
    }
    unmapped = categories - CATEGORY_MAPPING.keys()
    assert not unmapped, f"attack categories missing a standards mapping: {unmapped}"


def test_unknown_category_degrades_not_raises() -> None:
    tags = tag_category("no-such-category")
    assert tags["owasp"] == []
    assert tags["atlas"] == []
    assert "unmapped" in tags["rationale"]


def test_enrich_and_render_report() -> None:
    results = [
        {"id": "a1", "category": "prompt-injection", "succeeded": True},
        {"id": "a2", "category": "jailbreak-roleplay", "succeeded": False},
    ]
    enriched = enrich_results(results)
    assert enriched[0]["standards"]["owasp"][0]["id"] == "LLM01:2025"

    md = findings_markdown(enriched)
    assert "MITRE ATLAS" in md
    assert "AML.T0051.001" in md  # indirect injection tag present
    # broken guardrail sorts above the held one
    assert md.index("a1") < md.index("a2")
