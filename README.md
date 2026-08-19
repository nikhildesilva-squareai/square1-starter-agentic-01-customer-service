# Customer Service Agent — Square 1 AI starter

**Part of [Square 1 AI](https://square1-tutor.vercel.app) · Agentic AI · Project 1.**

✅ **Data included.** The dataset is committed in [`dataset/`](dataset/) — the same standardized, 100% synthetic, Square 1-owned dataset every learner uses (no third-party or personal data). You can also download it as a single zip from the project page on Square 1.

The instructions below refer to `data/`. The data is already here — either copy it across (`mkdir -p data && cp -r dataset/* data/`) or point the commands straight at `dataset/`. Nothing to download.

🚀 **Start here.** Implement the function stubs (they `raise NotImplementedError`) until the contract tests pass, then build out the full solution described in the project brief. Nova reviews your code + git history.

```bash
pip install -r requirements.txt
python -m pytest tests -q   # 3 contract tests, all failing — make them pass
```

MIT licensed — fork it, build on it, put it in your portfolio.

---

# Customer Service Agent — starter

Starter for Square 1 AI **Agentic AI · Project 1**. Build an agent that reads an inbound support ticket, applies a written returns policy, and decides one action — `refund`, `replace`, `deny` or `escalate` — citing the clause it relied on.

## Setup
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...                      # live runs only, never for tests
```

## Get the sample material
Download `policy.md`, `tickets.json` and `eval_key.json` from your project page (Resources → Dataset) into `data/`.

## Your task
Three tests define the contract — they fail until you implement the stubs in `support/agent.py`:
```bash
pytest -q
python -m support.cli --ticket T004
python -m support.cli --all --score      # scores action + cited clause against eval_key.json
```
`load_policy(path)` → parsed clauses in document order · `classify_ticket(ticket, policy, llm=None)` → `{"action", "clause"}` · `run(ticket)` → the full loop, decision plus a customer-facing reply.

The tests run **offline**: the policy is a tiny in-test fixture and the LLM is a fake callable passed in as `llm=`, so no key and no network. That injection point is the design — keep it, or the tests stop being reproducible.

## The two things that decide your score
1. **Precedence.** `policy.md` is evaluated strictly in order, P1 first, first match wins. A later clause never overrides an earlier one. Most wrong answers come from applying the "obvious" clause instead of the first matching one.
2. **Structured fields beat the prose.** Some customers state a delivery date that contradicts `days_since_delivery`. The field comes from the carrier scan and wins. Some messages sound urgent and deserving and are still outside the window.

Also: `has_receipt` can be `null` (unknown), which is not the same as `false`. Never guess an action for a ticket with missing fields — raise instead.

## Rules
Use **current model ids only** — `claude-sonnet-5` (default), `claude-haiku-4-5-20251001` (cheap path), `claude-opus-5` (hard cases). Never `claude-3-*`, never `claude-sonnet-4-*`. Read the key from `ANTHROPIC_API_KEY` only — never hardcode or commit it.

Full brief, rubric and references are on your Square 1 project page. MIT licensed.
