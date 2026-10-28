**Idioma:** [English](README.md) | **Português (Brasil)**

# Wavern Skills

```text
   ___
  | __|   FINCRAFT / WAVERN SKILLS
  | _|
  |_|
```

**Um conjunto de skills para investigar registros fiscais e financeiros com mais contexto.**

Estas skills ajudam agentes de programação a organizar documentos, eventos e transações em casos que uma pessoa consegue revisar. Cada uma reúne instruções para o agente, dados de exemplo e um pequeno motor Python. Você pode instalar as skills em agentes compatíveis ou executar os exemplos diretamente.

## Instale uma skill

```bash
npx skills@latest add fincraft-solutions/wavern-skills
```

Escolha as skills durante a instalação. Para instalar apenas a investigadora de NF-e:

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill nfe-incident-investigator
```

Veja o [guia de instalação](docs/pt-BR/installation.md) para instalação individual, execução local e atualizações.

## A coleção

| Skill | O que investiga |
| --- | --- |
| [NF-e Incident Investigator](skills/nfe-incident-investigator/README.pt-BR.md) | Emissão de NF-e, recibos, respostas cStat e conflitos de protocolo. |
| [Duplicate Payment Investigator](skills/duplicate-payment-investigator/README.pt-BR.md) | Possíveis pagamentos duplicados, extratos repetidos e devoluções. |
| [Payment Fee Auditor](skills/payment-fee-auditor/README.pt-BR.md) | MDR, tarifas fixas e divergências em relação às taxas contratadas. |

## Rode um exemplo

Os motores Python usam apenas a biblioteca padrão. Comece pela investigação de NF-e:

```bash
cd skills/nfe-incident-investigator
python3 scripts/investigate.py --input examples/incident-lot-incomplete.json --out /tmp/nfe-report.json
```

Abra `/tmp/nfe-report.json` e `/tmp/nfe-report.md` para explorar a linha do tempo, a conclusão fundamentada nos eventos e as informações ainda necessárias.

## Adapte ao seu trabalho

As skills são arquivos comuns. Leia o [`SKILL.md`](skills/nfe-incident-investigator/SKILL.md) e os [contratos de referência](skills/nfe-incident-investigator/references/) para entender as instruções do agente. Você pode modificar o fluxo para atender às necessidades da sua equipe.

Os exemplos usam registros fictícios. Investigações reais dependem de entradas confiáveis e de verificações externas realizadas pelas ferramentas da sua operação.

[Instalação](docs/pt-BR/installation.md) · [Como contribuir](CONTRIBUTING.pt-BR.md) · [Histórico](CHANGELOG.pt-BR.md) · [Fincraft](https://github.com/fincraft-solutions)
