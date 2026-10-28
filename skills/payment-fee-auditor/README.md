**Language:** **English** | [Português (Brasil)](README.pt-BR.md)

# Payment Fee Auditor

```text
   ___
  | __|   FINCRAFT / PAYMENT-FEE-AUDITOR
  | _|
  |_|
```

**Check card processing fees against the contract you supplied.**

Compare observed MDR and fixed fees with dated commercial terms. The report keeps transaction evidence, applied rates and calculation steps together.

## Install for your agent

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill payment-fee-auditor
```

## Run a local example

From this skill's directory, with Python 3.10 or newer:

```bash
python scripts/investigate.py --input examples/fee-discrepancy.json --out /tmp/payment-fee-auditor.json
```

The example reports a fee difference and shows how it was calculated. Open the JSON report and its companion Markdown file in `/tmp`.

## How it works

The input uses `rates, transactions`. Agent instructions live in [`SKILL.md`](SKILL.md), supported by contracts in [`references/`](references/). Explore sample inputs and outputs in [`examples/`](examples/).

The investigator works with the evidence you supply. External verification and operational actions require additional integrations.

[All skills](../../README.md) · [Installation](../../docs/en/installation.md) · [Source](scripts/)
