# Matriz de lacunas e plano de prontidão open source — Conselho Central

**Snapshot:** 2026-11-14  
**Escopo:** Conselho Central e sua preparação como projeto open source.  
**Branch de trabalho:** `feat/central-portfolio-registry-20261114` (PR #6, Draft).  
**Regra:** este documento é pesquisa e planejamento. Não autoriza merge, deploy, publicação externa, criação de outro repositório, alteração de licença, custos ou mudanças de permissões.

## 1. Resumo executivo

O Conselho Central já tem uma base estrutural útil: catálogo de skills, roteador, registries, contratos de governança, testes determinísticos e um planner DAG. Isso ainda não equivale a um runtime multiagente operacional.

A oportunidade de diferenciação não é competir por quantidade de agentes. É oferecer um **sistema de engenharia assistida por agentes, governado, verificável, orientado a evidências e adaptável a diferentes clientes**.

A pesquisa externa reforça que os maiores problemas práticos são execução/orquestração, gestão de workflow, integração de ferramentas, memória/estado, depuração, qualidade e recuperação. Portanto, a evolução deve priorizar confiabilidade mensurável antes de ampliar a escala.

## 2. Evidências do nosso estado

### Estado observado no PR #6

- Repositório público: `japaprp/japaprp`.
- PR #6 aberto, Draft, não merged; HEAD observado: `b7bbfc93278ef845c0db655b4a4d532d824f7551`.
- Run #107, ID `43561502396`, concluído com `success`; 16 etapas nomeadas concluídas com sucesso.
- 37 skills, 13 famílias de capacidades, 19 projetos, 17 registros de repositórios e 50 casos de roteamento, conforme os artefatos/validações atuais do PR.
- Planner DAG valida projeto único, dependências, ciclos, IDs, concorrência e locks de recursos. Padrão 5; teto implementado 10.
- O planner seleciona tarefas elegíveis; **não despacha agentes-filhos nem executa ferramentas**.
- A/B/C e D1–D3 em sessão real continuam NOT RUN até validação no cliente/runtime alvo.
- O README da raiz na branch consultada descreve o perfil pessoal/portfólio do mantenedor; `skills/README.md` é o catálogo interno de skills.

### Lacunas de apresentação e colaboração observadas

Nos caminhos convencionais consultados na branch, não foram localizados: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `package.json`, `pyproject.toml`, nem templates comuns de issue em `.github/ISSUE_TEMPLATE/`. Isso não prova que não exista outra forma de distribuição, mas mostra que o projeto ainda não oferece uma experiência padrão de instalação/contribuição como framework ou pacote.

**Implicação de licença:** sem uma licença open source explícita, o público pode visualizar o código, mas não recebe automaticamente permissão ampla para reutilizá-lo, modificá-lo e redistribuí-lo. A escolha da licença é decisão do mantenedor e fica BLOCKED até decisão explícita.

## 3. Pesquisa externa — padrões recorrentes

### Estudos empíricos e levantamentos

1. **Understanding Issues, Causes and Solutions in Open-Source LLM-based Multi-Agent Systems** (2026-10-01): analisou 22.848 issues encerradas em 21 projetos e filtrou 944 issues relacionadas a sistemas multiagente. O problema mais frequente foi orchestration/execution; workflow, integração de ferramentas e memória foram causas recorrentes; otimização de workflow foi a solução predominante.  
   https://arxiv.org/abs/2610.00905

2. **A Large-Scale Study on the Development and Issues of Multi-Agent AI Systems** (2026-01-12): estudou mais de 42 mil commits e 4,7 mil issues resolvidas em oito sistemas. As categorias mais frequentes incluíram bugs, infraestrutura e coordenação entre agentes; o estudo aponta importância de testes, documentação e manutenção.  
   https://arxiv.org/abs/2601.07136

3. **LangChain — State of Agent Engineering (2026)**: pesquisa com mais de 1.300 profissionais. O relatório aponta qualidade como barreira de produção, ampla adoção de observabilidade e adoção ainda menor de avaliações sistemáticas.  
   https://www.langchain.com/state-of-agent-engineering

4. **Temporal — State of Development 2026**: pesquisa com engenheiros e líderes. Rastreamento de estado, depuração e custo aparecem entre os principais bloqueios; segurança é preocupação relevante para agentes mais autônomos.  
   https://temporal.io/reports/state-of-development-2026

5. **Relatos comunitários (Reddit)**: relatos de produção destacam handoffs estruturados, validação entre etapas, checkpoints, custos, latência, contexto compartilhado e pontos de aprovação humana. São relatos individuais, não estatísticas representativas.  
   https://www.reddit.com/r/aiagents/comments/1rpq0cy/lessons_from_running_a_12_agent_coordination/  
   https://www.reddit.com/r/AI_Agents/comments/1t09uei/lessons_learned_building_agents_in_production/  
   https://www.reddit.com/r/aiagents/comments/1tunuvc/anyone_actually_using_multiagent_ai_in_production/

### Projetos de referência para estudar mecanismos, não copiar arquiteturas inteiras

| Projeto | Mecanismo de referência | O que estudar |
|---|---|---|
| OpenHands | Ambiente real de execução de tarefas de engenharia | Isolamento, ferramentas, experiência de desenvolvedor e verificação |
| LangGraph | Workflows com estado e checkpoints | Estado, retomada e controle explícito |
| OpenAI Agents SDK | Handoffs, guardrails e ferramentas | Delegação e fronteiras de responsabilidade |
| AgentCompass | Avaliação que separa modelo, benchmark, harness e ambiente | Reprodutibilidade, persistência de resultados, traces e execução isolada |
| Open Multi-Agent | Checkpoints, approvals duráveis, run records e leases | Recuperação, idempotência, auditoria e concorrência |
| MAS Lab | Especificação de agentes/workflows com observabilidade e governança | Separação entre intenção, execução, telemetria e política |
| OpenWOP | Protocolo de workflows duráveis e interoperáveis | Pausa/retomada, replay, idempotência e aprovação humana |
| A2A + MCP | Protocolos complementares | A2A para agente-agente; MCP para agente-ferramenta |

Links:
- https://github.com/All-Hands-AI/OpenHands
- https://github.com/langchain-ai/langgraph
- https://github.com/openai/openai-agents-python
- https://github.com/open-compass/AgentCompass
- https://github.com/open-multi-agent/open-multi-agent
- https://github.com/ioc-project/mas-lab
- https://github.com/openwop/openwop
- https://a2a-protocol.org/

**Decisão arquitetural:** não substituir o Conselho Central por um framework de terceiros apenas por popularidade. Reutilizar componentes ou protocolos somente quando resolverem uma lacuna comprovada, forem compatíveis com o runtime e tiverem custo/risco aceitáveis.

## 4. Matriz de lacunas técnicas

| Prioridade | Capacidade | Estado atual | Trabalho necessário | Critério verificável de aceite |
|---|---|---|---|---|
| P0 | Dispatch real de agentes-filhos | NOT RUN | Identificar runtime/adaptador disponível no Codex/VS Code; provar dispatch | Dois agentes reais, IDs distintos, execução independente observável |
| P0 | QA independente | Parcial no contrato | Verificador separado do executor, critérios de aceite e rejeição | QA encontra defeito plantado e impede status DONE |
| P0 | Fresh-session activation A/B/C | NOT RUN | Executar sessão realmente nova no cliente-alvo | Instruções carregadas, roteamento e limites comprovados com traces |
| P1 | Estado persistente | Não comprovado | Modelo persistente de workflow e tarefas | Retomar após reinício sem perder estado nem duplicar ações |
| P1 | Idempotência e receipts | Contrato parcial | IDs de operação, deduplicação e recibos de ações externas | Retry não repete mutação já confirmada |
| P1 | Cancelamento e recovery | Não comprovado | Cancelamento cooperativo, timeout, retry limitado e recuperação | Testes de interrupção, retomada e cancelamento com evidências |
| P1 | Observabilidade | Telemetria descrita, runtime não comprovado | Trace por workflow/tarefa/agente, logs estruturados e custos quando disponíveis | Reconstruir uma execução completa e localizar uma falha injetada |
| P1 | Task Proof System | Status global já existe | Evidência obrigatória por critério de aceite; separar alegação de prova | Tarefa não fica DONE sem artefato/teste/receipt verificável |
| P1 | Segurança e isolamento | Regras documentadas | Permissões mínimas, isolamento de projeto, redaction e threat model | Testes negativos de vazamento, acesso indevido e ação sem aprovação |
| P2 | Benchmark comportamental | 50 casos de roteamento estrutural | Dataset de tarefas reais, rubricas e resultados versionados | Baseline reproduzível por cliente/modelo/versão |
| P2 | Orçamento e admission control | Teto de concorrência no planner | Limites por workflow e tarefa, timeout e budget stop | Teste prova parada ao atingir limite |
| P2 | Adaptadores de cliente | AGENTS.md e Copilot instructions | Matriz Codex, VS Code/Copilot e demais clientes suportados | Testes por cliente; nenhuma alegação de suporte sem execução |
| P3 | Interoperabilidade | Ainda não implementada | Avaliar MCP e A2A após estabilizar contratos internos | Um exemplo funcional, seguro e reproduzível com outro agente/tool host |

## 5. Matriz de prontidão open source

| Área | Estado observado | Próxima entrega |
|---|---|---|
| Identidade do produto | Nome/conceito existe, mas raiz apresenta perfil pessoal | Definir identidade e promessa pública do Conselho Central |
| Repositório de produto | Código está em `japaprp/japaprp`, repositório de perfil do usuário | Avaliar repositório dedicado; não criar/migrar sem aprovação |
| README público | README raiz é perfil/portfólio | Landing README com problema, proposta, estado real, demo e quickstart |
| Instalação | Não há manifesto padrão de pacote identificado | Escolher distribuição após definir formato e clientes suportados |
| Demo | Não há demo pública reproduzível identificada nesta auditoria | Demo local read-only, sem credenciais e com saída esperada |
| Licença | LICENSE não localizada na raiz da branch | BLOCKED — decisão explícita do mantenedor |
| Contribuição | CONTRIBUTING não localizado nos caminhos padrão | Guia de setup, testes, escopo e PR |
| Código de conduta | CODE_OF_CONDUCT não localizado nos caminhos padrão | Adotar política simples e aplicável |
| Segurança | SECURITY não localizada nos caminhos padrão | Política de divulgação responsável e contato de segurança |
| Issues/PRs | Templates comuns não localizados | Bug report, feature request, questionário de runtime e PR template |
| Releases | Processo de release/tag não comprovado | Changelog, versionamento semântico e notas de release |
| Compatibilidade | Clientes-alvo descritos, mas não testados de ponta a ponta | Matriz de versões e status por cliente |
| Testes | CI estrutural forte para o catálogo/planner | Acrescentar testes comportamentais e de integração conforme runtime |
| Documentação | Catálogo interno existe | Quickstart, arquitetura, exemplos, FAQ e troubleshooting |
| Governança | Gates de autorização documentados | Publicar modelo de ameaças, permissões e limites |
| Manutenção | Mantenedor individual | Roadmap público, issue triage e política de suporte realista |

### Recomendação sobre estrutura do GitHub

O repositório atual `japaprp/japaprp` usa o padrão especial de repositório de perfil do GitHub e sua raiz já contém a apresentação pessoal. A opção mais clara para adoção de terceiros é manter esse repositório como perfil e, depois de aprovada a estratégia, publicar o Conselho Central em um **repositório de produto dedicado**. Isso evita transformar o perfil em uma página de produto e permite README, releases, issues, licença, documentação e métricas próprias.

Não criar, transferir, duplicar ou publicar outro repositório nesta etapa.

## 6. Plano de execução recomendado

### Fase 0 — Fechar evidências internas (antes de promover publicamente)

1. Executar A/B/C em sessão nova no cliente-alvo.
2. Executar D1–D3 com dispatch real; se o runtime não oferecer subagentes observáveis, registrar BLOCKED e escolher um adaptador compatível em vez de simular.
3. Validar QA independente, locks, cancelamento, recuperação e gates de autorização.
4. Atualizar ENGINE_STATUS e PR description com o HEAD e run corretos.
5. Fazer revisão completa do diff e de todas as claims públicas.

**Gate:** não anunciar runtime multiagente operacional enquanto dispatch e recuperação não forem demonstrados.

### Fase 1 — Definir o produto distribuível

1. Definir público inicial: desenvolvedores que usam Codex/VS Code e clientes compatíveis.
2. Definir escopo do produto: pacote de skills/roteamento/governança, runtime ou ambos. Não misturar contrato implementado com runtime futuro.
3. Escolher estrutura de repositório de produto e estratégia de distribuição.
4. Decidir licença explicitamente.
5. Criar README, quickstart, demo, compatibilidade e FAQ.

**Gate:** uma pessoa sem contexto prévio deve conseguir entender o produto e executar a demo seguindo apenas a documentação.

### Fase 2 — Saúde da comunidade

1. Adicionar CONTRIBUTING, CODE_OF_CONDUCT, SECURITY e templates de issues/PR.
2. Definir política de suporte e triagem que o mantenedor consiga cumprir.
3. Criar roadmap público com issues pequenas e reproduzíveis.
4. Publicar changelog e releases versionadas.
5. Criar exemplos seguros e testes de instalação/upgrade.

**Gate:** um colaborador externo consegue reproduzir os testes, abrir issue útil e enviar PR sem orientação privada.

### Fase 3 — Distribuição e adoção

1. Escolher canal de distribuição adequado ao artefato real (release ZIP/GitHub, template, CLI ou package registry).
2. Só publicar pacote npm/PyPI quando houver interface estável, testes de instalação e manutenção definida.
3. Preparar exemplos e tutorial curto em português e inglês.
4. Divulgar em comunidades relevantes com transparência e sem pedir estrelas artificiais.
5. Coletar feedback e priorizar problemas reais de onboarding e confiabilidade.

**Gate:** instalação, uso e atualização reproduzíveis; versão e documentação consistentes.

## 7. Métricas de adoção e qualidade

Não usar estrelas como única métrica. Acompanhar mensalmente:

- Descoberta: visualizações, visitantes únicos, fontes de referência e páginas populares.
- Intenção de uso: clones totais e únicos, downloads por release/pacote, quickstarts iniciados.
- Adoção: instalações verificadas quando tecnicamente mensuráveis, exemplos executados e usuários recorrentes quando houver telemetria consentida.
- Comunidade: stars, forks, issues úteis, contribuidores externos, PRs aceitos e tempo de resposta.
- Qualidade: taxa de sucesso do quickstart, regressões, falhas por cliente, tarefas concluídas com evidência, recovery e segurança.
- Sustentabilidade: releases no prazo, backlog, tempo de manutenção e custo operacional.

GitHub Traffic fornece uma janela móvel de 14 dias para visitantes, visualizações, clones, fontes e conteúdo popular; é necessário registrar snapshots periódicos para análise histórica. Stars indicam interesse, não equivalem a downloads nem a usuários ativos.

## 8. Estratégia legítima de descoberta

- Descrição curta, tópicos corretos, README orientado ao usuário e releases reais.
- Demo reproduzível e screenshots/diagramas que expliquem a arquitetura.
- Artigos técnicos com benchmarks e limitações publicados junto das versões.
- Exemplos práticos e issues `good first issue` somente quando forem realmente acessíveis.
- Participação útil em fóruns, Reddit, Discord e comunidades de agentes, respondendo problemas concretos.
- Pedir feedback honesto; nunca comprar estrelas, usar contas artificiais ou prometer capacidades não comprovadas.

O GitHub informa que stars participam de descoberta e rankings, mas Trending considera sinais de atividade recente como stars, forks, commits, follows e pageviews; não há fórmula pública completa nem posição garantida. Downloads dependem do canal de distribuição e devem ser medidos separadamente.

## 9. Decisões pendentes do mantenedor

| Decisão | Recomendação técnica | Estado |
|---|---|---|
| Repositório dedicado ao produto | Sim; manter perfil pessoal separado | Aguardando decisão/escopo |
| Licença | MIT para simplicidade ou Apache-2.0 para concessão explícita de patentes; avaliar dependências | BLOCKED — decisão do mantenedor |
| Nome/descrição pública | Conselho Central — Governed Agent Engineering Toolkit (provisório) | A validar |
| Idiomas | README e quickstart em inglês e português | Planejado |
| Distribuição inicial | GitHub Release/template reproduzível antes de pacote | Planejado |
| Telemetria de produto | Opt-in, mínima e documentada; sem coleta oculta | Obrigatório antes de implementar |

## 10. Fontes de referência

### Pesquisa e comunidade
- https://arxiv.org/abs/2610.00905
- https://arxiv.org/abs/2601.07136
- https://www.langchain.com/state-of-agent-engineering
- https://temporal.io/reports/state-of-development-2026
- https://www.reddit.com/r/aiagents/comments/1rpq0cy/lessons_from_running_a_12_agent_coordination/
- https://www.reddit.com/r/AI_Agents/comments/1t09uei/lessons_learned_building_agents_in_production/
- https://www.reddit.com/r/aiagents/comments/1tunuvc/anyone_actually_using_multiagent_ai_in_production/

### Projetos e protocolos
- https://github.com/All-Hands-AI/OpenHands
- https://github.com/langchain-ai/langgraph
- https://github.com/openai/openai-agents-python
- https://github.com/open-compass/AgentCompass
- https://github.com/open-multi-agent/open-multi-agent
- https://github.com/ioc-project/mas-lab
- https://github.com/openwop/openwop
- https://a2a-protocol.org/

### Boas práticas oficiais do GitHub
- README: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- Boas práticas de repositório: https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories
- Contribuição: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors
- Segurança: https://docs.github.com/en/code-security/getting-started/securing-your-repository
- Tráfego: https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository
- Métricas open source: https://opensource.guide/metrics/

---

**Conclusão:** o Conselho Central tem uma fundação de catálogo, roteamento e governança. Para se tornar um projeto open source respeitado, precisa provar o runtime, oferecer uma experiência de instalação/demo simples, adotar licença e políticas de colaboração explícitas e medir adoção e qualidade separadamente. O caminho recomendado é confiabilidade primeiro, produto distribuível em seguida, divulgação depois.
