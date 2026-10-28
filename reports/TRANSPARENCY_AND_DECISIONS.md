# S07 — Relatório de resultados, decisões e limitações

## Escopo fechado
As Skills C02, B07 e B02 foram escolhidas na S06 e a S6.5 revisou a arquitetura estudando o projeto `grilling` de Matt Pocock. S07 **implementou** as três, sem reabrir seleção nem prolongar o processo em S08. Os arquivos foram escritos como Skills autossuficientes; não usam serviços privados da Wavern.

## Evidência objetiva
- SHA-256 de `CASES_FROZEN_S06_v1.json`: `c5dfd03cd32c997dc37cae195a6ad9b19ef9bef00cb28664307879eefe8f85a9` (inalterado entre S06/S6.5/S07).
- Testes prévios à implementação: 14 cenários NF-e, 14 de duplicidade e 14 de tarifa. Primeiro run: **41/42**; FE13 revelou problema no agregador de transações repetidas. Correção ocorreu **no motor**, sem mudar dados/oráculo. Run subsequente: **42/42**, zero falhas críticas nesse conjunto.
- Testes adversariais adicionais posteriores à S06: unittest por Skill, incluindo entradas adversas, comando malicioso em log, recibo ambíguo, status de pagamento, devolução parcial, contrato vencido, fixed fee diferente e falha de sobrescrita direta da entrada.
- Demonstrações de CLI geraram JSON e Markdown para cada Skill. A execução não depende de API e não contatou SEFAZ, PSP, banco, provedor LLM ou Wavern.
- Ver `QUALITY_AUDIT.json` para validação de metadados, testes e ZIPs.

## Comparação causal honesta
A linha **B1** é o mesmo motor determinístico executado diretamente, *sem LLM*. B1 e o motor disponível para T empatam em **42/42** no conjunto já estruturado. A linha B0 é propositalmente fraca e não é a referência adequada para alegar superioridade. Isto demonstra precisão sobre fixtures específicas, **não** eficácia diferencial das instruções de LLM.

**LLM_COMPARATIVE_NOT_EXECUTED.** Não houve agente hospedeiro disponível para instalar a Skill e medir ativação, seleção de referências, qualidade de perguntas ou melhoria sobre a LLM sem Skill. Os 12 cenários adicionais S6.5 são rubrica preparada, não resultados experimentais.

## Limites reais / riscos residuais
- Classificação feita sobre dados padronizados. A LLM ainda terá de extrair XML/log/CSV heterogêneo com proveniência; isso não foi avaliado ponta a ponta.
- NF-e: origem `sefaz_response` no arquivo é uma alegação não autentificada. 100+protocolo produz `reported_authorization`, nunca veredito fiscal atual. Correlacionador não cobre todos os layouts de retorno de provedores nem eventos históricos complexos.
- Duplicidade: `review_candidate` significa sobrepagamento potencial na mesma obrigação com evidências alegadas. Não valida settlement bancário nem obrigações contratualmente consolidadas, e regras simplificadas podem produzir candidatos falsos em pagamentos parciais complexos.
- Tarifas: restringe-se a MDR e tarifa fixa separáveis, com `HALF_UP` explicitado, sem fórmula de antecipação nem reconciliação contábil completa. Tarifas de fornecedores podem ter condições especiais não representadas.
- CSVs exigem nomes de colunas do contrato; PDF escaneado não tem OCR nativo; scripts não autentificam digitalmente documentos.
- Os dados são sintéticos e parcialmente alinhados ao design do motor. **42/42 não é estimativa de acurácia real.**
- A publicação pública e licença open source dependem de autorização do titular. A identificação Wavern é crédito de criação, sem login, rastreamento ou publicidade durante a análise.

## Desfecho
**Entrega técnica concluída; confiança nas propriedades determinísticas testadas: alta dentro do domínio dos 42 casos. Confiança de valor adicional de LLM/uso em produção: indeterminada por falta de A/B com modelos e documentos reais.** Nenhuma Sprint adicional foi criada.
