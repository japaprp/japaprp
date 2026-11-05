# Portfólio — matriz de oportunidades de Data Science e segurança

> Estado inicial em 2026-11-05. Este arquivo registra oportunidades e referências; não afirma que modelos estejam implementados nem que dados de produção estejam disponíveis. Atualizar somente após inspecionar o repositório e confirmar os dados.

## Decisão arquitetural
Criar padrões e módulos reutilizáveis, não um banco compartilhado entre aplicações. Cada projeto conserva repositório, banco, credenciais, tenants, permissões e ciclo de release próprios. Reutilizar definições, código sem estado, contratos e procedimentos; compartilhar dados agregados/anonimizados somente com autorização e finalidade documentada.

## Referências open-source avaliadas

| Repositório | Evidência observada | Uso nesta etapa | Limites |
|---|---|---|---|
| [Beginner-Data-Science-Projects](https://github.com/tkarim45/Beginner-Data-Science-Projects) | README organiza notebooks em classificação, regressão, séries temporais, NLP, clustering, recomendação, anomalias, EDA e visão computacional. Inclui retail sales forecasting, product recommendation, market basket e supply-chain demand prediction. | Catálogo educacional para estudar técnicas e selecionar notebooks pontuais. | Não importar tudo. Metadados consultados indicam aprox. 862 MB; evitar clone completo no equipamento limitado. Inspecionar notebook, dataset, dependências e licença antes de reutilizar. |
| [Mafifrizi/ARES](https://github.com/Mafifrizi/ARES) | README descreve plataforma red-team direcionada por operador, com FastAPI/Python, React, controles de escopo e módulos MITRE ATT&CK. Metadados consultados indicam MIT, 827 stars e 168 forks em 2026-11-05. | Referência separada para estudar controles de escopo, auditoria e validação de segurança autorizada. | Não é plataforma de analytics nem dependência de negócio. Não executar módulos ofensivos nos sistemas reais. Revisar código, dependências e escopo antes de qualquer teste. |

## Matriz por projeto

| Projeto | Repositório identificado | Oportunidades iniciais | Dados mínimos a confirmar | Prioridade |
|---|---|---|---|---|
| Horti-fruit / Varejão do Povo | [japaprp/varejao-backend](https://github.com/japaprp/varejao-backend) — público | Já há serviço de analytics com resumo por período, série diária e top produtos; serviço de estoque registra entradas e perdas. Próximo: validar histórico e persistência antes de prever demanda. | O código usa pedidos, itens, saídas, entradasEstoque e perdasEstoque em database.json; confirmar volume/histórico real, custo por item, datas e integridade. | Alta oportunidade; prontidão de ML ainda baixa |
| Lanchonete / Hamburgueria com PDVs | [japaprp/hamburgueria](https://github.com/japaprp/hamburgueria) — privado | Modelos Order, OrderItem, InventoryItem, RecipeItem e DailySalesAggregate; serviço de agregação por data/tenant; entradas para demanda, custo e margem. | Confirmar histórico real e cobertura temporal; revisar agregador antes de usar métricas em modelos. | Alta oportunidade; prontidão de dados promissora, QA pendente |
| Sistema de RH | Repositório ainda não confirmado; o portfólio lista o sistema, mas não associa inequivocamente um repo. | Indicadores agregados de quadro, absenteísmo, rotatividade e treinamento. | Dados minimizados/autorizados, definições, departamento, períodos e regras de acesso. | Alta, controles reforçados |
| Perifa Pro | [japaprp/Perifa-Pro](https://github.com/japaprp/Perifa-Pro) — privado | Adoção, funis, retenção, uso de funcionalidades e indicadores agregados. | Eventos, definições de usuário ativo/conversão, timestamps e finalidade. | Média |
| Guerra Infinita | [japaprp/infinit-war-guerra-infinita](https://github.com/japaprp/infinit-war-guerra-infinita) — privado | Balanceamento, telemetria de gameplay, progressão, retenção e anomalias operacionais. | Eventos, versões, progressão, economia, sessões e definições de métricas. | Média; não misturar com dados de Dark War: Survival |
| Estância Renascer Belvedere | [japaprp/estacia-renascer-belvedere](https://github.com/japaprp/estacia-renascer-belvedere) — público | Procura por datas, origem de contatos, conversão em reservas e sazonalidade. | Leads/reservas, datas, origem, status e receita, se disponíveis e autorizados. | Média |
| Salão | [japaprp/salao](https://github.com/japaprp/salao) — público | Ocupação da agenda, recorrência, faltas, serviços, comissões e demanda. | Agendamentos, status, serviços, duração, profissional e valores. | Média |
| Salão do Arthur | [japaprp/salao-do-arthur](https://github.com/japaprp/salao-do-arthur) — público; também existe repo legado arquivado salao-do-artur. | Reutilizar padrões confirmados; agenda, recorrência e serviços. | Confirmar qual repo é fonte ativa e quais dados existem. | Pendente |
| EventosRP | [japaprp/eventosrp](https://github.com/japaprp/eventosrp) — público | Demanda por datas, ocupação, conversão de consultas e receita por evento. | Consultas, reservas, calendário, status, tipo e valores. | Média |
| Casa Prática OFC | Repositório de aplicação próprio ainda não confirmado; WA-AKG é referência separada, não app comprovadamente instalado. | Ranking de produtos, cliques/conversões, comissão, sazonalidade e campanhas. | Relatórios autorizados de afiliado, cliques, pedidos, comissão, SKU e datas; respeitar termos da plataforma. | Pendente |

## Evidências da primeira inspeção de código

### Horti-fruit / Varejão do Povo
- O backend contém analyticsService.js com resumo por dia/semana/mês/ano, série temporal e top 10 produtos.
- inventoryService.js registra entradas e perdas e calcula giro/saídas; database.json contém catálogo de produtos de exemplo.
- repository.js lê e grava database.json diretamente no filesystem. Isso é uma limitação importante para analytics confiável em operação concorrente/produção; não tratar o arquivo versionado como histórico real de vendas.
- Conclusão: há lógica inicial de indicadores, mas a prontidão para previsão depende de validar origem, persistência, volume e qualidade do histórico.

### Hamburgueria
- Foram localizados modelos de pedidos, itens, estoque, ficha técnica/receita e agregados diários por tenant, canal, tipo de pedido e PDV.
- QA estático em DailySalesAggregateService.php: a consulta de pedidos não seleciona payment_status, mas paid_orders_count tenta ler esse atributo; a contagem fica incorreta. A margem soma itens de todos os pedidos do grupo, enquanto receita soma apenas status finais, podendo incluir cancelados/pendentes.
- QA estático em ReportService.php: salesByDay aplica escopo de tenant na consulta, mas a chave de cache contém somente intervalo de datas. Como a API define TenantContext por usuário, duas empresas consultando o mesmo intervalo podem compartilhar a mesma chave e receber resultado de outra empresa. Risco alto de vazamento entre tenants; precisa de teste de regressão e correção incluindo tenant_id na chave.
- BelongsToTenant só adiciona filtro quando TenantContext não é null. A rota API inspecionada usa middleware tenant e limpa o contexto em finally; o comando agendado roda sem tenant e agrega explicitamente todos os tenants por grupo. Manter esse comportamento batch apenas se for intencional e documentado; consultas de negócio sem contexto devem falhar fechadas ou exigir tenant explícito.
- A tabela daily_sales_aggregates tem unique composto incluindo pdv_id nullable. Em bancos que permitem múltiplos NULL em índices únicos, upsert pode não ser idempotente para linhas sem PDV; confirmar no SGBD configurado e cobrir teste.
- O modelo DailySalesAggregate é tenant-aware. Conclusão: a estrutura de dados é promissora, mas existem defeitos de contagem, margem e isolamento/cache que precisam ser corrigidos e testados antes de confiar nos indicadores ou treinar modelos.

## Sequência recomendada
1. Inventariar schema, granularidade, cobertura, qualidade, atualização, permissões e isolamento em cada repo.
2. Horti-fruit: começar com relatório de vendas/estoque e baseline sazonal; depois testar previsão de demanda e perdas.
3. Hamburgueria: validar ficha técnica, custo, pedidos e estoque; construir margem e previsão por faixa horária.
4. RH: iniciar somente com métricas agregadas e controles LGPD; excluir inferências sensíveis e decisões automatizadas sobre pessoas.
5. Priorizar os demais por prontidão dos dados e valor operacional, não pela sofisticação do algoritmo.
6. ARES: apenas referência para plano de auditoria autorizado, em ambiente de teste isolado.

## Técnicas para selecionar pontualmente

| Técnica do catálogo educacional | Aplicação possível | Cuidado |
|---|---|---|
| Retail Sales Forecasting / Time Series | Horti-fruit e hamburgueria | Histórico curto/descontínuo pode não sustentar previsão |
| Supply Chain Demand Prediction | Reposição e compras | Não substitui regras de estoque e conhecimento operacional |
| Market Basket Analysis | Combos e produtos comprados juntos | Associação não prova causalidade |
| Product Recommendation | Catálogo e campanhas | Exige volume suficiente e finalidade adequada |
| EDA / dashboards | Todos | Gráfico sozinho não explica causa |
| Anomaly Detection | Falhas operacionais, estoque ou transações | Alerta não é fraude confirmada |
| Classification / Regression | Casos com alvo e rótulos claros | Não usar scores para decisões automatizadas sobre pessoas |

## Governança
- Um tenant/projeto não pode consultar tabelas, arquivos, modelos ou credenciais de outro.
- Minimizar dados; documentar finalidade, retenção e base legal aplicável.
- Não exportar dados reais para notebooks públicos, datasets externos ou ferramentas não aprovadas.
- Não usar dados sensíveis ou atributos protegidos para perfis, pontuações ou decisões individuais.
- Modelos devem ter baseline, avaliação temporal quando aplicável, explicabilidade, monitoramento e fallback.
- Integrações futuras exigem contrato/API explícito e escopos mínimos.
- Esta matriz é recomendação estratégica; nenhum módulo foi implementado ou validado em produção por este registro.

## Estado de validação
- PASS — repositório Conselho Central, branch de trabalho e catálogo atual inspecionados.
- PASS — repositórios listados como confirmados encontrados na conta GitHub conectada.
- PASS — README do Beginner Data Science Projects consultado para categorias e exemplos.
- PASS — README e metadados do ARES consultados para escopo e licença declarada.
- PASS — inspeção estática inicial de serviços de analytics/estoque do Horti-fruit e modelos/agregador/relatórios/middleware da Hamburgueria.
- PASS — defeito de seleção de payment_status e risco de chave de cache sem tenant identificados diretamente no código.
- BLOCKED — volume, histórico real, qualidade e persistência dos dados não foram validados em ambiente de execução; SGBD configurado não foi confirmado para testar a unicidade com pdv_id NULL.
- NOT RUN — notebooks externos não foram executados.
- NOT RUN — testes de agregação, correção de payment_status/margem, isolamento de cache multi-tenant e upsert com pdv_id NULL não foram executados.
- NOT RUN — nenhum modelo foi treinado, implantado ou conectado aos aplicativos.
- NOT RUN — auditoria ARES não foi executada.
