---
name: infrastructure-database-engineering
description: Auditar infraestrutura, banco de dados, migrações, conexões, deploys e recuperação segura com custo controlado.
---

# Infrastructure & Database Engineering

## Protocolo
1. Leia instruções do repositório e identifique stack, entrypoints, manifests, Dockerfile/Blueprint, migrations e configuração de deploy.
2. Comece por logs, stack trace, status, diff recente e arquivos diretamente relacionados. Não varra o repositório inteiro sem motivo.
3. Mapeie o caminho mínimo: cliente → API → serviço → banco/terceiro → resposta.
4. Confirme nomes de variáveis e mecanismo de configuração; nunca imprima segredos.
5. Verifique conectividade, DNS, TLS, pool, timeouts, permissões, limites, health checks e compatibilidade entre driver e banco.
6. Para schema, confira migrations, constraints, índices, foreign keys, transações e rollback.
7. Prefira migrations versionadas e idempotentes. Não execute DROP, reset, truncate ou migração destrutiva sem aprovação explícita e backup validado.
8. Em produção, planeje rollback e verificação pós-deploy. Não alegue sucesso sem evidência.
9. Faça smoke test do caminho crítico e registre comandos, resultados e riscos restantes.

## Banco
- Use queries parametrizadas e transações para operações atômicas.
- Evite N+1, consultas sem paginação e SELECT * em caminhos quentes.
- Inspecione o plano de execução antes de otimizar consultas lentas.
- Considere concorrência, idempotência, locks, deadlocks, retries com backoff e limites de pool.
- Não copie dados de produção para testes sem anonimização.

## SSH, terminal remoto e servidores

- Confirme host, usuário, ambiente e finalidade da conexão antes de executar comandos; use apenas conexões e contas autorizadas.
- Prefira chaves SSH protegidas e permissões mínimas. Nunca solicite, imprima, registre ou comite chaves privadas, senhas, tokens ou conteúdo de arquivos sensíveis.
- Verifique fingerprint/host key por canal confiável; não desative validação de host para contornar erros.
- Comece com comandos de leitura (pwd, whoami, hostname, status e logs limitados) e confirme o diretório e o ambiente antes de qualquer escrita.
- Use timeouts, sessões reproduzíveis e logs redigidos. Evite despejar logs extensos ou variáveis de ambiente que possam conter segredos.
- Antes de reiniciar serviços, mudar firewall/permissões, editar configuração, instalar pacotes ou encerrar processos, avalie impacto, janela, rollback e autorização.
- Não execute comandos destrutivos ou encadeados difíceis de revisar. Explique comandos de alto impacto e peça aprovação quando a autorização não estiver clara.
- Ao copiar arquivos, valide origem/destino, permissões, integridade e exposição de dados; não transfira dados de produção para máquinas não autorizadas.

## Infraestrutura e custo
- Verifique limites de CPU/RAM, armazenamento, egress, backups e retenção.
- Não habilite serviços pagos nem faça upgrade sem autorização expressa.
- Diferencie local, staging e produção; use timeouts explícitos e encerramento gracioso.

## Confiabilidade, observabilidade e release

- Defina health checks que testem dependências críticas sem tornar uma dependência transitória uma indisponibilidade total desnecessária.
- Para serviços com tráfego real, identifique sinais úteis: taxa de erro, latência p95/p99 quando disponível, saturação, falhas de dependências e freshness dos dados.
- Antes de deploy, confirme escopo, ambiente, migrações, compatibilidade de versão, smoke tests e procedimento de rollback.
- Prefira releases graduais quando suportadas; não prometa zero downtime sem validar arquitetura e plataforma.
- Para incidentes, preserve logs relevantes sem segredos, estabeleça impacto, mitigue primeiro e faça análise de causa após estabilizar.
- Meça baseline antes de otimizar. Não invente SLO, percentis, redução de custo ou ganho de desempenho sem dados.
- Não adicione monitoramento pago nem altere planos/limites de hospedagem sem autorização de custo.

## Entrega
Causa comprovada ou hipóteses, arquivos envolvidos, correção mínima, migration/rollback, testes, impacto operacional/custo e pontos não verificados.