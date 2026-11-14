# Conselho Central — contrato de orquestração multiagente

**Estado:** especificação operacional proposta e validável estruturalmente; runtime multiagente real ainda não comprovado.

## Topologia lógica

Owner → Conselho Central (orquestrador) → Diretores → Gerentes → Líderes → Executores

QA independente e Governança/Auditoria acompanham o fluxo transversalmente. Papéis podem ser combinados por um mesmo agente/runtime; a hierarquia descreve responsabilidade, não exige uma instância por cargo.

## Plano de execução

Um comando gera um plano com:
- objetivo e projeto resolvido;
- tarefas com IDs estáveis;
- dependências DAG;
- skills/ferramentas selecionadas;
- escopo e permissões;
- recursos e limite de concorrência;
- critérios de aceite;
- responsável e verificador independente.

Somente tarefas READY (todas as dependências DONE) entram na fila. Tarefas independentes podem executar em paralelo se passarem admission control. Tarefas com recurso compartilhado exclusivo são serializadas por lock.

## Estados e transições

PENDING → READY → RUNNING → DONE

Saídas alternativas:
- BLOCKED: falta acesso, autorização, contexto ou capacidade;
- FAILED: execução ocorreu e falhou;
- PENDING: dependência ainda não terminou.

Retry exige causa identificada, limite de tentativas e idempotência. Não repetir automaticamente ações externas ou mutações não idempotentes.

## Limites iniciais recomendados

| Perfil | Executores concorrentes | Condição |
|---|---:|---|
| Conservador | 2–5 | padrão inicial |
| Expandido | 5–10 | métricas de qualidade e recursos aprovadas |
| Alto volume | 20–30 | filas, locks, cancelamento, observabilidade e orçamento testados |
| Aspiracional | 100+ | teste de carga, isolamento, quotas e supervisão; nunca padrão |

O helper determinístico scripts/agent-orchestration-planner.mjs valida IDs, dependências, ciclos, projeto único, concorrência e locks exclusivos; ele seleciona tarefas READY, mas não inicia agentes nem executa ferramentas.\n\nO limite efetivo é min(runtime, ferramentas, quotas, recursos, orçamento, política). Se a capacidade do runtime não estiver confirmada, não simular agentes reais: marcar dispatch multiagente como NOT RUN e executar apenas o paralelismo de ferramentas disponível.

## Matriz de autoridade

| Papel | Decide | Não pode autorizar sozinho |
|---|---|---|
| Owner | objetivo, prioridade e ações reservadas | — |
| Conselho Central | decomposição, atribuição, ordem e síntese | merge, deploy, exclusão, segredos, permissões, custos |
| Diretor/gerente/líder | decisões técnicas reversíveis dentro do escopo | ampliar escopo, cruzar projetos ou exceder recursos |
| Executor | implementação delimitada e testes | aprovar o próprio trabalho ou integrar mudanças conflitantes |
| QA | aceitar/reprovar critérios com evidência | dispensar controles de governança |
| Governança | bloquear por risco, isolamento ou falta de autorização | conceder autorização do Owner |

## Locks e isolamento

- Lock por arquivo, schema, contrato, ambiente ou recurso compartilhado.
- Um único writer por recurso mutável, salvo mecanismo transacional comprovado.
- Branch/worktree por unidade de implementação quando disponível.
- Contexto, dados, credenciais e artefatos separados por project_id.
- Nenhuma tarefa herda credenciais ou autorização de outra tarefa.

## Telemetria mínima

Registrar: task_id, parent_task_id, project_id, agent/role, skill, start/end, estado, dependências, arquivos tocados, ferramentas usadas, custo/uso quando disponível, evidências, teste e motivo de bloqueio/falha.

## Critério de ativação

O desenho só pode ser chamado de runtime multiagente operacional após:
1. adapter/runtime identificado e disponível;
2. teste demonstrando dispatch real de pelo menos duas tarefas independentes;
3. prova de isolamento de contexto e escopo;
4. conflito de escrita detectado/prevenido;
5. QA independente e consolidação;
6. bloqueio de ação reservada sem autorização;
7. cancelamento/recovery e observabilidade demonstrados.

Até lá, classificar como **PASS — contrato estrutural** e **NOT RUN — execução real multiagente**.
