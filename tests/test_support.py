"""Contract tests - they fail against the starter stubs; make them pass.

All three run OFFLINE: no network, no ANTHROPIC_API_KEY. The policy is a tiny
in-test fixture (not the full dataset) and the LLM is a fake callable injected
into classify_ticket(), so nothing here ever reaches the Anthropic API.
"""
import json

import pytest

from support import ALLOWED_ACTIONS, classify_ticket, load_policy

# A two-clause policy in the same format as dataset/policy.md.
TINY_POLICY_MD = """# Tiny test policy

## The clauses

### P4 - The 30-day return window
Returns are accepted for 30 days from the delivery date. A ticket with
days_since_delivery greater than 30 is refused. Action: deny.

### P10 - Standard change-of-mind refund
Everything else, inside the window and with a receipt, is refunded in full.
Action: refund.
"""

TINY_TICKET = {
    "id": "T999",
    "customer_message": "Wrong size, tags still on, never worn. Refund please.",
    "order_value": 60.0,
    "days_since_delivery": 5,
    "has_receipt": True,
    "category": "apparel",
    "condition": "new_unopened",
}


def _write_policy(tmp_path):
    path = tmp_path / "policy.md"
    path.write_text(TINY_POLICY_MD, encoding="utf-8")
    return str(path)


def test_load_policy_returns_parsed_clauses_in_order(tmp_path):
    clauses = load_policy(_write_policy(tmp_path))

    assert isinstance(clauses, list) and len(clauses) == 2
    assert [c["id"] for c in clauses] == ["P4", "P10"]  # document order = precedence
    assert clauses[0]["title"].strip() == "The 30-day return window"
    assert "30 days" in clauses[0]["text"]
    assert all(c["text"].strip() for c in clauses)


def test_classify_ticket_returns_a_valid_action_and_a_cited_clause(tmp_path):
    policy = load_policy(_write_policy(tmp_path))
    calls = []

    def fake_llm(prompt: str) -> str:
        calls.append(prompt)
        return json.dumps({"action": "refund", "clause": "P10"})

    result = classify_ticket(TINY_TICKET, policy, llm=fake_llm)

    assert set(result) >= {"action", "clause"}
    assert result["action"] in ALLOWED_ACTIONS
    assert result["clause"] in {c["id"] for c in policy}
    assert len(calls) == 1
    # The prompt must actually carry the policy and the structured fields.
    assert "P10" in calls[0] and "days_since_delivery" in calls[0]


def test_malformed_ticket_raises_instead_of_guessing(tmp_path):
    policy = load_policy(_write_policy(tmp_path))
    calls = []

    def fake_llm(prompt: str) -> str:
        calls.append(prompt)
        return json.dumps({"action": "refund", "clause": "P10"})

    broken = {"id": "T998", "customer_message": "Please refund me."}  # no order fields

    with pytest.raises(ValueError):
        classify_ticket(broken, policy, llm=fake_llm)

    # Validation happens before the model is called: no guessing, no spend.
    assert calls == []
