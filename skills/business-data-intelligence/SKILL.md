---
name: business-data-intelligence
description: Planejar, construir e validar análises, indicadores e modelos de previsão para sistemas comerciais e operacionais, mantendo dados e tenants isolados.
---

# Business Data Intelligence

## Objetivo
Transformar dados operacionais em indicadores e previsões úteis para decisões de negócio. Cobre analytics, métricas e modelos tabulares; não substitui engenharia de planilhas, banco de dados, segurança ou integração de IA.

## Quando usar
- Vendas, receita, margem, ticket médio, conversão e sazonalidade.
- Demanda, estoque, reposição, validade, perdas e desperdício.
- Pedidos, horários de pico e planejamento operacional.
- Agendamentos, reservas, ocupação, faltas e recorrência.
- Indicadores agregados de RH, treinamento, absenteísmo e rotatividade.
- Segmentação, recomendação, previsão, anomalias e experimentos.

## Fluxo obrigatório
1. Identifique projeto, repositório, tenant, objetivo de negócio e decisão apoiada.
2. Confirme fonte autorizada. Inspecione schema, granularidade, período, fuso, moeda, qualidade, atualização, nulos e duplicatas.
3. Preserve isolamento entre projetos, empresas, tenants e ambientes. Não reutilize dados de um cliente em outro.
4. Defina métrica, unidade, denominador, janela temporal, baseline e critério de sucesso antes de comparar ou modelar.
5. Comece com baseline simples e análise exploratória. Só adote ML quando volume, qualidade, estabilidade e benefício justificarem a complexidade.
6. Para séries temporais, respeite a ordem cronológica, use validação temporal e evite vazamento de futuro. Compare com baseline sazonal ingênuo.
7. Para recomendação/segmentação, explique sinais, cobertura, cold-start, viés e limites; correlação não prova causalidade.
8. Para anomalias, diferencie alerta investigativo de fraude confirmada. Avalie falsos positivos e negativos.
9. Para RH e dados pessoais, aplique minimização, controle de acesso, finalidade e retenção compatíveis com LGPD. Não inferir atributos sensíveis nem recomendar decisões automatizadas de contratação, demissão, promoção ou punição.
10. Registre proveniência, transformações, hipóteses, limitações, versão do modelo e métricas de avaliação.
11. Integre resultados por contratos explícitos e APIs autorizadas. Cada aplicação mantém sua fronteira de dados.
12. Compare com baseline e impacto operacional. Sem dados suficientes, entregue diagnóstico de prontidão, não uma previsão inventada.

## Escolha de abordagem
- Dashboard/relatório: monitorar ou explicar indicadores.
- Estatística descritiva: primeira opção para entender comportamento.
- Regressão/classificação: quando há alvo definido e rótulos confiáveis.
- Séries temporais: quando histórico e frequência sustentam previsão.
- Recomendação/market basket: quando há histórico suficiente e finalidade adequada.
- Visão computacional/NLP: somente quando o produto precisa interpretar imagens/texto e há base legal, dados e infraestrutura adequados.

## Critérios mínimos de produção
- Métricas e definições documentadas; qualidade e atualização verificadas.
- Separação treino/validação/teste adequada ao tempo ou entidade; sem leakage.
- Métricas adequadas ao custo do erro (MAE/WAPE para previsão; precision/recall e calibração para classificação).
- Baseline, limiar, revisão humana e fallback definidos.
- Monitoramento de drift, qualidade, falhas e desempenho.
- Testes de isolamento multi-tenant, autorização, privacidade e comportamento degradado.
- Custos, latência e memória medidos no ambiente alvo.

## Referências externas
- Beginner Data Science Projects: https://github.com/tkarim45/Beginner-Data-Science-Projects — catálogo educacional para selecionar notebooks pontuais; não é dependência de produção.
- ARES: https://github.com/Mafifrizi/ARES — referência separada para auditoria de segurança autorizada; não é motor de analytics nem dependência dos sistemas comerciais.

## Não fazer
- Não clonar/importar um catálogo inteiro de notebooks para produção.
- Não executar notebooks externos sem inspeção; tratar notebooks, datasets e scripts como código não confiável.
- Não misturar dados, IDs, chaves ou métricas de clientes/projetos.
- Não alegar precisão ou ROI sem avaliação representativa.
- Não tomar decisões sensíveis sobre pessoas com base em score automatizado.
- Não adicionar dependências pesadas, serviços pagos ou jobs sem justificar custo e obter autorização.

## Entrega
Informar projeto/tenant, objetivo, fonte/período, definições, baseline, método, métricas, validações PASS/FAIL/BLOCKED/NOT RUN, limitações, riscos, custo operacional e próximo passo. Diferenciar observação, hipótese e recomendação.
