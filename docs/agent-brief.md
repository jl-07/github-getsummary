# Agent Brief — git-career-telemetry

## Objetivo do projeto
Ferramenta em Python que coleta dados públicos do GitHub (API), analisa consistência de atividade (gaps entre commits) e gera relatórios (Markdown/HTML) + gráficos.

## Como rodar (local)
- Criar venv e instalar deps.
- Rodar testes antes e depois de mudanças.
- Gerar um relatório de exemplo para validar.

## Regras / Restrições (importante)
- NÃO ler nem imprimir conteúdo de arquivos sensíveis: .env, tokens, chaves, credenciais.
- NÃO commitar venv/, reports/ e cache/ (se estiverem no .gitignore, manter).
- NÃO mudar formato de saída dos relatórios sem avisar e justificar.
- Mudanças devem ser pequenas, com commits claros.

## Definition of Done (DoD)
- `pytest` passando
- Lint/format OK (se existir ruff/black)
- README atualizado quando necessário
- Exemplo de execução funcionando

## Prioridades (ordem)
1) Cache da GitHub API para reduzir rate-limit e acelerar re-runs
2) CLI profissional (subcomandos, help, exemplos)
3) CI (GitHub Actions: lint + tests)
4) Docs/README + demo visual
