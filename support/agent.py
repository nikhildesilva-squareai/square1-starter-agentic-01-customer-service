"""
Customer Service Agent - policy-grounded ticket triage.

An inbound ticket arrives. You read the written returns policy, apply it to the
ticket, and decide exactly one action - refund, replace, deny or escalate -
citing the policy clause the decision rests on.

The three tests in tests/ define the contract for load_policy(),
classify_ticket() and the malformed-input behaviour. Implement the stubs until
they pass, then wire run() to the real Anthropic loop.

The LLM is injected, never imported at call time: classify_ticket() takes an
`llm` callable so tests can pass a fake and run offline with no API key.

Models (current ids only - NEVER claude-3-*, never claude-sonnet-4-*):
  - default: claude-sonnet-5
  - cheap:   claude-haiku-4-5-20251001
  - hard:    claude-opus-5
Read the key from the ANTHROPIC_API_KEY environment variable only.
"""
from __future__ import annotations

from typing import Any, Callable

# The only actions the agent may return. Anything else is a bug, not a decision.
ALLOWED_ACTIONS = ("refund", "replace", "deny", "escalate")

# Every field a ticket must carry before it can be classified.
REQUIRED_FIELDS = (
    "id",
    "customer_message",
    "order_value",
    "days_since_delivery",
    "has_receipt",
    "category",
    "condition",
)

DEFAULT_MODEL = "claude-sonnet-5"
CHEAP_MODEL = "claude-haiku-4-5-20251001"


def load_policy(path: str) -> list[dict[str, str]]:
    """Parse policy.md into an ordered list of clauses.

    Clause headings in policy.md have the form:  `### P4 - The 30-day return window`
    The body of a clause is every line up to the next `### ` heading.

    TODO: return a list of dicts, in document order, each with:
        {"id": "P4", "title": "The 30-day return window", "text": "<clause body>"}
    Read the file with encoding="utf-8". Ignore headings that are not clause
    headings (`# `, `## `). The order matters - it is the precedence ladder the
    policy tells you to walk, and the tests and the eval key both depend on it.
    """
    raise NotImplementedError("Implement load_policy")


def build_prompt(ticket: dict[str, Any], policy: list[dict[str, str]]) -> str:
    """Render the policy + the ticket into the prompt you send to the model.

    TODO: produce a single string that contains (a) every clause in order with
    its id, (b) the ticket's structured fields, (c) the customer message, and
    (d) an instruction to answer with JSON only:
        {"action": "<one of ALLOWED_ACTIONS>", "clause": "<clause id>"}
    Make the precedence rule and the "structured fields beat the prose" rule
    explicit - the model will not infer them from a wall of text.
    """
    raise NotImplementedError("Implement build_prompt")


def classify_ticket(
    ticket: dict[str, Any],
    policy: list[dict[str, str]],
    llm: Callable[[str], str] | None = None,
) -> dict[str, str]:
    """Decide one action for one ticket and cite the clause it rests on.

    Args:
        ticket: a dict carrying every field in REQUIRED_FIELDS.
        policy: the clause list returned by load_policy().
        llm:    a callable taking a prompt string and returning the model's raw
                text. Defaults to the Anthropic-backed client (see _default_llm).
                Tests inject a fake so they run with no API key.

    Returns:
        {"action": <one of ALLOWED_ACTIONS>, "clause": <a clause id from policy>}

    TODO:
      1. Validate the ticket first. If a field in REQUIRED_FIELDS is missing, or
         the ticket is not a dict, raise ValueError. Never guess an action for a
         malformed ticket - a wrong refund costs real money.
      2. Build the prompt, call `llm`, parse the JSON it returns.
      3. Validate the result: action must be in ALLOWED_ACTIONS and clause must
         be an id present in `policy`. If the model returns anything else, raise
         ValueError rather than passing garbage downstream.
    """
    raise NotImplementedError("Implement classify_ticket")


def run(ticket: dict[str, Any], policy_path: str = "data/policy.md") -> dict[str, Any]:
    """Full loop for one ticket: load policy -> classify -> draft the reply.

    TODO:
      1. policy = load_policy(policy_path)
      2. decision = classify_ticket(ticket, policy) using the real Anthropic
         client (anthropic.Anthropic() reads ANTHROPIC_API_KEY from the env).
      3. Draft a short customer-facing reply that states the outcome and quotes
         the clause that produced it. On `escalate`, say a human will follow up -
         do not promise money or stock.
      4. Return {"id", "action", "clause", "reply"}.

    Keep the model call in one place so the cheap model (claude-haiku-4-5-20251001)
    can be swapped in for the reply draft while the decision stays on
    claude-sonnet-5. Never hardcode an API key.
    """
    raise NotImplementedError("Implement run")


def _default_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Anthropic-backed llm callable: prompt in, raw model text out.

    TODO: call the Messages API with `model`, return the text of the first
    content block. Read the key from ANTHROPIC_API_KEY (the SDK does this for
    you - do not pass a literal key). Raise a clear error if the key is unset.
    """
    raise NotImplementedError("Implement _default_llm")
