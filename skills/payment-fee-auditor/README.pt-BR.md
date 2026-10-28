**Idioma:** [English](README.md) | **Português (Brasil)**

# Payment Fee Auditor

```text
   ___
  | __|   FINCRAFT / PAYMENT-FEE-AUDITOR
  | _|
  |_|
```

**Compare tarifas cobradas e contratadas.**

Compare MDR e tarifas fixas observadas com as condições comerciais vigentes fornecidas. O relatório mantém transações, taxas e memória de cálculo no mesmo lugar.

## Instale no seu agente

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill payment-fee-auditor
```

## Experimente localmente

Na pasta desta skill, com Python 3.10 ou superior:

```bash
python scripts/investigate.py --input examples/fee-discrepancy.json --out /tmp/payment-fee-auditor.json
```

O exemplo mostra uma diferença de tarifa e a memória de cálculo correspondente. Confira o JSON e o Markdown gerados no diretório `/tmp`.

## Como funciona

A entrada utiliza os campos `rates, transactions`. As regras de investigação estão em [`SKILL.md`](SKILL.md), com esquemas e contratos em [`references/`](references/). Os exemplos ficam em [`examples/`](examples/).

A análise usa as evidências fornecidas localmente. Conexões com instituições externas e decisões operacionais exigem integração própria.

[Catálogo de skills](../../README.pt-BR.md) · [Instalação](../../docs/pt-BR/installation.md) · [Código](scripts/)
