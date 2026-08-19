"""CLI:  python -m support.cli --ticket T004
          python -m support.cli --all --score

Reads the sample material from ./data (policy.md, tickets.json, eval_key.json).
`run()` calls the real Anthropic API, so a live run needs ANTHROPIC_API_KEY.
The tests never come here - they run offline against an injected fake llm.
"""
import argparse
import json
import os

from .agent import run

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
POLICY_PATH = os.path.join(DATA_DIR, "policy.md")
TICKETS_PATH = os.path.join(DATA_DIR, "tickets.json")
KEY_PATH = os.path.join(DATA_DIR, "eval_key.json")


def load_tickets() -> list[dict]:
    with open(TICKETS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_key() -> dict[str, dict]:
    with open(KEY_PATH, encoding="utf-8") as f:
        return {k["id"]: k for k in json.load(f)}


def main() -> None:
    ap = argparse.ArgumentParser(description="Customer Service Agent - decide one ticket, or all of them.")
    ap.add_argument("--ticket", help="Ticket id to decide, e.g. T004.")
    ap.add_argument("--all", action="store_true", help="Decide every ticket in tickets.json.")
    ap.add_argument("--score", action="store_true",
                    help="Score the decisions against eval_key.json (action + cited clause).")
    args = ap.parse_args()

    tickets = load_tickets()
    if args.ticket:
        tickets = [t for t in tickets if t["id"] == args.ticket]
        if not tickets:
            raise SystemExit(f"No ticket with id {args.ticket}")
    elif not args.all:
        raise SystemExit("Pass --ticket <id> or --all.")

    key = load_key() if args.score else {}
    action_hits = clause_hits = 0

    for ticket in tickets:
        decision = run(ticket, policy_path=POLICY_PATH)
        line = f"{ticket['id']}  {decision['action']:<8} {decision['clause']}"
        if args.score and ticket["id"] in key:
            want = key[ticket["id"]]
            action_ok = decision["action"] == want["expected_action"]
            clause_ok = decision["clause"] == want["expected_policy_clause"]
            action_hits += action_ok
            clause_hits += clause_ok
            line += f"   expected {want['expected_action']}/{want['expected_policy_clause']}"
            line += "   OK" if action_ok and clause_ok else "   MISS"
        print(line)

    if args.score and tickets:
        n = len(tickets)
        print(f"\naction accuracy {action_hits}/{n} ({action_hits * 100.0 / n:.1f}%)  |  "
              f"clause accuracy {clause_hits}/{n} ({clause_hits * 100.0 / n:.1f}%)")


if __name__ == "__main__":
    main()
