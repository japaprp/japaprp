# Portfólio — matriz de oportunidades de Data Science e segurança

> Estado inicial em 2026-11-05. Este arquivo registra oportunidades e referências; não afirma que modelos estejam implementados nem que dados de produção estejam disponíveis. Atualizar somente após inspecionar o repositório e confirmar os dados.

## Decisão arquitetural
Criar padrões e módulos reutilizáveis, não um banco compartilhado entre aplicações. Cada projeto conserva repositório, banco, credenciais, tenants, permissões e ciclo de release próprios. Reutilizar definições, código sem estado, contratos e procedimentos; compartilhar dados agregados/anonimizados somente com autorização e finalidade documentada.

## Referências open-source avaliadas

| Repositório | Evidência observada | Uso nesta etapa | Limites |
|---|---|---|---|
| [Beginner-Data-Science-Projects](https://github.com/tkarim45/Beginner-Data-Science-Projects) | README organiza notebooks em classificação, regressão, séries temporais, NLP, clustering, recomendação, anomalias, EDA e visão computacional. Inclui retail sales forecasting, product recommendation, market basket e supply-chain demand prediction. | Catálogo educacional para estudar técnicas e selecionar notebooks pontuais. | Não importar tudo. Metadados consultados indicam aprox. 862 MB; evitar clone completo no equipamento limitado. Inspecionar notebook, dataset, dependências e licença antes de reutilizar. |
| [Mafifrizi/ARES](https://github.com/Mafifrizi/ARES) | README descreve plataforma red-team direcionada por operador, com FastAPI/Python, React, controles de escopo e módulos MITRE ATT&CK. Metadados consultados indicam MIT, 827 stars e 168 forks em 2026-11-05. | Referência separada para estudar controles de escopo, auditoria e validação de segurança autorizada. | Não é plataforma de analytics nem dependência de negócio. Não executar módulos ofensivos nos sistemas reais. Revisar código, dependências e escopo antes de qualquer teste. |

## Referência transversal — legislação brasileira e governança

| Repositório | Evidência consultada em 2026-11-05 | Uso no Conselho Central | Limitações e controles obrigatórios |
|---|---|---|---|
| [ctresb/leis — Todas as leis do Brasil](https://github.com/ctresb/leis) | Repositório público; página consultada exibia aproximadamente 2,5 mil stars e 418 forks. Organiza legislação em Markdown, com metadados estruturados e link de origem. A estrutura inclui normas federais, estaduais/distritais, municipais, reguladores, tratados e parte da jurisprudência. | Fonte de descoberta e referência para localizar normas brasileiras, apoiar análise preliminar de requisitos legais e orientar skills de governança, privacidade, segurança, RH, biometria, câmeras e operações. Não é uma dependência de runtime nem um parecer jurídico. | O próprio README declara que as conversões/OCR são informativas e não substituem Diário Oficial; exige conferir a fonte. A cobertura tem lacunas declaradas (inclusive municipal e atos infralegais), e a atualização/qualidade varia por fonte. Verificar versão, vigência, alterações, jurisdição e texto oficial antes de qualquer decisão. Não presumir que “todas as leis” signifique cobertura completa. |

### Regra de uso jurídico
1. Pesquisar primeiro nesta referência catalogada e identificar a norma/artigo potencialmente aplicável.
2. Confirmar o texto, vigência, alterações, regulamentação e jurisprudência em fonte oficial competente (por exemplo, Planalto, Diário Oficial, órgão regulador ou tribunal).
3. Registrar jurisdição, data da consulta, URL oficial, versão e contexto de aplicação.
4. Separar informação geral de interpretação jurídica; apontar incerteza e encaminhar questões materiais a profissional qualificado.
5. Não tratar a base como prova de conformidade nem como substituta de avaliação jurídica, RIPD ou decisão do controlador.
6. Reutilizar essa referência entre projetos apenas como fonte pública; nunca compartilhar dados pessoais, imagens, biometria, credenciais ou documentos privados entre projetos.


## Referências open-source — criptografia e análise de credenciais

> Pesquisa inicial em 2026-11-05. Os números de stars são sinais de adoção observados na consulta, não medidas de segurança ou qualidade. Nenhuma ferramenta foi clonada, instalada ou executada.

| Projeto | Evidência pública consultada | Uso recomendado no Conselho | Licença / maturidade / limites |
|---|---|---|---|
| [CrypTool 2](https://github.com/CrypToolProject/CrypTool-2) | Repositório oficial descreve ambiente interativo de aprendizagem de criptografia e criptoanálise; 169 stars e 125 forks na página consultada. | Primeira escolha educacional para visualizar cifras, algoritmos, protocolos e conceitos de criptoanálise com exemplos didáticos. | Apache-2.0 declarada no GitHub. Projeto educacional; verificar requisitos de Windows/.NET e releases antes de qualquer instalação. |
| [CyberChef](https://github.com/gchq/CyberChef) | Ferramenta web para codificação, parsing, hashes, checksums, AES/DES/Blowfish, hexdumps e análise de dados; aproximadamente 36,3 mil stars e 4,2 mil forks. README informa execução local no navegador, sem envio do conteúdo ao servidor na versão não modificada; algumas operações específicas fazem chamadas externas. | Ferramenta prática para inspecionar formatos, transformar dados de laboratório, calcular hashes e explorar operações criptográficas sem criar scripts para cada tarefa. | Apache-2.0; atividade recente observada no repositório GCHQ. Preferir versão standalone verificada para dados sensíveis e revisar operações que fazem chamadas externas. |
| [OpenSSL](https://github.com/openssl/openssl) | Biblioteca/toolkit geral para TLS/DTLS/QUIC e primitivas criptográficas; aproximadamente 31,2 mil stars e 11,6 mil forks. | Referência técnica para certificados, chaves, assinaturas, hashes, TLS e interoperabilidade; útil para validar parâmetros e formatos em ambientes próprios. | Apache-2.0; projeto maduro e ativo. Exige cuidado com versões, opções legadas e configuração segura. |
| [GnuPG](https://github.com/gpg/gnupg) | Implementação livre de OpenPGP com criptografia, assinatura e gestão de chaves; o espelho GitHub consultado declara GPL e alerta que não é o canal de manutenção oficial. | Estudar cadeia de confiança, pares de chaves, assinaturas, revogação, exportação e formatos OpenPGP. | GPL; usar o site/repositório oficial do projeto para releases e suporte, não tratar o espelho GitHub como fonte primária de manutenção. |
| [Wireshark](https://github.com/wireshark/wireshark) | Analisador de protocolos e capturas; repositório GitHub é espelho read-only do GitLab oficial. Licença GPL-2.0; histórico extenso de commits. | Estudar negociação TLS/SSH, metadados de protocolo, certificados e comportamento de rede em capturas próprias ou sintéticas. | GPL-2.0; usar o repositório oficial GitLab para desenvolvimento. Capturas podem conter dados pessoais, tokens e conteúdo privado: sanitizar e limitar escopo. |
| [hashcat](https://github.com/hashcat/hashcat) | Plataforma de auditoria/recuperação offline de hashes com CPU/GPU, múltiplos backends e centenas de formatos; aproximadamente 27,3 mil stars e 3,6 mil forks. Licença MIT declarada. | Laboratório avançado para medir resistência de hashes sintéticos e avaliar políticas de senha com parâmetros controlados; também permite benchmarks para comparar custo de KDFs. | Ferramenta dual-use de alto potencial. Não integrar automaticamente nem apontar para dumps, contas ou serviços reais. Usar somente hashes sintéticos ou conjuntos próprios formalmente autorizados, com escopo e limites de execução documentados. |
| [John the Ripper (jumbo)](https://github.com/openwall/john) | Auditoria e recuperação offline de senhas; suporta numerosos formatos de hashes, arquivos e chaves protegidas. O projeto alerta que parte do código jumbo tem maturidade variável. | Alternativa para laboratório de hashes sintéticos e avaliação de formatos protegidos, comparando cobertura e compatibilidade com hashcat. | GPL-2.0-or-later com exceções e componentes sob termos distintos; revisar LICENSE e licenças por componente. Não usar em dados de terceiros ou credenciais de serviços. |

### Priorização para o Conselho

1. **Começar por CrypTool 2 + CyberChef** para ensino visual, parsing e experimentos reproduzíveis com dados sintéticos.
2. **Usar OpenSSL + GnuPG** como referências técnicas para operações reais de criptografia, certificados, assinaturas e gestão de chaves em ambiente próprio.
3. **Adicionar Wireshark** quando a pergunta exigir análise de tráfego/capturas autorizadas.
4. **Manter hashcat e John the Ripper como referências de laboratório avançado**, não como ferramentas padrão acionadas pelo roteador. A skill deve primeiro classificar o material, confirmar propriedade/autorização e limitar testes a hashes sintéticos ou próprios.
5. Não instalar nem clonar agora. Antes de adoção, verificar release atual, assinatura/checksum, dependências, compatibilidade com Windows/Android/Termux, consumo de RAM/CPU/GPU e licença aplicável.

### Regra de experimentação de credenciais

- Preferir hashes artificiais gerados para o laboratório e senhas descartáveis sem reutilização.
- Medir custo/tempo de derivação e comparar MD5/SHA simples com Argon2id, scrypt e bcrypt para fins didáticos; não transformar resultados em listas de senhas reais.
- Nunca inserir credenciais de jogo, dumps de usuários, tokens, arquivos de autenticação ou chaves privadas em serviços online de análise.
- Não testar login, SSH ou autenticação de serviços de terceiros. Para SSH, priorizar análise de configuração, fingerprint, algoritmo negociado e validação de host key em laboratório próprio.
- Preservar os originais; qualquer arquivo de teste deve ser descartável e isolado.

### Estado desta pesquisa
- PASS — GitHub Actions #66 da branch concluiu com sucesso no commit `ad74f15357b74150f1c5e902df08f3ee0bb1a4cf`.
- PASS — páginas oficiais/GitHub consultadas para CrypTool 2, CyberChef, OpenSSL, GnuPG, Wireshark, hashcat e John the Ripper.
- PASS — licenças declaradas e limitações relevantes registradas quando visíveis.
- NOT RUN — clonagem, instalação, execução, benchmark ou integração de qualquer ferramenta.
- NOT RUN — teste de compatibilidade em Windows, Galaxy Book Go, Galaxy S21 ou Termux.

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
- QA estático no índice unique de daily_sales_aggregates: inclui pdv_id nullable. O teste usa SQLite e SQLite permite múltiplos NULL em índices UNIQUE; assim, agregações sem PDV podem duplicar em upserts repetidos. Confirmar também no driver de produção e adicionar teste de idempotência.
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
- PASS — inspeção estática inicial de analytics/estoque e snapshot database.json do Horti-fruit.
- PASS — inspeção estática de modelos/agregador/relatórios/middleware/migration da Hamburgueria.
- PASS — defeito de seleção de payment_status, margem sem filtro de status e risco de chave de cache sem tenant identificados diretamente no código.
- PASS — no snapshot versionado do Horti-fruit, pedidos, entradasEstoque e perdasEstoque estão vazios; previsão não pode ser validada com esse conjunto.
- PASS — o phpunit.xml configura SQLite em memória; o índice UNIQUE com pdv_id nullable requer teste específico de idempotência.
- BLOCKED — dados de produção, volume histórico e driver real de produção não foram consultados.
- NOT RUN — notebooks externos não foram executados.
- NOT RUN — testes de agregação, correção de payment_status/margem, isolamento de cache multi-tenant e upsert com pdv_id NULL não foram executados.
- NOT RUN — testes de concorrência/persistência do Varejão, filtro de status em giro de estoque e ordenação temporal da série não foram executados.
- NOT RUN — nenhum modelo foi treinado, implantado ou conectado aos aplicativos.
- NOT RUN — auditoria ARES não foi executada.
