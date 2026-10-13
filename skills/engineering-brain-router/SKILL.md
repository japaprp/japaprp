---
name: engineering-brain-router
description: Orquestrar tarefas de engenharia escolhendo o menor conjunto de skills necessário, ferramentas e verificações; use no início de tarefas de programação quando for preciso decidir por onde começar ou como evitar trabalho e contexto redundantes.
---

# Engineering Brain — roteador enxuto

**Missão:** entregar a menor mudança segura que resolve o problema real, com evidência e custo de contexto mínimo. Não é uma enciclopédia: encaminha para a skill especializada e só carrega detalhes quando necessários.

## Protocolo de decisão

1. Reescreva mentalmente o pedido como resultado esperado, restrições e critério verificável de conclusão. Faça pergunta apenas se uma ambiguidade bloquear uma decisão importante.
2. Identifique repositório, branch, estado do trabalho, stack e instruções locais. Comece por `git status`, diff, logs, busca de símbolos e arquivos de entrada; não faça leitura total por padrão.
3. Escolha **uma skill principal** e, no máximo, duas complementares quando houver necessidade concreta. Não leia todas as skills nem copie instruções de uma para outra.
4. Use ferramentas determinísticas para descobrir fatos (busca, testes, lint, typecheck, profiler, logs, SQL EXPLAIN) e o modelo para raciocínio, decisões e mudanças que exigem julgamento.
5. Trace somente o caminho de execução relacionado ao pedido. Separe fato observado, inferência e hipótese; teste a hipótese mais provável com a menor verificação útil.
6. Planeje um diff mínimo antes de editar. Preserve arquitetura, contratos, estilo, alterações locais e arquivos não relacionados.
7. Valide a mudança pelo risco: teste focal primeiro; amplie para integração, regressão, build ou E2E quando o impacto justificar.
8. Revise o diff final, efeitos colaterais e comandos executados. Pare quando os critérios de aceitação estiverem atendidos; não comece tarefas extras sem necessidade.

## Roteamento por intenção

- Entender repositório, onboarding, fluxo de dados ou arquitetura desconhecida → `repo-reverse-engineering`.
- Bug, crash, lentidão ou regressão → `targeted-debugging-performance`; acrescente `testing-regression-quality` para regressão verificável.
- Login, permissões, sessão, tenant, exposição de dados ou segredos → `application-security-auth`.
- Infra, deploy, migração, banco, conexão, rollback ou custo operacional → `infrastructure-database-engineering`.
- Formulários, cadastro, CRUD, duplicidade ou consistência → `forms-crud-data-integrity`; acrescente segurança quando houver controle de acesso ou dados privados.
- Testes, qualidade de release ou mudança de comportamento → `testing-regression-quality`.
- UI nova ou redesign → `premium-distinctive-web-design`; ela também cobre a auditoria de UX/acessibilidade. Não carregue uma segunda skill de design.
- React/Next.js com gargalo de performance → `vercel-react-performance`, junto da skill de debug apenas quando necessário.
- Supabase/PostgreSQL e RLS → `supabase-postgres-specialist`. Não aplicar comandos ou sintaxe específicos ao MySQL; adaptar apenas conceitos portáveis.
- Remotion ou HyperFrames → a skill específica do pipeline utilizado.
- REA / análise assistida autorizada → `rea-assisted-analysis`.
- Reduzir custo de contexto ou uso de IA → `ai-token-budget`.
- Criar ou revisar as próprias skills → usar as práticas de autoria do catálogo e referências públicas; auditar gatilhos e sobreposição antes de criar qualquer skill nova.

## Guardrails comuns

- Não expor segredos, tokens, dados pessoais nem valores de variáveis sensíveis em logs ou relatórios.
- Não executar exclusões, reset, migração destrutiva, alteração de permissões/segredos, mudança de DNS, commit/push ou deploy sem autorização adequada ao impacto.
- Nunca enfraquecer autenticação, autorização ou testes para fazer a verificação passar.
- Não inventar comandos, ferramentas, resultados, telemetria, testes, screenshots ou deploys.
- Em projetos do usuário, respeitar a identidade correta do repositório e da aplicação; confirme pelo contexto do código antes de tocar no backend.
- Em stack desconhecida, descubra a tecnologia real antes de aplicar uma skill específica.
- Não adicionar dependência, infraestrutura paga ou serviço externo sem justificar benefício e custo.
- Não inventar arquitetura ou reescrever o sistema quando uma correção localizada basta.

## Saída padrão

Se a tarefa for simples, responda com o resultado e a verificação em poucas linhas. Se for complexa, informe apenas:
1. Diagnóstico/evidência.
2. Mudança realizada e arquivos afetados.
3. Testes realmente executados e resultados.
4. Risco ou bloqueio restante.

Não narre cada passo. Não repita informações já presentes no diff ou nos logs. Se não for possível concluir, diga exatamente qual evidência ou acesso falta e indique o próximo passo mínimo.
