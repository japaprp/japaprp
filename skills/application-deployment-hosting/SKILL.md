---
name: application-deployment-hosting
description: Escolher e publicar sites, APIs e backends em hospedagem apropriada, com configuração segura, domínio/HTTPS, observabilidade, custos e rollback.
---

# Application Deployment & Hosting

## Objetivo
Levar uma aplicação do repositório até um ambiente acessível e operável, selecionando a hospedagem conforme stack, requisitos, tráfego, persistência, orçamento e manutenção. Deploy é um fluxo verificável, não apenas clicar em “Publish”.

## 1. Descoberta antes da escolha

Inspecione o projeto e determine:
- Tipo de aplicação: site estático, SPA, SSR, API/backend, worker, cron job ou aplicação full-stack.
- Stack, versão de runtime, comandos de build/start, porta, health check e arquivos de configuração.
- Necessidade de banco, armazenamento persistente, filas, jobs, WebSockets, uploads e tarefas em segundo plano.
- Requisitos de região/latência, disponibilidade, escala, segurança, backups e domínio.
- Orçamento mensal máximo, uso previsto e tolerância a suspensão, cold start ou limites de plano gratuito.

Não escolha um provedor apenas por popularidade. Primeiro identifique os requisitos reais e as restrições do plano.

## 2. Escolha do serviço

Compare provedores e produtos compatíveis, por exemplo:
- **Frontend estático/SPA:** Vercel, Cloudflare Pages, Netlify ou hospedagem estática equivalente.
- **API/backend/container:** Render, Railway, Fly.io ou serviço equivalente, conforme runtime, região, rede e modelo de cobrança.
- **Funções/serverless:** Vercel Functions, Cloudflare Workers ou alternativas quando limites e runtime atenderem.
- **Banco gerenciado:** escolha um serviço compatível com o mecanismo usado e confirme plano, persistência, backups, limites de conexão e região.
- **VM/servidor próprio:** considere apenas se houver necessidade e capacidade para atualizar o sistema operacional, firewall, TLS, monitoramento, backups e resposta a incidentes.

Essa lista não garante disponibilidade, gratuidade ou elegibilidade atual. Consulte preços, limites, regiões e políticas oficiais no momento da decisão. Diferencie plano grátis, crédito promocional, trial e custo recorrente. Calcule também egress, armazenamento, banco, backups, domínio, logs e serviços auxiliares.

## 3. Preparar a aplicação

1. Leia README, manifests, Dockerfile, scripts e workflows existentes.
2. Confirme que o build/start funcionam localmente ou em ambiente reproduzível.
3. Garanta que o servidor escute na porta fornecida pelo ambiente quando exigido; não fixe portas sem motivo.
4. Adicione health/readiness checks adequados e graceful shutdown quando necessário.
5. Separe configuração por ambiente e documente apenas nomes de variáveis.
6. Garanta migrações repetíveis e estratégia de inicialização; não execute SQL destrutivo automaticamente.
7. Verifique dependências, lockfile, tamanho do artefato, arquivos estáticos, logs e limites de memória/CPU.
8. Para workers e cron jobs, use serviços próprios em vez de esconder tarefas duradouras dentro de uma requisição web.

## 4. Segurança de produção

- Segredos apenas em variáveis protegidas/secret manager; nunca em Git, frontend público, imagem Docker ou logs.
- Use princípio do menor privilégio para deploy tokens, banco, armazenamento e contas de serviço.
- Configure HTTPS e cookies seguros; valide CORS, origens, headers e redirects.
- Não exponha painel administrativo, banco, debug endpoint ou arquivos de configuração.
- Restringa acesso de rede e portas; mantenha runtime e dependências atualizados.
- Evite executar migração destrutiva em produção sem backup, plano de rollback e aprovação explícita.
- Não cole tokens, chaves privadas, connection strings ou valores de env no relatório.

## 5. Domínio e DNS

- Antes de alterar DNS, confirme domínio, provedor, registros atuais, destino esperado e impacto sobre site/e-mail.
- Use instruções oficiais do provedor para CNAME/A/AAAA/TXT e verificação de domínio; não invente valores.
- Preserve registros de e-mail (MX/SPF/DKIM/DMARC) quando não fizerem parte do escopo.
- Confirme propagação, certificado TLS, redirecionamento HTTP→HTTPS e domínio canônico.
- Mudanças de DNS exigem autorização explícita; prepare os valores e explique rollback antes de alterar.

## 6. Deploy seguro e reversível

1. Defina ambiente e commit/branch exatos; não publique branch ou repositório errado.
2. Rode build e testes disponíveis; se não puder executar, diga claramente.
3. Configure variáveis por nome e valide presença sem imprimir valores.
4. Faça deploy conforme a autorização e o risco; não atualize produção silenciosamente.
5. Verifique estado do deploy, logs de inicialização, health check, rotas críticas e conexão com banco.
6. Teste fluxo principal com dados sintéticos, sem ações financeiras ou irreversíveis reais.
7. Se falhar, capture erro relevante sem segredos, identifique causa e corrija o mínimo necessário.
8. Tenha rollback: versão anterior, migração compatível e procedimento de recuperação. Não reverta banco cegamente se isso puder causar perda de dados.

## 7. Persistência e operação

- Confirme se o filesystem é efêmero; uploads e dados duráveis precisam de volume ou armazenamento apropriado.
- Configure backups e teste recuperação quando dados forem importantes.
- Monitore disponibilidade, erros, latência, consumo, fila, conexões de banco e limites do plano.
- Documente logs, health checks, alertas, reinício, deploy e rollback.
- Para serviços gratuitos, monitore suspensão por inatividade, limites de uso, quotas e mudanças de política.
- Para banco, valide região, TLS, pooling, limite de conexões, credenciais separadas e política de backup.
- Não confunda “serviço online” com “aplicação funcional”: confirme endpoint e jornada de usuário.

## 8. Critérios de aceite

- Provedor escolhido com justificativa de stack, persistência, custo e limites.
- Build/deploy com status observado; URL real confirmada a partir do provedor ou output da ferramenta.
- HTTPS, health check e rota principal verificados quando acessíveis.
- Variáveis e banco configurados sem exposição de segredos.
- Persistência, logs, backups e rollback considerados conforme criticidade.
- Custos recorrentes e limitações do plano comunicados.
- Nenhum sucesso declarado sem evidência observável.

## Guardrails

- Não comprar plano, domínio ou recurso pago sem autorização explícita.
- Não alterar DNS, segredos, banco ou produção sem autorização adequada ao impacto.
- Não inventar URL de produção, status de deploy, preço atual ou disponibilidade de plano gratuito.
- Não destruir recursos existentes nem recriar infraestrutura sem necessidade demonstrada.
- Preferir o menor diff possível e respeitar arquivos de configuração existentes.

## Saída esperada
Resuma provedor e produto escolhidos, motivo, URL confirmada, serviços dependentes, custos/limites, verificações realizadas, riscos e como reverter.
