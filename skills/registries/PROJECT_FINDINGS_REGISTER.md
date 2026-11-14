# Registro de findings dos projetos

**Snapshot inicial:** 2026-11-14  
**Branch:** `feat/project-findings-inventory-20261114`  
**Base:** HEAD verificado do PR #6 do Conselho Central  
**Fonte canônica:** `skills/registries/PROJECT_FINDINGS.json`

## Objetivo

Manter um inventário rastreável de problemas por projeto, sem misturar repositórios, branches, dados, credenciais, ambientes ou ciclos de release. Cada finding possui ID estável, origem, evidência, status, correção associada, teste de regressão e critérios de encerramento.

## Regras de encerramento

Um finding só pode passar para **PASS** quando:
1. a origem e o comportamento afetado estiverem identificados;
2. a correção estiver vinculada ao commit exato;
3. o teste de regressão correspondente tiver sido executado e aprovado nesse commit;
4. a evidência do CI/runtime for independente da autodeclaração de quem implementou;
5. o QA confirmar que o resultado atende ao critério de aceite.

Um CI verde em SHA anterior, um teste apenas estrutural ou uma descrição de PR não encerram um finding. Resultados ausentes não significam sucesso.

## Estados

| Estado | Significado |
|---|---|
| PASS | Correção e regressão comprovadas no commit final |
| FAIL | Validação executada e falhou |
| BLOCKED | Não é seguro ou possível avançar por falta de acesso, decisão, capacidade ou autorização |
| NOT RUN | Etapa ainda não executada; não representa sucesso nem falha |

Fatos, inferências, hipóteses e desconhecidos são separados no campo `source.evidence_label`.

## Frentes e isolamento

- **Conselho Central:** governança, roteamento, orquestração e qualidade do próprio núcleo.
- **Guerra Infinita — desenvolvimento:** código, builds, autenticação, backend, banco, UI e testes do sucessor original.
- **Dark War: Survival — REA:** pesquisa de artefatos originais e documentação. Compartilha apenas a linha estratégica `guerra-infinita`; não compartilha branch de desenvolvimento, pipeline de build, arquivos-fonte ou credenciais.
- **Demais aplicações:** cada uma permanece vinculada ao próprio `project_id` e repositório.
- **Casa Prática OFC:** frente de comércio/afiliados independente; não há repositório GitHub verificado no snapshot.

## Findings iniciais

| ID | Projeto/frente | Prioridade | Estado | Próximo gate |
|---|---|---:|---|---|
| CC-001 | Conselho Central / ativação | P0 | NOT RUN | Fresh-session A/B/C |
| CC-002 | Conselho Central / orquestração | P0 | NOT RUN | Runtime real D1-D3 |
| CC-003 | Conselho Central / open source | P1 | BLOCKED | Decisões explícitas do mantenedor |
| GI-001 | Guerra Infinita / Firebase | P0 | NOT RUN | Regressões de token e spoofing |
| GI-002 | Guerra Infinita / PostgreSQL | P0 | BLOCKED | Diagnóstico isolado do 28P01 |
| GI-003 | Guerra Infinita / Android | P0 | NOT RUN | Instalação e aceitação no Galaxy S21 |
| GI-004 | Guerra Infinita / API hospedada | P1 | NOT RUN | Fluxo autenticado em HTTPS real |
| GI-005 | Guerra Infinita / expedições | P1 | NOT RUN | Sincronização autenticada e isolamento de dois usuários |
| GI-006 | Guerra Infinita / chips | P2 | NOT RUN | Modelo, persistência e regressões determinísticas |
| GI-007 | Guerra Infinita / conflito PR #22 | P0 | BLOCKED | Resolver dirty merge state e repetir testes |
| GI-008 | Guerra Infinita / PR #32 superado pela base | P0 | BLOCKED | Registrar disposição do PR sem mesclar a versão antiga |
| REA-001 | Dark War REA / Lua 5.5 | P1 | BLOCKED | Decoder estrutural customizado |
| REA-002 | Dark War REA / manifests | P1 | NOT RUN | Crosswalk LuaTxt vs LuaTxt_55 |
| PP-001 | Perifa Pro | P0 | FAIL | Integrar correções de senha/rate-limit e fechar JWT/CORS fail-closed |
| HF-001 | Hortifruti | P0 | FAIL | Capability do carrinho, transações e preservação de dados live |
| RH-001 | RH | P0 | FAIL | Corrigir escopo empresa_id e testar duas empresas sintéticas |
| HAM-001 | Hamburgueria | P1 | NOT RUN | RBAC de catálogo e taxas server-side |
| LC-001 | Leitor de Código | P1 | NOT RUN | Autenticação, totais e idempotência |
| SAL-001 | Salão da Lu | P1 | NOT RUN | Concorrência de agendamento, tenant e preço |
| EVT-001 | EventosRP | P1 | NOT RUN | OAuth, comissões, migração e pagamento em staging |
| ERB-001 | Estância Renascer | P2 | NOT RUN | Reserva, disponibilidade e anti-spam |
| PORT-001 | Portfólio | P2 | NOT RUN | Responsividade, acessibilidade e claims |
| CASA-001 | Casa Prática OFC | P2 | BLOCKED | Vincular repositório se existir |
| EMPTY-001 | Reboquei | P3 | BLOCKED | Repositório sem código |
| EMPTY-002 | Elegance | P3 | BLOCKED | Repositório sem código |
| UNKNOWN-001 | Memórias Amigos | P3 | BLOCKED | Definir propósito e critérios de aceite |
| BA-001 | Barbearia do Artur ativa | P2 | NOT RUN | Revalidar código e CI próprios |
| MC-001 | Me Conta protótipo | P3 | BLOCKED | Registrar propósito e critérios de aceite |
| CB-001 | Central Bridge | P2 | BLOCKED | Aguardar ambiente/orçamento autorizado para validação read-only |
| LEGACY-001 | Barbearia do Artur legado | P3 | NOT RUN | Testar separação do repositório ativo |

## Cobertura e limitações do snapshot

Este primeiro inventário consolida findings previamente registrados no próprio Conselho Central, issues/PRs do GitHub e notas de continuidade da REA. Findings de aplicações fora das frentes prioritárias ainda exigem revalidação direta do código e CI antes de qualquer correção. Por isso, esses itens começam em **NOT RUN** ou **BLOCKED**, nunca como PASS.

O inventário é deliberadamente conservador: não cria findings fictícios a partir de ausência de informação, não considera branch recente como prova de correção e não autoriza merge, deploy, publicação, exclusão, alteração de segredos/permissões, DNS, produção ou custos.

## Teste de regressão

`node scripts/test_project_findings.mjs` valida IDs estáveis, referência a projetos existentes, proveniência, status permitidos, presença de testes e gates, e impede que um finding seja marcado PASS sem commit final e regressão aprovada. O teste também verifica que REA e desenvolvimento de Guerra Infinita permaneçam em frentes distintas.

O CI do Conselho Central deve executar esse teste sempre que o registro, scripts ou workflow forem alterados.
