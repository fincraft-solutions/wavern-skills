**Language:** **English** | [Português (Brasil)](README.pt-BR.md)

# Wavern Skills

```text
   ___
  | __|   FINCRAFT / WAVERN SKILLS
  | _|
  |_|
```

**Give your coding agent a better way to investigate financial records.**

We use these skills to organize messy evidence into cases that someone can actually review. Each one comes with an agent instruction file, example data and a small Python engine. You can install a skill into a supported coding agent or run its examples directly.

## Install a skill

```bash
npx skills@latest add fincraft-solutions/wavern-skills
```

Choose the skills that belong in your project when prompted. To install only the NF-e investigator:

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill nfe-incident-investigator
```

See the [installation guide](docs/en/installation.md) for individual installs, local execution and updates.

## The collection

| Skill | What it helps you investigate |
| --- | --- |
| [NF-e Incident Investigator](skills/nfe-incident-investigator/) | NF-e transmission timelines, receipts, cStat responses and protocol conflicts. |
| [Duplicate Payment Investigator](skills/duplicate-payment-investigator/) | Duplicate settlements, repeated exports and refund records. |
| [Payment Fee Auditor](skills/payment-fee-auditor/) | Card MDR, fixed charges and differences against agreed rates. |

## Take one for a spin

The Python engines run with the standard library. Start with the NF-e example:

```bash
cd skills/nfe-incident-investigator
python3 scripts/investigate.py --input examples/incident-lot-incomplete.json --out /tmp/nfe-report.json
```

Open `/tmp/nfe-report.json` and `/tmp/nfe-report.md`. You'll see the timeline, a conclusion based on the supplied events, and the gaps left to investigate.

## Make them yours

Skills are ordinary files. Read the [`SKILL.md`](skills/nfe-incident-investigator/SKILL.md) and the associated [reference contracts](skills/nfe-incident-investigator/references/) to understand how the agent is guided. Fork the repo, adjust the workflow and keep the parts that fit your team.

The examples use fabricated records. For real investigations, prepare the input carefully and confirm external facts through your own systems.

[Installation](docs/en/installation.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md) · [Fincraft](https://github.com/fincraft-solutions)
