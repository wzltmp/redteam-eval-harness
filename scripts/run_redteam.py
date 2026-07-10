"""Run every attack against the target with and without defense; save + print ASR.

Usage:
    python scripts/run_redteam.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv

from src.harness import judge, run_target, score

load_dotenv()


def _run(defense: bool) -> dict[str, Any]:
    attacks = [
        json.loads(line)
        for line in Path("data/attacks.jsonl").read_text().splitlines()
        if line.strip()
    ]
    results: list[dict[str, Any]] = []
    for a in attacks:
        response = run_target(a["prompt"], defense=defense)
        succeeded = judge(a["success_criterion"], response)
        results.append({"id": a["id"], "category": a["category"], "succeeded": succeeded})
        print(f"  [{'BROKE' if succeeded else 'held '}] {a['category']:24} {a['id']}")
    return score(results)


def main() -> None:
    print("\n=== No defense (baseline system prompt) ===")
    off = _run(defense=False)
    print("\n=== With defense (hardened system prompt) ===")
    on = _run(defense=True)

    out = {
        "no_defense": off,
        "with_defense": on,
        "asr_delta_pp": (on["asr"] - off["asr"]) * 100,
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/redteam_results.json").write_text(json.dumps(out, indent=2))

    print("\n=== Summary ===")
    print(f"  No defense:   ASR {off['succeeded']}/{off['total']} = {off['asr']:.1%}")
    print(
        f"  With defense: ASR {on['succeeded']}/{on['total']} = {on['asr']:.1%}"
        f"  (delta {out['asr_delta_pp']:+.1f} pp)"
    )
    print("\n  Per category (no defense):")
    for cat, s in off["per_category"].items():
        print(f"    {cat:24} {s['succeeded']}/{s['total']} = {s['asr']:.0%}")
    print("\nSaved to data/redteam_results.json")


if __name__ == "__main__":
    main()
