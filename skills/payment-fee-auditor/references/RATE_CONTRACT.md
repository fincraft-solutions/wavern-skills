# Contrato de tarifa (planejamento S06)
`rate_schedule`: `contract_id`, `version`, `approved_by_user`, `effective_from`, `effective_to`, `provider`, `channel`, `brand`, `modality`, `installments`, `currency`, `mdr_percent` (decimal), `fixed_fee` (decimal), `rounding_rule` (`HALF_UP` apenas quando explicitamente confirmado), `tolerance` (valor; nunca presumir), `source_file`, `source_location`.

`transactions`: `transaction_id`, `occurred_at`, `gross_amount`, `currency`, `provider`, `channel`, `brand`, `modality`, `installments`, `charged_mdr`, `charged_fixed`, `anticipated` e componentes adicionais quando declarados, `source_file`, `source_row`.

Compatibilidade requer modalidade, parcelas, moeda, bandeira (ou wildcard declarada), vigência sem conflito e método de cálculo explicitamente confirmado. Antecipação só deve ser computada se houver contrato com fórmula inequívoca; caso contrário classificar à parte. Divergência bruto→líquido sozinha não identifica tarifa específica. Se '0,00' for de tarifa ausente em vez de tarifa cobrada, bloquear comparação.
