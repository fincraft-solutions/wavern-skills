# Contrato de evento NF-e (planejamento S06)
JSONL: `event_id`, `timestamp` (ISO 8601 ou unknown), `kind` (`send|receipt_query|key_query|service_status|transport_error`), `key` (44 dígitos quando houver), `env` (`producao|homologacao`), `uf`, `lot_id`, `receipt_id`, `cstat`, `protocol`, `docs` (itens individuais em retorno 104), `source` (`file`, `line`), `origin_claim` (não verificada).

Técnica: agrupar (UF,ambiente,chave); vincular recibo com lote apenas mediante trilha demonstrada; retornar estado *reportado* e não o estado atual da SEFAZ. 204 / 103 / 104 / 105 / 107 isolados não comprovam autorização. 100/150 vinculado à chave e protocolo é *autorização reportada na fonte*, não autenticação oficial do log. 101 cancelamento não equivale a autorização vigente. Havendo retorno individual conflitante, sinalizar conflito e bloqueio.

Na S07 implementar preservação de `source_file:line` e validação de campos sem inferir chaves inexistentes. Tratamento de timestamps fora de ordem respeita sequência causal quando disponível; ordem por data é apenas apresentação.
