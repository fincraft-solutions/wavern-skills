**Language:** **English** | [Português (Brasil)](../pt-BR/installation.md)

# Installing Wavern Skills

[Back to Wavern Skills](../../README.md)

## With your coding agent

Run this command in your working project:

```bash
npx skills@latest add fincraft-solutions/wavern-skills
```

The installer lets you choose the skills and supported agents. For a specific skill:

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill duplicate-payment-investigator
```

To see the available skills:

```bash
npx skills@latest add fincraft-solutions/wavern-skills --list
```

To check for updates:

```bash
npx skills@latest check
npx skills@latest update
```

## Run without an agent

Each skill also has a standalone Python engine, with no third-party packages required. For example:

```bash
cd skills/payment-fee-auditor
python3 scripts/investigate.py --input examples/fee-discrepancy.json --out /tmp/fee-report.json
```

The output files are written to the path given in `--out`. Review the corresponding `SKILL.md` and `references/` directory for the expected input structure.

## Releases

Versions are tagged for the collection. Each skill keeps its own changelog in its folder. You can pin a Git tag when you need a stable revision of the source files. The installer copies the selected skill into your agent's environment; you can edit the installed files to suit your workflow.
