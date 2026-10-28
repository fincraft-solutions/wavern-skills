**Idioma:** [English](../en/installation.md) | **Português (Brasil)**

# Instalação do Wavern Skills

[Voltar para Wavern Skills](../../README.pt-BR.md)

## No seu agente de programação

Dentro do projeto em que você trabalha, execute:

```bash
npx skills@latest add fincraft-solutions/wavern-skills
```

O instalador permite escolher as skills e o agente compatível. Para instalar somente uma:

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill duplicate-payment-investigator
```

Para listar o catálogo:

```bash
npx skills@latest add fincraft-solutions/wavern-skills --list
```

Para conferir atualizações:

```bash
npx skills@latest check
npx skills@latest update
```

## Execução sem agente

Cada skill também oferece um motor Python independente, sem bibliotecas de terceiros:

```bash
cd skills/payment-fee-auditor
python3 scripts/investigate.py --input examples/fee-discrepancy.json --out /tmp/fee-report.json
```

Os arquivos de saída ficam no caminho informado em `--out`. Leia o `SKILL.md` e a pasta `references/` para conhecer o formato das entradas.

## Versões

As tags identificam versões da coleção. Cada skill mantém seu próprio changelog. É possível fixar uma tag do Git quando a equipe precisar de uma revisão específica. O instalador copia os arquivos selecionados para o ambiente do agente, permitindo adaptações locais.
