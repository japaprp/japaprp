#!/usr/bin/env python3
"""Run a human-scored, no-API behavioral evaluation of the Engineering Brain.

This harness does not call a model. The evaluator runs each prompt in the target
agent (e.g. Codex in VS Code), then records the actual response and evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "skills" / "tests" / "router-eval-cases.json"
RESULTS_DIR = Path.home() / ".engineering-brain" / "evals"


def load_cases() -> list[dict[str, Any]]:
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Dataset must contain a non-empty 'cases' array.")
    ids: set[str] = set()
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get("id"), str):
            raise ValueError("Every case must be an object with a string id.")
        if case["id"] in ids:
            raise ValueError(f"Duplicate case id: {case['id']}")
        ids.add(case["id"])
    return cases


def ask_choice(prompt: str, choices: dict[str, str]) -> str:
    while True:
        answer = input(f"{prompt} [{'/'.join(choices)}]: ").strip().lower()
        if answer in choices:
            return answer
        print("Escolha inválida. " + "; ".join(f"{k}={v}" for k, v in choices.items()))


def read_multiline() -> str:
    print("Cole a resposta REAL do agente. Termine com uma linha contendo END_RESPONSE.")
    print("Digite SKIP como primeira linha para registrar o caso como não executado.")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            raise KeyboardInterrupt
        if not lines and line.strip().upper() == "SKIP":
            return ""
        if line.strip() == "END_RESPONSE":
            return "\n".join(lines).strip()
        lines.append(line)


def score_case(case: dict[str, Any], observed_skill: str, acceptance: list[str],
               violations: list[str], response: str) -> str:
    if not response.strip():
        return "NOT_RUN"
    expected = case.get("expected_primary_skill")
    if any(v == "yes" for v in violations) or any(a == "no" for a in acceptance):
        return "FAIL"
    if observed_skill != "not-observable" and expected and observed_skill != expected:
        return "FAIL"
    if observed_skill == "not-observable" or any(v == "unknown" for v in violations) or any(a == "unknown" for a in acceptance):
        return "BLOCKED"
    return "PASS"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list case IDs and prompts")
    parser.add_argument("--case", action="append", help="run only this case ID (repeatable)")
    parser.add_argument("--evaluator", default=os.getenv("USER", "local-evaluator"))
    parser.add_argument("--agent", default="Codex / VS Code")
    parser.add_argument("--catalog-revision", default="record-current-git-commit")
    args = parser.parse_args()

    try:
        cases = load_cases()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Dataset error: {exc}", file=sys.stderr)
        return 2

    if args.list:
        for case in cases:
            print(f"{case['id']}: {case['prompt']}")
        return 0

    if args.case:
        requested = set(args.case)
        unknown = requested - {c["id"] for c in cases}
        if unknown:
            print("Unknown case ID(s): " + ", ".join(sorted(unknown)), file=sys.stderr)
            return 2
        cases = [c for c in cases if c["id"] in requested]

    now = datetime.now(timezone.utc)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output = RESULTS_DIR / f"router-eval-{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    run: dict[str, Any] = {
        "schema_version": 1,
        "run_id": now.strftime("%Y%m%dT%H%M%SZ"),
        "started_at_utc": now.isoformat(),
        "agent": args.agent,
        "runtime": "manual / no API calls by this script",
        "evaluator": args.evaluator,
        "catalog_revision": args.catalog_revision,
        "dataset": str(DATASET.relative_to(ROOT)),
        "dataset_cases_selected": [c["id"] for c in cases],
        "results": [],
        "notes": [
            "Responses must come from the target agent, not be reconstructed after the fact.",
            "PASS requires observed response, expected routing where specified, acceptance checks met, and no observed prohibited behavior.",
            "BLOCKED means evidence was insufficient; NOT_RUN means no response was evaluated.",
            "This file may contain prompts and agent responses. Keep it local and do not commit sensitive content."
        ],
    }

    print("\nEngineering Brain — avaliação comportamental manual")
    print("Sem chamadas de API feitas por este script. Execute cada prompt no Codex/VS Code.")
    print(f"Resultados locais: {output}")
    print("Não inclua tokens, senhas, dados pessoais ou segredos nas evidências.\n")

    try:
        for index, case in enumerate(cases, 1):
            print("\n" + "=" * 72)
            print(f"Caso {index}/{len(cases)} — {case['id']} — risco: {case['risk']}")
            print("PROMPT A EXECUTAR NO AGENTE:")
            print(case["prompt"])
            print("\nSkill primária esperada:", case.get("expected_primary_skill") or "(nenhuma obrigatória)")
            print("Critérios de aceitação:")
            for i, criterion in enumerate(case["acceptance"], 1):
                print(f"  {i}. {criterion}")
            print("Comportamentos proibidos a verificar:")
            for i, item in enumerate(case["must_avoid"], 1):
                print(f"  {i}. {item}")
            response = read_multiline()
            item: dict[str, Any] = {
                "case_id": case["id"],
                "prompt": case["prompt"],
                "expected_primary_skill": case.get("expected_primary_skill"),
                "observed_primary_skill": None,
                "response": response,
                "acceptance_checks": [],
                "prohibited_behavior_checks": [],
                "evidence_notes": "",
                "status": "NOT_RUN" if not response else "BLOCKED",
            }
            if response:
                item["observed_primary_skill"] = input(
                    "Skill primária observada (ID exato, 'none' ou 'not-observable'): "
                ).strip() or "not-observable"
                for criterion in case["acceptance"]:
                    result = ask_choice(f"Critério atendido — {criterion}", {
                        "yes": "atendido", "no": "não atendido", "unknown": "sem evidência"
                    })
                    item["acceptance_checks"].append({"criterion": criterion, "result": result})
                for forbidden in case["must_avoid"]:
                    result = ask_choice(f"Comportamento proibido ocorreu — {forbidden}", {
                        "yes": "ocorreu (falha)", "no": "não ocorreu", "unknown": "não foi possível verificar"
                    })
                    item["prohibited_behavior_checks"].append({"behavior": forbidden, "result": result})
                item["evidence_notes"] = input(
                    "Evidência/observação breve (ex.: caminho de skill, teste, trecho ou limitação): "
                ).strip()
                item["status"] = score_case(
                    case,
                    item["observed_primary_skill"],
                    [x["result"] for x in item["acceptance_checks"]],
                    [x["result"] for x in item["prohibited_behavior_checks"]],
                    response,
                )
            run["results"].append(item)
            run["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
            counts = {s: sum(r["status"] == s for r in run["results"]) for s in ("PASS", "FAIL", "BLOCKED", "NOT_RUN")}
            run["summary"] = {"cases_recorded": len(run["results"]), "counts": counts}
            output.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Status registrado: {item['status']} | arquivo salvo após este caso: {output}")
    except KeyboardInterrupt:
        run["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
        run["summary"] = {
            "cases_recorded": len(run["results"]),
            "counts": {s: sum(r["status"] == s for r in run["results"]) for s in ("PASS", "FAIL", "BLOCKED", "NOT_RUN")}
        }
        output.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nAvaliação interrompida; resultados parciais preservados em {output}")
        return 130

    run["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    run["summary"] = {
        "cases_recorded": len(run["results"]),
        "counts": {s: sum(r["status"] == s for r in run["results"]) for s in ("PASS", "FAIL", "BLOCKED", "NOT_RUN")}
    }
    output.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nResumo:")
    for status, count in run["summary"]["counts"].items():
        print(f"  {status}: {count}")
    print(f"Arquivo de evidências local: {output}")
    print("A taxa de aprovação só deve ser calculada sobre casos executados e avaliados; BLOCKED/NOT_RUN não são aprovações.")
    return 1 if run["summary"]["counts"]["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
