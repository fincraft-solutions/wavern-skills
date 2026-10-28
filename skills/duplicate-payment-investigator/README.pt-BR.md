**Idioma:** [English](README.md) | **Português (Brasil)**

# Duplicate Payment Investigator

```text
   ___
  | __|   FINCRAFT / DUPLICATE-PAYMENT-INVESTIGATOR
  | _|
  |_|
```

**Compare obrigações e registros de liquidação.**

Compare obrigações, transações, liquidações e devoluções em uma mesma análise. A skill ajuda a distinguir reexportações do extrato de situações que merecem investigação.

## Instale no seu agente

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill duplicate-payment-investigator
```

## Experimente localmente

Na pasta desta skill, com Python 3.10 ou superior:

```bash
python scripts/investigate.py --input examples/double-payment-candidate.json --out /tmp/duplicate-payment-investigator.json
```

O resultado indica um candidato à conferência e os registros que sustentam o apontamento. Confira o JSON e o Markdown gerados no diretório `/tmp`.

## Como funciona

A entrada utiliza os campos `payments, obligations, refunds`. As regras de investigação estão em [`SKILL.md`](SKILL.md), com esquemas e contratos em [`references/`](references/). Os exemplos ficam em [`examples/`](examples/).

A análise usa as evidências fornecidas localmente. Conexões com instituições externas e decisões operacionais exigem integração própria.

[Catálogo de skills](../../README.pt-BR.md) · [Instalação](../../docs/pt-BR/installation.md) · [Código](scripts/)
