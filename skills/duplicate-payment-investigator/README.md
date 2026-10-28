**Language:** **English** | [Português (Brasil)](README.pt-BR.md)

# Duplicate Payment Investigator

```text
   ___
  | __|   FINCRAFT / DUPLICATE-PAYMENT-INVESTIGATOR
  | _|
  |_|
```

**Find the evidence behind a possible duplicate payment.**

Compare obligations, transaction IDs, settlements and refunds in one review. The investigator helps distinguish a repeated bank export from a second payment worth following up.

## Install for your agent

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill duplicate-payment-investigator
```

## Run a local example

From this skill's directory, with Python 3.10 or newer:

```bash
python scripts/investigate.py --input examples/double-payment-candidate.json --out /tmp/duplicate-payment-investigator.json
```

The result highlights a candidate for review, along with the records that led to it. Open the JSON report and its companion Markdown file in `/tmp`.

## How it works

The input uses `payments, obligations, refunds`. Agent instructions live in [`SKILL.md`](SKILL.md), supported by contracts in [`references/`](references/). Explore sample inputs and outputs in [`examples/`](examples/).

The investigator works with the evidence you supply. External verification and operational actions require additional integrations.

[All skills](../../README.md) · [Installation](../../docs/en/installation.md) · [Source](scripts/)
