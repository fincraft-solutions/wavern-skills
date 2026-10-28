> Documentation: [English](README.md) | [Português (Brasil)](docs/pt-BR/installation.md)

# Limites, segurança e interpretação

Estes programas avaliam **registros fornecidos pelo usuário**, não a verdade definitiva registrada por bancos, SEFAZ ou prestadores.

- **NF-e:** uma autorização declarada num log é evidência reportada, não confirmação de status atual. Não reenviar, cancelar ou emitir automaticamente com base na saída.
- **Duplicidade:** um `review_candidate` significa "merece investigação", não dinheiro recuperável ou duplicidade comprovada.
- **Tarifas:** só interpreta MDR e tarifa fixa separáveis com contrato identificável; não substitui conciliação financeira completa.
- **Privacidade:** os scripts Python não fazem chamadas de rede e os exemplos são sintéticos. A execução *por um modelo hospedado* pode enviar conteúdo ao provedor desse modelo. Não use contratos, CNPJ, extratos, tokens nem XMLs reais em issues, demonstrações ou posts.
- **Evidência:** 42/42 casos estruturados e 39 testes de Python não medem eficácia com agentes de IA nem acurácia em documentos reais. A avaliação comparativa com LLM não foi realizada.

Mais detalhes e ressalvas estão em [`reports/TRANSPARENCY_AND_DECISIONS.md`](reports/TRANSPARENCY_AND_DECISIONS.md).
