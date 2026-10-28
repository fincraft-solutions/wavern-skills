**Language:** **English** | [Português (Brasil)](README.pt-BR.md)

# NF-e Incident Investigator

```text
   ___
  | __|   FINCRAFT / NFE-INCIDENT-INVESTIGATOR
  | _|
  |_|
```

**Trace an NF-e incident from transmission logs to the individual document.**

Reconstruct an NF-e timeline from receipts, environment, document keys and protocol events. Follow the evidence through timeouts, batch responses and conflicting entries.

## Install for your agent

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill nfe-incident-investigator
```

## Run a local example

From this skill's directory, with Python 3.10 or newer:

```bash
python scripts/investigate.py --input examples/incident-lot-incomplete.json --out /tmp/nfe-incident-investigator.json
```

The sample shows a processed batch without sufficient evidence of a document-level authorization. Open the JSON report and its companion Markdown file in `/tmp`.

## How it works

The input uses `events, target, target_env`. Agent instructions live in [`SKILL.md`](SKILL.md), supported by contracts in [`references/`](references/). Explore sample inputs and outputs in [`examples/`](examples/).

The investigator works with the evidence you supply. External verification and operational actions require additional integrations.

[All skills](../../README.md) · [Installation](../../docs/en/installation.md) · [Source](scripts/)
