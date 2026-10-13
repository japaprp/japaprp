# Yago's Agent Skills

Catálogo enxuto de skills autorais para Codex, VS Code e agentes compatíveis com `SKILL.md`. O objetivo é qualidade de engenharia com pouco contexto, ferramentas bem escolhidas e mudanças seguras — não acumular skills.

## Comece pelo cérebro

- [engineering-brain-router](./engineering-brain-router/SKILL.md) — roteia a tarefa para o menor conjunto de skills necessário; use como ponto de entrada quando a tarefa não for óbvia.
- [Princípios comuns](#princípios-comuns) — regras transversais de segurança, evidência e entrega.

## Catálogo por tarefa

| Necessidade | Skill principal | Complementar somente quando necessário |
|---|---|---|
| Entender repositório, arquitetura e fluxo | [repo-reverse-engineering](./repo-reverse-engineering/SKILL.md) | debug ou segurança se a investigação exigir |
| Bug, crash, lentidão, regressão | [targeted-debugging-performance](./targeted-debugging-performance/SKILL.md) | [testing-regression-quality](./testing-regression-quality/SKILL.md) |
| Testes e qualidade de release | [testing-regression-quality](./testing-regression-quality/SKILL.md) | segurança ou infraestrutura conforme o risco |
| Login, autorização, sessão, isolamento de dados | [application-security-auth](./application-security-auth/SKILL.md) | CRUD/testes quando necessário |
| Infra, banco, migração, deploy, rollback e custo | [infrastructure-database-engineering](./infrastructure-database-engineering/SKILL.md) | segurança ou testes conforme o risco |
| Formulários, cadastro, CRUD e integridade | [forms-crud-data-integrity](./forms-crud-data-integrity/SKILL.md) | segurança se houver dados privados ou permissões |
| UI nova, redesign e auditoria de UX/acessibilidade | [premium-distinctive-web-design](./premium-distinctive-web-design/SKILL.md) | [vercel-react-performance](./vercel-react-performance/SKILL.md) apenas para React/Next.js com necessidade real |
| Performance React/Next.js | [vercel-react-performance](./vercel-react-performance/SKILL.md) | debug/testes se a tarefa exigir |
| Supabase/PostgreSQL/RLS | [supabase-postgres-specialist](./supabase-postgres-specialist/SKILL.md) | segurança/testes quando necessário |
| Vídeo programático Remotion | [remotion-video-engineering](./remotion-video-engineering/SKILL.md) | pipeline de render se aplicável |
| Composição/pipeline HyperFrames | [hyperframes-video-pipeline](./hyperframes-video-pipeline/SKILL.md) | debug se necessário |
| Análise assistida com REA | [rea-assisted-analysis](./rea-assisted-analysis/SKILL.md) | engenharia reversa se necessário |
| Economia de contexto/créditos de IA | [ai-token-budget](./ai-token-budget/SKILL.md) | roteador para reduzir leitura redundante |

## Regras de composição

1. Use uma skill principal e no máximo duas complementares, salvo motivo técnico explícito.
2. Não carregue várias skills que cobrem o mesmo comportamento. A direção de arte e a auditoria geral de UI estão consolidadas em `premium-distinctive-web-design`; React/Next performance continua separada por ser específica da stack.
3. `supabase-postgres-specialist` é específica de Supabase/PostgreSQL. Não aplicar diretamente comandos ou sintaxe ao MySQL; adaptar apenas princípios portáveis.
4. Consulte referências públicas para aprofundar quando houver necessidade; não copie conteúdo inteiro nem crie skill nova apenas por popularidade.
5. Prefira instruções curtas e de alta prioridade em `SKILL.md`; materiais longos e exemplos devem ser carregados sob demanda.
6. As skills não instalam extensões, não ativam MCPs e não concedem acesso automaticamente. Use somente ferramentas realmente disponíveis no ambiente e confirme a execução antes de relatar sucesso.

## Princípios comuns

1. Ler as instruções locais relevantes e identificar a stack real antes de agir.
2. Usar logs, diff, símbolos e testes focados antes de abrir grandes quantidades de arquivos.
3. Separar fatos observados, inferências e hipóteses.
4. Não expor segredos, tokens, cookies, chaves, dados pessoais nem valores sensíveis de configuração.
5. Definir escopo e critério de aceitação; preservar alterações existentes e contratos do sistema.
6. Fazer a menor mudança que resolva a causa real; não reescrever módulos sem evidência.
7. Rodar verificações proporcionais ao risco e relatar exatamente o que foi executado, o resultado e as limitações.
8. Não executar operações destrutivas, alterar produção, fazer deploy ou publicar alterações fora do escopo autorizado.
9. Não alegar instalação, teste, renderização, inspeção visual, medição de tokens ou deploy sem evidência.
10. Em engenharia reversa, analisar apenas software próprio ou autorizado; não contornar controles nem coletar dados de terceiros.

## Referências públicas selecionadas

As skills locais são guias autorais adaptados para os projetos e o fluxo de trabalho do usuário; as fontes abaixo são referências para consulta, não duplicatas a carregar por padrão.

- [OpenAI Codex — boas práticas](https://developers.openai.com/codex/learn/best-practices) — contexto, instruções persistentes, ferramentas e fluxos reutilizáveis.
- [Anthropic Skills](https://github.com/anthropics/skills) — frontend-design e autoria de skills.
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) — React/Next.js e diretrizes de interface.
- [obra/superpowers](https://github.com/obra/superpowers) — depuração sistemática e desenvolvimento guiado por testes.
- [Supabase Agent Skills](https://github.com/supabase/agent-skills) — PostgreSQL, RLS e práticas específicas do Supabase.
- [Agent Skills format](https://github.com/Open-Dot-Agents/SKILL.md) — estrutura interoperável de skills.

## Uso

Para uma tarefa clara, invoque diretamente a skill principal. Para tarefa ampla ou ambígua, comece com `engineering-brain-router`. Exemplos:

- “Use `repo-reverse-engineering` para mapear o fluxo de login sem editar arquivos.”
- “Use `targeted-debugging-performance` para encontrar a causa raiz e `testing-regression-quality` apenas para validar a correção.”
- “Use `premium-distinctive-web-design` para redesenhar esta tela sem quebrar acessibilidade ou fluxos existentes.”

O catálogo é uma camada de método. Cada repositório ainda precisa de contexto e comandos reais; não assuma que toda skill se aplica a toda stack.
