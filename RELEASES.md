# Política de versões

**Versão por coleção, não por arquivo.** A tag `v0.1.0` identifica um snapshot consistente das três skills; consulte `skills/<nome>/CHANGELOG.md` para mudanças individuais. Não há publicação no npm: `npx skills add` instala a partir do repositório GitHub.

- `PATCH`: melhoria de documentação, teste ou bug sem alterar contrato esperado.
- `MINOR`: novo recurso, skill ou campo compatível, após validação.
- `MAJOR`: alteração incompatível no contrato dos motores/saídas ou renomeação de skill.

A primeira versão deve ser um **pre-release**; testes internos com 42 cenários sintéticos não provam uso operacional. Anexe, quando necessário, um ZIP de cada pasta `skills/<nome>/` sem incluir dados reais; para o CLI a tag e o repositório bastam.

Manter changelog e release notes em português objetivo: o que mudou, como testar, limitações e caminho de migração.
