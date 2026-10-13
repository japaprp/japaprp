---
name: ai-token-budget
description: Reduzir tokens e créditos de IA com contexto seletivo, tarefas pequenas, checkpoints e telemetria honesta de consumo.
---

# AI Token Budget & Efficient Agent Workflow

## Protocolo econômico
1. Comece com objetivo, restrições, critérios de aceitação e arquivos prováveis.
2. Use git status/diff, árvore rasa, busca de símbolos e testes focados antes de abrir arquivos extensos.
3. Leia instruções e trechos necessários; expanda contexto sob demanda. Não cole arquivos/logs inteiros quando bastam trechos.
4. Divida mudanças grandes em etapas verificáveis e mantenha resumo compacto de decisões, estado, arquivos e próximo passo.
5. Reaproveite resultados validados e não repita análises sem novas evidências.
6. Prefira ferramentas determinísticas (ripgrep, testes, typecheck, linter, EXPLAIN, profiler) para fatos que não exigem geração.
7. Peça diff pequeno e relatório final objetivo; não desperdice tokens narrando ou repetindo contexto.
8. Pare a exploração quando a hipótese estiver confirmada e o teste de regressão passar.
9. Nunca economize removendo testes críticos, segurança ou revisão de migração.

## Medidor de tokens/custo
- Separe tokens reais reportados pelo provedor, estimativas locais e dados indisponíveis.
- Tokens reais exigem telemetria/usage metadata da API ou ferramenta. A interface do ChatGPT/Codex pode não expor consumo por chamada ao projeto.
- Se não houver contagem real, rotule como estimativa e informe o método; nunca apresente aproximação como gasto real.
- Acompanhe input/output tokens, cached input quando disponível, modelo, requests, período e preço versionado.
- Só calcule custo com preço conhecido; mostre moeda, fonte e se é estimado.
- Assinatura fixa não deve ser convertida em custo marginal por token sem base oficial.
- Não guarde prompts completos ou segredos apenas para contar consumo. Prefira metadados agregados e retenção curta.
- Mostre fonte, última atualização, quota conhecida/desconhecida e limite configurado pelo usuário. Não invente quota.
- Alertas 50/80/100% são limites locais configuráveis, não garantias do provedor.

Skills não ativam telemetria automaticamente. Confirme qual API/CLI expõe uso antes de prometer um medidor preciso.