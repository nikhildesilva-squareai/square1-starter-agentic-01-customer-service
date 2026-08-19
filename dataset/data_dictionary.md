# Sample material — Customer Service Agent

**Synthetic — Square 1-owned, free for learners.** Three files: a written policy, a queue of inbound tickets, and an answer key. Together they let the whole decide-and-cite loop run and be scored **offline**, so your contract tests are deterministic.

> ⚠️ Northbeam Supply Co., every customer message, product, price and date below is **invented**. No real people, orders or companies appear here.

Regenerate any time with `python generate_dataset.py` (seed 42) — output is byte-identical on re-run.

## `policy.md`

The returns and refunds policy the agent must apply. Ten clauses, `P1` … `P10`, each under a heading of the form `### P4 - The 30-day return window`, plus an explicit **order of precedence**: clauses are evaluated strictly in order, the first clause whose condition is met decides the ticket, and evaluation stops there. Your `load_policy()` parses this file; the clause ids are what your decisions must cite.

Read it properly before you write a prompt. The 30-day window, the receipt requirement, the electronics restocking fee, damaged-on-arrival, the high-value threshold and the tone rule all interact, and the interactions are decided by precedence rather than by which clause sounds most relevant.

## `tickets.json`

45 inbound tickets. One JSON array; each element:

| Field | Type | Description |
|---|---|---|
| `id` | string | Ticket id, e.g. `T004`. |
| `customer_message` | string | What the customer actually wrote — free text, no fixed structure. |
| `order_value` | number | Total paid in USD. |
| `days_since_delivery` | integer | Whole days between the carrier's delivery scan and the ticket. |
| `has_receipt` | boolean \| null | `true` = proof of purchase held, `false` = customer confirmed none, **`null` = not established**. |
| `category` | string | `electronics`, `apparel`, `home`, `outdoors`, `accessories`. |
| `condition` | string | `new_unopened`, `opened_unused`, `used`, `defective`, `damaged_on_arrival`. |

Ticket order is shuffled, so position tells you nothing about the outcome.

### The dirt you have to handle

- **Prose that contradicts the fields.** Several customers state a delivery date that disagrees with `days_since_delivery` — in both directions (one insists they are inside the window when they are not; another says "back in March" about a two-week-old order). The policy tells you which one wins. An agent that reasons from the message text alone will get these wrong.
- **Sympathetic, urgent, well-argued requests that are still refused.** Tone is not evidence. Some of the most reasonable-sounding messages are outside the window.
- **`has_receipt: null` is not `false`.** Two tickets have unestablished receipt status; treating unknown as "no" produces the wrong action.
- **Escalations triggered by tone, not by numbers.** A few messages are hostile or threatening. One of them would otherwise be a straightforward refusal — precedence decides.
- **Near-duplicate messages about the same product** that resolve differently because one structured field differs. Do not pattern-match on wording.

## `eval_key.json`

The answer key, so you can score a batch run without grading prose.

| Field | Type | Description |
|---|---|---|
| `id` | string | Ticket id (join to `tickets.json`). |
| `expected_action` | string | One of `refund`, `replace`, `deny`, `escalate`. |
| `expected_policy_clause` | string | The clause id the decision must rest on, e.g. `P4`. |

**The signal:** every `expected_action` follows deterministically from the ticket's fields plus the policy's precedence order — the policy is complete enough that there is exactly one defensible answer per ticket. So a correct agent recovers the key, and a plausible-but-wrong one (keyword matching on the message, ignoring precedence, trusting the customer's date) measurably does not. Score both columns: the action **and** the cited clause. Getting the right action from the wrong clause means you got lucky, and it will not hold on the next ticket.

_Licence: Sample material — Square 1-owned (synthetic). No attribution required._
