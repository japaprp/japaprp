# Yago's Agent Skills

Skills autorais para usar com agentes de programação no VS Code, Codex e ferramentas compatíveis com o formato `SKILL.md`.

## Organização

- [repo-reverse-engineering](./repo-reverse-engineering/SKILL.md) — investigar um repositório com evidências, mapa arquitetural, fluxos e testes.
- [remotion-video-engineering](./remotion-video-engineering/SKILL.md) — estudar, desenvolver e depurar projetos de vídeo programático com Remotion.
- [hyperframes-video-pipeline](./hyperframes-video-pipeline/SKILL.md) — criar e diagnosticar composições HTML/CSS/JS e pipelines de renderização com HyperFrames.
- [rea-assisted-analysis](./rea-assisted-analysis/SKILL.md) — conduzir análises autorizadas com REA, documentando evidências e limites.

- [infrastructure-database-engineering](./infrastructure-database-engineering/SKILL.md) — infraestrutura, banco, migrações, deploy e custos.
- [application-security-auth](./application-security-auth/SKILL.md) — autenticação, autorização, cadastro seguro, isolamento multi-tenant e vulnerabilidades.
- [testing-regression-quality](./testing-regression-quality/SKILL.md) — testes unitários, integração, E2E, acessibilidade e regressão.
- [targeted-debugging-performance](./targeted-debugging-performance/SKILL.md) — bugs, travamentos, lentidão e diagnóstico por evidência sem ler tudo.
- [ai-token-budget](./ai-token-budget/SKILL.md) — economia de tokens/créditos e regras para medidor honesto de uso.
- [premium-distinctive-web-design](./premium-distinctive-web-design/SKILL.md) — direção de arte premium e interfaces sem aparência genérica de IA.
- [forms-crud-data-integrity](./forms-crud-data-integrity/SKILL.md) — cadastros, CRUD, validação, duplicidade e integridade dos dados.

## Princípios comuns

1. Ler primeiro as instruções do repositório (`README`, `AGENTS.md`, arquivos de contribuição e configuração do agente).
2. Mapear o código antes de editar; nunca presumir que nomes de arquivos provam comportamento.
3. Separar fatos observados, inferências e hipóteses.
4. Não expor, copiar ou registrar segredos: `.env`, tokens, chaves, cookies, dados pessoais e credenciais.
5. Antes de editar, definir escopo e critérios de aceitação; preservar alterações existentes do usuário.
6. Rodar os testes e verificações adequados e relatar exatamente o que foi executado, o que passou e o que não pôde ser validado.
7. Não alegar que algo foi instalado, executado, renderizado ou implantado sem evidência de execução.
8. Para engenharia reversa, analisar somente software próprio ou para o qual exista autorização; não contornar controles de acesso nem coletar dados alheios.

## Uso

Abra a skill relevante e peça ao agente uma tarefa concreta, por exemplo:

- “Use repo-reverse-engineering para mapear o fluxo de login deste projeto sem editar arquivos.”
- “Use remotion-video-engineering para investigar por que esta composição renderiza quadros diferentes.”
- “Use hyperframes-video-pipeline para diagnosticar áudio fora de sincronia e produzir um relatório.”
- “Use rea-assisted-analysis para investigar, com autorização, como esta funcionalidade se comporta e registrar as evidências.”

Estas skills são guias de trabalho. Elas não instalam ferramentas automaticamente; confira os requisitos do projeto antes de executar comandos.
