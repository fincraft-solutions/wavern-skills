# Wavern Skills

```text
   ___  __________
  |   ||   _____ /   FINCRAFT
  |___||  |____/    OPEN LAB
       |  |
       |__|
```

**Três investigações. Nenhum veredito sem evidência.**


Às vezes a parte difícil não é automatizar uma análise: é **saber o que os arquivos realmente demonstram**. Estas três skills orientam agentes de código a investigar incidentes fiscais e financeiros sem inventar confirmação externa.

Cada skill é uma pasta independente com `SKILL.md`, contratos de entrada, exemplos e um **motor Python determinístico** que funciona sem LLM nem serviços privados. Instale uma, duas ou todas; não precisa da Wavern para rodar os scripts.

## Escolha pela dúvida — não pelo nome da ferramenta

| Investigação | Pergunta de entrada | Saída exemplar | A fronteira |
| --- | --- | --- | --- |
| [NF-e](skills/nfe-incident-investigator/) | O lote retornou 104; a nota foi autorizada? | `indeterminate` quando falta resultado individual | Não consulta SEFAZ |
| [Pagamento duplicado](skills/duplicate-payment-investigator/) | Dois comprovantes indicam dois débitos? | `review_candidate` ou exclusão de reexportação | Não consulta banco |
| [Tarifas](skills/payment-fee-auditor/) | O MDR cobrado bate com contrato vigente? | `discrepancy_candidate` com fórmula e fonte | Não comprova direito à restituição |

## Instale a investigação que você precisa

Dentro do projeto em que seu agente trabalha (Node.js **22.20+**):

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill nfe-incident-investigator
# Ou descubra o catálogo sem instalar:
npx skills@latest add fincraft-solutions/wavern-skills --list
```

O instalador permite escolher seu agente e o escopo da instalação. As atualizações são explícitas (`npx skills@latest check` / `npx skills@latest update`). **A instalação pelo GitHub só pode ser verificada após a publicação pública**; o modo local já pode ser conferido. Veja [INSTALACAO.md](INSTALACAO.md).

## Teste o motor sem instalar skill nenhuma

```bash
cd skills/nfe-incident-investigator
python scripts/investigate.py --input examples/incident-lot-incomplete.json --out /tmp/nfe-report.json
```

Abra `/tmp/nfe-report.json` e `/tmp/nfe-report.md`. O caso demonstra por que um lote processado não basta para afirmar autorização individual. No Windows, escolha um caminho de saída local em vez de `/tmp`.

## Como verificamos — e onde a evidência termina

- **39 testes unitários Python** e **42 casos sintéticos congelados** no conjunto original. Execute os testes pelo workflow de CI ou `python reports/evaluate_frozen.py` na raiz.
- Esses números medem regressão **em dados inventados e definidos previamente**. Não são taxa de acerto com documentos de clientes.
- **Ganho com LLM não comprovado.** O código Python serve de referência verificável; a skill organiza o raciocínio, não dispensa conferência externa.

Os critérios e os experimentos estão em [`reports/`](reports/); limites de privacidade em [`LIMITES-E-PRIVACIDADE.md`](LIMITES-E-PRIVACIDADE.md).

**Continue por:** [instalação](INSTALACAO.md) · [como contribuir](CONTRIBUTING.md) · [releases](RELEASES.md) · [histórico](CHANGELOG.md) · [licença](LICENCIAMENTO.md).

Coleção mantida pela [Fincraft](https://github.com/fincraft-solutions). Traga um caso fictício que faça uma regra falhar — isso ajuda mais do que uma estrela.
