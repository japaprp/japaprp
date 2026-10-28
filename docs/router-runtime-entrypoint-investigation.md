# Investigação do entrypoint real do Engineering Brain Router

Data: 2026-10-28  
Branch investigada: `chore/content-skills-consolidation`  
Commit-base da inspeção: `7a2f0e3e4b0683481c4f59cf5999372ba1b91c3b`

## Resultado

**Estado: BLOCKED — runtime consumidor externo não identificado neste repositório.**

A inspeção recursiva da árvore do repositório encontrou skills declarativas em Markdown, scripts de validação e um harness de avaliação manual. Não encontrou um entrypoint executável de agente (por exemplo, aplicação/orquestrador que carregue `SKILL.md` e faça dispatch de tarefas) nem configuração que demonstre que o runtime de produção importa `engineering-brain-router`.

Evidências observadas:
- `skills/README.md` descreve o catálogo como destinado a Codex, VS Code e agentes compatíveis com `SKILL.md`, e recomenda o router como ponto de entrada.
- `skills/engineering-brain-router/SKILL.md` é uma especificação de roteamento em Markdown, não um dispatcher executável.
- `scripts/run_router_eval.py` declara explicitamente que não chama um modelo; recolhe manualmente respostas do agente-alvo.
- `skills/tests/LOCAL_MANUAL_EVAL.md` orienta a execução manual no Codex / VS Code, com o catálogo configurado no workspace e observação do trace/contexto real.
- A árvore inspecionada contém `scripts/validate_skills.py` e workflows de validação; estes verificam artefatos do catálogo, não provam carregamento pelo runtime.

## Decisão técnica

Não adicionar um segundo dispatcher executável neste PR. Isso criaria uma integração especulativa sem saber qual agente/runtime é o consumidor real e poderia duplicar regras ou divergir da configuração efetivamente utilizada.

A integração só pode avançar depois de inspecionar o ambiente-alvo autorizado e observar:
1. qual agente/runtime está em uso (por exemplo, Codex no VS Code);
2. onde o catálogo de skills é instalado/configurado e qual revisão está ativa;
3. qual entrypoint ou mecanismo real carrega/seleciona skills;
4. um trace/contexto ou outro sinal observável mostrando a seleção de `engineering-brain-router`;
5. um caso sintético executado no agente-alvo em que a skill esperada e o comportamento observado coincidam.

## Próximo procedimento de validação

1. No workspace do agente-alvo, confirmar o commit/revisão do catálogo e localizar a configuração de skills ativa.
2. Executar casos selecionados do dataset de avaliação no próprio agente, sem alterar as skills durante a rodada.
3. Capturar evidência não sensível da skill realmente carregada e da resposta real; registrar `not-observable` quando não houver trace.
4. Classificar cada caso como `PASS`, `FAIL`, `BLOCKED` ou `NOT_RUN`; não inferir ativação a partir de CI verde.
5. Só então propor uma integração mínima no entrypoint confirmado, se o runtime oferecer um ponto de extensão real e documentado.

## Limites

Esta investigação foi somente leitura no GitHub. Não acessou o computador local do usuário, não inspecionou configurações locais do Codex/VS Code, não instalou ferramentas, não executou prompts em uma sessão independente e não alterou permissões, segredos, publicação ou deploy. A integração de runtime permanece **NOT RUN/BLOCKED** até obter evidência do ambiente consumidor.
