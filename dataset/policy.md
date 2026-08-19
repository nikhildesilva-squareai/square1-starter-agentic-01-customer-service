# Northbeam Supply Co. - Returns & Refunds Policy

Version 4.2. Effective for all consumer orders placed through the Northbeam web
store. This document is the single source of truth for return decisions. Support
agents (human or automated) must decide exactly one action per ticket:

`refund` | `replace` | `deny` | `escalate`

Every decision must cite the clause id (P1 - P10) it rests on.

---

## Order of precedence (read this first)

Clauses are evaluated **strictly in order, P1 first**. The first clause whose
condition is met decides the ticket, and evaluation stops there. A later clause
never overrides an earlier one. If no clause P1 - P9 applies, P10 decides.

---

## The clauses

### P1 - Abusive, threatening or hostile messages
Any message containing abusive language directed at Northbeam or its staff
(profanity, insults such as "idiots" or "morons"), threats of legal action
("lawyer", "sue", "legal action", "take you to court"), or threats to report the
company to an authority ("report you to", "trading standards") is escalated to a
human agent immediately. Do not attempt to resolve the return yourself, and do
not let the merits of the underlying request change this. **Action: `escalate`.**

### P2 - High-value orders
Any order with an `order_value` **above 500.00** must be reviewed by a human
before money or stock moves, whatever the state of the goods. **Action:
`escalate`.**

### P3 - Damaged on arrival
Goods recorded as `damaged_on_arrival` are always replaced with an identical
item. This applies **regardless of the return window and regardless of whether a
receipt is held** - carrier damage is Northbeam's liability, not the customer's.
**Action: `replace`.**

### P4 - The 30-day return window
Returns are accepted for **30 days from the delivery date**. A ticket with
`days_since_delivery` **greater than 30** is outside the window and is refused.
Day 30 itself is inside the window. Sympathy, urgency or a good reason does not
extend it. Where the customer's message and the `days_since_delivery` field
disagree about when the goods arrived, **the `days_since_delivery` field is
authoritative** - it comes from the carrier's confirmed delivery scan.
**Action: `deny`.**

### P5 - Proof of purchase required
A return requires proof of purchase. Where `has_receipt` is **false** - the
customer has confirmed they hold no receipt, order number or confirmation email
- the return is refused. **Action: `deny`.**

### P6 - Receipt status unknown
Where `has_receipt` is **null** - the customer has not confirmed either way, for
example because the order may sit under another name or a former email address -
do not guess. The ticket goes to a human who can look the order up. **Action:
`escalate`.**

### P7 - Faulty goods
Goods recorded as `defective` - they arrived intact but do not work as sold -
are replaced with an identical item. **Action: `replace`.**

### P8 - Used goods
Goods recorded as `used` cannot be resold and are not eligible for return under
the change-of-mind provisions. Note that a `defective` or `damaged_on_arrival`
item is handled by P3 or P7 above and never reaches this clause. **Action:
`deny`.**

### P9 - Electronics restocking fee
Change-of-mind returns in the `electronics` category are refunded **less a 15%
restocking fee** on the order value. The action is still a refund; the fee is
applied at settlement. **Action: `refund`.**

### P10 - Standard change-of-mind refund
Everything else - inside the window, receipt held, goods `new_unopened` or
`opened_unused`, not electronics - is refunded in full to the original payment
method. **Action: `refund`.**

---

## Field reference

| Field | Meaning |
|---|---|
| `order_value` | Total paid, in USD. |
| `days_since_delivery` | Whole days between the carrier delivery scan and the ticket. Authoritative. |
| `has_receipt` | `true` = proof held, `false` = customer confirmed none, `null` = not established. |
| `category` | `electronics`, `apparel`, `home`, `outdoors`, `accessories`. |
| `condition` | `new_unopened`, `opened_unused`, `used`, `defective`, `damaged_on_arrival`. |

_Northbeam Supply Co. is a fictional company. This policy is synthetic teaching
material owned by Square 1 AI._
