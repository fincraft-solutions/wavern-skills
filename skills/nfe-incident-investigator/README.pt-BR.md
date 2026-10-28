**Idioma:** [English](README.md) | **Português (Brasil)**

# NF-e Incident Investigator

```text
   ___
  | __|   FINCRAFT / NFE-INCIDENT-INVESTIGATOR
  | _|
  |_|
```

**Correlacione eventos do lote e do documento.**

Investigue incidentes de NF-e com rastreabilidade de recibos, ambiente, chave e protocolo. A skill organiza a linha do tempo de transmissão e ajuda a localizar eventos contraditórios.

## Instale no seu agente

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill nfe-incident-investigator
```

## Experimente localmente

Na pasta desta skill, com Python 3.10 ou superior:

```bash
python scripts/investigate.py --input examples/incident-lot-incomplete.json --out /tmp/nfe-incident-investigator.json
```

O exemplo mostra um lote processado sem informação suficiente para concluir sobre a autorização individual. Confira o JSON e o Markdown gerados no diretório `/tmp`.

## Como funciona

A entrada utiliza os campos `events, target, target_env`. As regras de investigação estão em [`SKILL.md`](SKILL.md), com esquemas e contratos em [`references/`](references/). Os exemplos ficam em [`examples/`](examples/).

A análise usa as evidências fornecidas localmente. Conexões com instituições externas e decisões operacionais exigem integração própria.

[Catálogo de skills](../../README.pt-BR.md) · [Instalação](../../docs/pt-BR/installation.md) · [Código](scripts/)
