# Payment Fee Auditor

```text
   ___  __________
  |   ||   _____ /   FINCRAFT
  |___||  |____/    OPEN LAB
       |  |
       |__|
```

**A diferença entre bruto e líquido não é sempre MDR.**

Compara tarifas observadas com condições contratuais **fornecidas e datadas**, sem misturar antecipação ou chargeback às taxas de cartão.

A skill combina instruções em [`SKILL.md`](SKILL.md), contratos em [`references/`](references/) e um motor Python executável. Não é necessário criar conta na Wavern.

## Um caso para testar

```bash
# Execute na pasta desta skill; Python 3.10+ (biblioteca padrão)
python scripts/investigate.py --input examples/fee-discrepancy.json --out /tmp/payment-fee-auditor.json
```

Procure o estado **`discrepancy_candidate`** e examine os caminhos de evidência e as lacunas no relatório. Os dados do exemplo são **sintéticos**. A saída também inclui um Markdown de leitura humana.

**Fronteira:** Não consulta adquirentes, não busca contratos automaticamente e não confirma restituição.

## Usar com agente de código

```bash
npx skills@latest add fincraft-solutions/wavern-skills --skill payment-fee-auditor
```

O comando depende de repositório público e ainda precisa de validação pós-publicação; sem CLI, copie a pasta inteira para o diretório de skills do seu agente. Veja [instruções de instalação](../../INSTALACAO.md).

### Entrada e saída

`rates` (condições aprovadas, versões, vigência, modalidade, parcelas, moeda, MDR, fee fixo e arredondamento) e `transactions` (data, bruto, moeda, modalidades, MDR cobrado separadamente, fontes). CSVs opcionais com esses campos. Não usar um anúncio genérico como contrato.

O programa é **somente leitura** dos arquivos de entrada; grava um JSON e um Markdown separados em `--out`. Mostra o estado no terminal. Consulte `references/OUTPUT_AND_SAFETY.md` e o contrato específico em `references/` para detalhes.

### Limites

Sem coleta automática de contratos, sem login em adquirente, sem captura de taxas atualizadas, sem cálculos de antecipação onde fórmula não foi fornecida. A Skill não consulta bancos, adquirentes, SEFAZ ou a Wavern. Resultados são candidatos/alegações documentais, não prova externa. Não use arquivos reais em demos, repositórios, issues ou posts. Hospedar arquivos numa LLM em nuvem pode transmiti-los ao provedor escolhido.

### Diagnóstico rápido

- `python scripts/investigate.py --help` lista modos e parâmetros.
- JSON inválido ou cabeçalhos CSV incompatíveis: normalize para os nomes do contrato; o programa não é conversor universal.
- Arquivo sem informação suficiente: um estado inconclusivo é um resultado legítimo; não invente informações.
- Execução só em chat sem Python: não alegar que o motor foi executado.

### Instalação e distribuição

Para um agente que admite pastas de Skills, coloque **esta pasta** no diretório de Skills apropriado do agente e siga o mecanismo de recarga dele. Instalação via `npx skills` requer publicação do repositório e teste em um ambiente compatível; veja [INSTALACAO.md](../../INSTALACAO.md). Consulte a licença do repositório antes de reutilizar ou distribuir o código.

### Teste local

```bash
python -m unittest discover -s evals -p 'test_*.py' -v
```

Documentos: `SKILL.md` (fluxo do agente), `references/` (contratos), `examples/` (dados sintéticos) e `evals/` (testes). Versão **0.1.0** (primeira implementação S07). Código não implantado em produção. Nenhum ganho de produtividade comprovado com LLM.
