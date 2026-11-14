---
name: agent-orchestration
description: Planejar e coordenar trabalho paralelo entre agentes especializados por meio de hierarquia, DAG de dependências, limites de concorrência, isolamento, revisão e gates de autorização.
---

# Agent Orchestration — coordenação multiagente governada

## Missão

Transformar um único comando do usuário em um plano rastreável de tarefas independentes, atribuí-las a agentes especializados, permitir execução paralela quando segura e consolidar resultados com evidências. O objetivo é aumentar throughput sem perder coerência, segurança, controle de custos ou responsabilidade.

Esta skill define o contrato de orquestração. Ela não afirma que um pool de agentes está ativo, que o host consegue iniciar agentes-filhos, nem que 100 agentes podem executar simultaneamente. A capacidade real depende do runtime e das ferramentas verificadas.

## 1. Hierarquia operacional

- **Owner / usuário:** define objetivo, prioridade e limites; mantém autoridade final sobre ações reservadas.
- **Diretor-geral / Conselho Central:** interpreta o comando, identifica o projeto, resolve contexto, define sucesso, decompõe o trabalho e consolida a prestação de contas.
- **Diretores funcionais:** tecnologia/arquitetura, operações/produto, qualidade/confiabilidade e governança/segurança. Atuam como coordenadores de domínio, não como aprovadores de ações reservadas do usuário.
- **Gerentes:** transformam objetivos de domínio em entregáveis, dependências e critérios de aceite.
- **Líderes técnicos:** distribuem subtarefas, controlam interfaces, conflitos, bloqueios e integração.
- **Agentes especialistas/executores:** realizam uma tarefa delimitada com ferramentas e permissões mínimas.
- **QA independente:** verifica entregáveis sem depender da autodeclaração do executor.
- **Governança/auditoria:** verifica isolamento, evidências, custo, permissões e gates.

A hierarquia é lógica. Não exige criar um agente separado para cada cargo: um runtime pode combinar papéis quando isso for seguro e eficiente.

## 2. Ciclo de um comando único

1. **Intake:** registrar comando, objetivo, projeto, restrições, prazo se houver e evidência de sucesso.
2. **Context resolution:** identificar exatamente um projeto e carregar apenas contexto/skills pertinentes.
3. **Planning:** decompor o objetivo em tarefas pequenas com task_id, responsável, entradas, saídas, critérios de aceite, risco e dependências.
4. **DAG:** construir grafo acíclico de dependências; tarefas sem dependências entre si podem ser paralelizadas.
5. **Admission control:** verificar ferramentas, permissões, RAM/CPU, limites do host, quotas, custo e concorrência. Se não houver runtime multiagente comprovado, executar somente paralelismo de ferramentas realmente disponível e marcar agentes-filhos como NOT RUN.
6. **Dispatch:** atribuir cada tarefa a um agente compatível, com escopo mínimo, contexto mínimo e instruções explícitas.
7. **Execution:** agentes retornam artefatos, diffs, logs, testes, hipóteses e bloqueios; não podem ampliar o próprio escopo.
8. **Integration:** integrar apenas entregáveis compatíveis; usar locks por arquivo/recurso, branches/worktrees isolados ou serialização para evitar escrita concorrente.
9. **Independent QA:** testar requisitos, regressões, segurança e evidências; reabrir tarefas com falha.
10. **Governance gate:** bloquear ações reservadas sem autorização explícita do Owner.
11. **Synthesis:** apresentar resultado consolidado, evidências, pendências, custo/recursos observados e status PASS/FAIL/BLOCKED/NOT RUN.

## 3. Contrato mínimo de tarefa

Cada tarefa deve carregar:
- task_id estável e parent_task_id;
- project_id, repositório, branch e ambiente verificados;
- objetivo e escopo permitido/proibido;
- assigned_role / skill primária;
- entradas e referências de evidência;
- depends_on e recursos/arquivos que serão tocados;
- risco, permissões e teto de custo;
- critério de aceite e verificação independente;
- estado PENDING, READY, RUNNING, BLOCKED, FAILED ou DONE;
- saída, evidência, commit/diff quando aplicável e agente responsável.

Não inclua segredos ou dados pessoais desnecessários no contexto compartilhado.

## 4. Paralelismo e escala

- Comece com 1 coordenador e 2–5 executores em tarefas independentes.
- Suba para 5–10 somente após medir qualidade, latência, conflitos e consumo.
- 20–30 é uma escala avançada, condicionada a filas, observabilidade e limites comprovados.
- 100+ é capacidade máxima aspiracional, nunca concorrência padrão. Exige particionamento forte, orçamento, rate limits, quotas, cancelamento, supervisão e testes de carga.
- Não crie agentes só para preencher cargos. Prefira o menor número que reduz tempo sem aumentar risco.
- O número de agentes é limitado pelo menor teto entre runtime, ferramentas, quotas, recursos e orçamento.

## 5. Regras de concorrência e integração

- Paralelize pesquisa, leitura, testes independentes e mudanças em arquivos/áreas isoladas.
- Serialize mudanças no mesmo arquivo, schema, contrato público, banco, configuração compartilhada ou recurso mutável.
- Um agente não pode editar o mesmo worktree/arquivo que outro sem lock e protocolo de integração.
- Agentes não podem rebasear, descartar, sobrescrever ou incorporar mudanças alheias sem revisão.
- Use branch/worktree por tarefa de código quando o runtime suportar; caso contrário, atribua ownership exclusivo por arquivo.
- Após cada lote, rode integração e testes focados antes de liberar dependentes.
- Em falha, preserve evidências, pare dependentes, replaneje e não esconda resultados parciais.

## 6. Autonomia por classe de risco

**Permitido dentro do escopo:** leitura, busca, análise, planejamento, execução de testes locais seguros, documentação e alterações isoladas em branches autorizadas.

**Exige aprovação explícita do Owner:** merge, deploy, publicação externa, exclusão, migração destrutiva, alteração de segredos/permissões, mudança de DNS/produção, instalação global ou paga, criação de custos, compra ou envio de comunicações externas.

O comando operacional “DEUS É FIEL” inicia o fluxo de identificação, planejamento e execução segura; não concede novas permissões nem remove os gates acima.

## 7. Resolução de conflito

Prioridade: segurança e isolamento > instrução explícita do Owner > fonte autoritativa do projeto > contrato/arquitetura > critério de aceite > preferência de implementação.

Se dois agentes discordarem:
1. preserve as duas evidências;
2. identifique se a divergência é factual, arquitetural ou de preferência;
3. peça verificação independente para fatos;
4. aplique o menor desenho compatível com requisitos e segurança;
5. escale ao Owner somente quando houver decisão irreversível, ambiguidade material ou conflito de autoridade.

## 8. Relatório final obrigatório

Para cada frente: responsável/papel, resultado, evidência, testes, recursos/custo conhecido, status e próximo bloqueio. O relatório global deve distinguir:
- **PASS:** critério verificado;
- **FAIL:** critério executado e reprovado;
- **BLOCKED:** impedimento externo ou de autorização;
- **NOT RUN:** não executado, sem inferir sucesso.

Nunca transformar cobertura estrutural em prova de comportamento multiagente real.
