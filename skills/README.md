# Yago's Agent Skills

Catálogo enxuto de skills autorais para Codex, VS Code e agentes compatíveis com `SKILL.md`. O objetivo é qualidade de engenharia com pouco contexto, ferramentas bem escolhidas e mudanças seguras — não acumular skills.

## Comece pelo cérebro

- [engineering-brain-router](./engineering-brain-router/SKILL.md) — roteia a tarefa para o menor conjunto de skills necessário; use como ponto de entrada quando a tarefa não for óbvia.
- [skill-onboarding-profiler](./skill-onboarding-profiler/SKILL.md) — entrevista iniciantes para identificar área, objetivo, stack e nível; recomenda skills e explica como começar.
- [Guia para iniciantes e compartilhamento](./GUIA-PARA-AMIGOS.md) — explicação simples de todas as skills, exemplos de uso e cuidados ao compartilhar o pacote.
- [Princípios comuns](#princípios-comuns) — regras transversais de segurança, evidência e entrega.

## Catálogo por tarefa

| Necessidade | Skill principal | Complementar somente quando necessário |
|---|---|---|
| Não sei qual skill ou tecnologia usar; preciso explicar meu trabalho | [skill-onboarding-profiler](./skill-onboarding-profiler/SKILL.md) | [engineering-brain-router](./engineering-brain-router/SKILL.md) |
|---|---|---|
| Entender repositório, arquitetura e fluxo | [repo-reverse-engineering](./repo-reverse-engineering/SKILL.md) | debug ou segurança se a investigação exigir |
| Bug, crash, lentidão, regressão | [targeted-debugging-performance](./targeted-debugging-performance/SKILL.md) | [testing-regression-quality](./testing-regression-quality/SKILL.md) |
| Testes e qualidade de release | [testing-regression-quality](./testing-regression-quality/SKILL.md) | segurança ou infraestrutura conforme o risco |
| Revisão de diff/PR e correção cirúrgica | [code-review-minimal-change](./code-review-minimal-change/SKILL.md) | testes, segurança ou infraestrutura conforme os achados |
| Design, versionamento e testes de APIs/webhooks | [api-engineering-contracts](./api-engineering-contracts/SKILL.md) | segurança, CRUD ou testes conforme o fluxo |
| Aplicativos móveis, especialmente Flutter/Dart | [mobile-flutter-engineering](./mobile-flutter-engineering/SKILL.md) | API, segurança ou testes conforme o fluxo |
| Integração de modelos e APIs de IA, prompts e RAG | [ai-integration-evaluation](./ai-integration-evaluation/SKILL.md) | API, segurança ou ai-token-budget conforme a necessidade |
| Descoberta de produto, MVP, critérios de aceitação e lançamento | [product-discovery-delivery](./product-discovery-delivery/SKILL.md) | design, API, testes ou infraestrutura conforme o risco |
| Pagamentos, reembolsos, cashback e webhooks financeiros | [payments-billing-integrations](./payments-billing-integrations/SKILL.md) | API, segurança e testes conforme o fluxo |
| Ferramentas MCP e integrações para agentes | [mcp-tooling-engineering](./mcp-tooling-engineering/SKILL.md) | API, segurança e testes conforme o fluxo |
| Conteúdo curto, afiliados e distribuição entre plataformas | [content-commerce-distribution](./content-commerce-distribution/SKILL.md) | vídeo/pipeline ou produto conforme o objetivo |
| Login, autorização, sessão, isolamento de dados | [application-security-auth](./application-security-auth/SKILL.md) | CRUD/testes quando necessário |
| Infra, banco, migração, deploy, rollback e custo | [infrastructure-database-engineering](./infrastructure-database-engineering/SKILL.md) | segurança ou testes conforme o risco |
| Formulários, cadastro, CRUD e integridade | [forms-crud-data-integrity](./forms-crud-data-integrity/SKILL.md) | segurança se houver dados privados ou permissões |
| UI nova, redesign e auditoria de UX/acessibilidade | [premium-distinctive-web-design](./premium-distinctive-web-design/SKILL.md) | [vercel-react-performance](./vercel-react-performance/SKILL.md) apenas para React/Next.js com necessidade real |
| Performance React/Next.js | [vercel-react-performance](./vercel-react-performance/SKILL.md) | debug/testes se a tarefa exigir |
| Supabase/PostgreSQL/RLS | [supabase-postgres-specialist](./supabase-postgres-specialist/SKILL.md) | segurança/testes quando necessário |
| Vídeo programático Remotion | [remotion-video-engineering](./remotion-video-engineering/SKILL.md) | pipeline de render se aplicável |
| Composição/pipeline HyperFrames | [hyperframes-video-pipeline](./hyperframes-video-pipeline/SKILL.md) | debug se necessário |
| Análise assistida com REA | [rea-assisted-analysis](./rea-assisted-analysis/SKILL.md) | engenharia reversa se necessário |
| Gmail/Drive/Calendar ou extração via Actors | [external-workspace-data-tools](./external-workspace-data-tools/SKILL.md) | roteador e segurança conforme o risco |
| Economia de contexto/créditos de IA | [ai-token-budget](./ai-token-budget/SKILL.md) | roteador para reduzir leitura redundante |

## Validação do roteador

- [Router smoke tests](./tests/ROUTER_EVALS.md) — cenários baseados em stacks e problemas reais para revisar seleção de skills, economia de contexto e limites de segurança. São casos esperados; só conte como benchmark depois de executá-los no agente-alvo e registrar os resultados.

## Memória por projeto

- [Template Project Passport](./templates/PROJECT_CONTEXT.md) — modelo curto para registrar stack, comandos comprovados, arquitetura, integrações, riscos, decisões e estado validado de cada projeto. Copie para o repositório correspondente somente quando for útil; não preencha por suposição nem inclua segredos.

## Regras de composição

1. Use uma skill principal e no máximo duas complementares, salvo motivo técnico explícito.
2. Não carregue várias skills que cobrem o mesmo comportamento. A direção de arte e a auditoria geral de UI estão consolidadas em `premium-distinctive-web-design`; React/Next performance continua separada por ser específica da stack.
3. `supabase-postgres-specialist` é específica de Supabase/PostgreSQL. Não aplicar diretamente comandos ou sintaxe ao MySQL; adaptar apenas princípios portáveis.
4. Skills de API, mobile, IA, pagamentos e MCP têm escopos distintos; combine apenas as necessárias para o fluxo real e não presuma provedores, ferramentas, SDKs ou autenticação disponíveis.
4. Consulte referências públicas para aprofundar quando houver necessidade; não copie conteúdo inteiro nem crie skill nova apenas por popularidade.
5. Prefira instruções curtas e de alta prioridade em `SKILL.md`; materiais longos e exemplos devem ser carregados sob demanda.
6. As skills não instalam extensões, não ativam MCPs e não concedem acesso automaticamente. Use somente ferramentas realmente disponíveis no ambiente e confirme a execução antes de relatar sucesso.

## Princípios comuns

As regras transversais de investigação, segurança, edição mínima, autorização e relato de testes têm uma única fonte de verdade: [engineering-brain-router](./engineering-brain-router/SKILL.md). As skills especializadas devem conter apenas procedimentos específicos de seu domínio, evitando repetir o protocolo geral.

## Referências públicas selecionadas

As skills locais são guias autorais adaptados para os projetos e o fluxo de trabalho do usuário; as fontes abaixo são referências para consulta, não duplicatas a carregar por padrão.

- [OpenAI Codex — boas práticas](https://developers.openai.com/codex/learn/best-practices) — contexto, instruções persistentes, ferramentas e fluxos reutilizáveis.
- [Anthropic Skills](https://github.com/anthropics/skills) — frontend-design e autoria de skills.
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) — React/Next.js e diretrizes de interface.
- [Agency Agents](https://github.com/msitarzewski/agency-agents) — catálogo amplo de engenharia, APIs, mobile, IA, segurança, testes, produto, operações e marketing. Auditado seletivamente como matriz de lacunas; incorporar só competências úteis, não instalar todos os perfis.
- [obra/superpowers](https://github.com/obra/superpowers) — depuração sistemática e desenvolvimento guiado por testes.
- [Supabase Agent Skills](https://github.com/supabase/agent-skills) — PostgreSQL, RLS e práticas específicas do Supabase.
- [Agent Skills format](https://github.com/Open-Dot-Agents/SKILL.md) — estrutura interoperável de skills.

## Uso

Para uma tarefa clara, invoque diretamente a skill principal. Para tarefa ampla ou ambígua, comece com `engineering-brain-router`. Exemplos:

- “Use `repo-reverse-engineering` para mapear o fluxo de login sem editar arquivos.”
- “Use `targeted-debugging-performance` para encontrar a causa raiz e `testing-regression-quality` apenas para validar a correção.”
- “Use `premium-distinctive-web-design` para redesenhar esta tela sem quebrar acessibilidade ou fluxos existentes.”

O catálogo é uma camada de método. Cada repositório ainda precisa de contexto e comandos reais; não assuma que toda skill se aplica a toda stack.
