> Documentation: [English](docs/en/installation.md) | [Português (Brasil)](docs/pt-BR/installation.md)

# Instalação sem mistério

## Usar apenas Python

Não é preciso instalar uma Skill para rodar o motor. Entre numa pasta em `skills/` e execute `python scripts/investigate.py --help`. Os scripts usam Python 3.10+ e apenas a biblioteca padrão.

## Adicionar a um agente

Copie **uma pasta inteira** para o diretório que seu agente reconhece. Por exemplo, dentro do seu projeto:

```bash
mkdir -p .agents/skills
cp -R skills/nfe-incident-investigator .agents/skills/
```

Para Claude Code, use `.claude/skills/` no lugar de `.agents/skills/`. Reinicie/recarregue a sessão do agente quando necessário. Confira se o `SKILL.md` foi identificado antes de atribuir qualquer resultado ao agente.

## Instalar por CLI — somente após publicação

```bash
npx skills add fincraft-solutions/wavern-skills --skill duplicate-payment-investigator
```

O instalador depende de versões atuais de Node e de acesso à rede. **Esse caminho ainda deve ser validado em ambiente real**; a cópia manual e os scripts Python são o fallback documentado. O CLI pode coletar telemetria anônima por padrão; consulte [a documentação de privacidade](https://www.skills.sh/docs/cli).

Os três motores usam dados sintéticos no repositório e não possuem conexão com serviços privados da Wavern. Ao fornecer arquivos reais a um agente de IA, revise a política do provedor e remova informações pessoais/sigilosas.
