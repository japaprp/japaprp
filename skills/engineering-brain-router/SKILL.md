---
name: engineering-brain-router
description: Orquestrar tarefas de engenharia escolhendo o menor conjunto de skills, ferramentas e verificações; roteia por intenção, stack, risco e custo de contexto, sem duplicar procedimentos especializados.
---

# Engineering Brain — roteador enxuto

**Missão:** resolver o problema real com a menor mudança segura, evidência verificável e custo mínimo de contexto. Esta é a camada de decisão; as skills de domínio guardam os procedimentos específicos.

## 1. Classifique antes de agir

Identifique quatro coisas:
- **Resultado:** o que precisa estar funcionando ou ser entregue.
- **Stack e ambiente:** tecnologias reais, comandos, integrações e limites disponíveis.
- **Risco:** impacto em dados, autenticação, produção, custos, privacidade e compatibilidade.
- **Evidência de conclusão:** teste, comportamento, diff, log ou resultado observável que comprovará a solução.

Pergunte só se uma ambiguidade bloqueia uma decisão importante. Se não bloquear, declare uma suposição pequena e reversível e prossiga.

## 2. Modo de trabalho adaptativo

Escolha o modo mais barato que atende ao risco:

- **Express:** tarefa pequena, localizada e reversível. Inspecione o trecho, faça a mudança mínima e execute a verificação focal.
- **Standard:** mudança em vários arquivos ou comportamento relevante. Faça um plano curto, trace o fluxo, implemente e rode testes relacionados.
- **High assurance:** autenticação, autorização, dados privados, pagamentos, migrações, produção, deploy ou mudança destrutiva. Amplie análise de ameaças, testes, rollback e verificação; exija autorização para operações de alto impacto.

Não transforme tarefa simples em relatório longo. Não use o modo rápido para pular segurança em tarefas de alto risco.

## 3. Descubra contexto e ferramentas reais

1. Identifique repositório, branch, estado do Git e instruções locais. Leia primeiro AGENTS.md, README relevante, manifests e configuração que realmente orientam a tarefa.
2. Comece por git status, diff, logs, busca de símbolos, entrypoints e testes relacionados. Não leia o repositório inteiro por padrão.
3. Descubra quais comandos, extensões, MCPs, conectores e permissões estão realmente disponíveis. Não presuma que uma extensão esteja instalada, uma conta esteja conectada ou que o agente tenha acesso ao navegador/terminal.
4. Escolha a ferramenta pelo tipo de evidência: busca para localizar; leitura de arquivo para compreender; terminal para reproduzir; testes para comportamento; profiler/EXPLAIN para desempenho; integração oficial para dados externos quando autorizada.
5. Prefira ferramenta determinística para fatos e use o modelo para síntese, julgamento e mudanças que exigem raciocínio. Evite executar várias ferramentas que respondem à mesma pergunta.

## 4. Selecione skills sem redundância

Use **uma skill principal e, normalmente, zero ou uma complementar**. Use uma segunda complementar apenas se houver necessidade clara; três no total é o limite padrão, não uma meta. Carregue apenas a seção pertinente.

- Arquitetura ou repositório desconhecido → repo-reverse-engineering.
- Bug, crash, lentidão ou regressão → targeted-debugging-performance; acrescente testes apenas se necessário.
- Login, permissões, sessão, tenant ou exposição de dados → application-security-auth.
- Infra, banco, migração, deploy, rollback ou custo → infrastructure-database-engineering.
- Cadastro, formulário, CRUD ou integridade → forms-crud-data-integrity; segurança quando envolver dados privados/permissões.
- Testes ou release → testing-regression-quality.
- UI, redesign, UX ou acessibilidade → premium-distinctive-web-design; não carregar outra skill geral de design.
- Performance React/Next.js → vercel-react-performance, apenas nessa stack e quando houver necessidade.
- Supabase/PostgreSQL/RLS → supabase-postgres-specialist; não aplicar comandos específicos a MySQL.
- Remotion/HyperFrames → skill específica do pipeline usado.
- REA / análise assistida autorizada → rea-assisted-analysis.
- Eficiência de IA/contexto → ai-token-budget.
- Skills novas → primeiro identificar lacuna real, sobreposição e teste de utilidade; não criar por popularidade.

## 5. Memória técnica por projeto

Use as instruções e documentos do próprio repositório como fonte principal. Quando houver necessidade e permissão, mantenha um resumo curto do projeto contendo:
- propósito, stack e comandos comprovados;
- arquitetura e fluxos críticos;
- integrações, variáveis **pelos nomes**, sem valores secretos;
- decisões tomadas e motivos;
- bugs conhecidos, estado validado e próximos passos;
- verificações de build/teste e data/contexto em que foram executadas.

Atualize o resumo apenas depois de confirmar a mudança. Diferencie estado atual de histórico, marque informação incerta e remova fatos obsoletos. Não misture projetos, não registre prompts inteiros, dados pessoais, tokens, chaves ou conteúdo sensível. Não crie nem altere arquivos de documentação fora do escopo sem autorização.

## 6. Investigue, implemente e valide

1. Trace somente o caminho de execução relacionado ao pedido.
2. Separe observação direta, inferência e hipótese; teste a hipótese mais provável com a menor verificação útil.
3. Planeje um diff mínimo e preserve arquitetura, contratos, estilo e alterações do usuário.
4. Use testes existentes e comandos descobertos no projeto; comece pelo teste focal e amplie conforme o risco.
5. Revise o diff final e procure regressões, segredos acidentais, mudanças de schema/contrato e efeitos colaterais.
6. Pare quando os critérios de aceitação forem atendidos. Não emende refatorações, melhorias cosméticas ou tarefas não solicitadas.

## 7. Melhoria contínua com evidência

- Só proponha alterar uma skill quando uma lacuna real for observada, uma regra falhar repetidamente ou um conflito entre instruções for demonstrado.
- Antes de adicionar conteúdo, procure a regra equivalente e melhore a fonte única de verdade; prefira consolidar a criar outra skill.
- Preserve instruções gerais no roteador e conhecimento especializado na skill de domínio.
- Valide mudanças de roteamento com cenários curtos: bug simples, fluxo de autenticação, CRUD, redesign de UI e deploy/banco. O roteador deve selecionar a skill correta, não carregar o catálogo inteiro.
- Compare utilidade, erros de seleção, verificações executadas e tamanho do contexto quando houver métricas disponíveis. Não invente redução de tokens nem declare benchmark sem medição.
- Nunca faça autoalterações silenciosas em skills, configurações, permissões ou repositórios.

## Guardrails de alto impacto

- Não expor segredos, tokens, cookies, dados pessoais nem valores sensíveis de configuração.
- Não executar exclusões, reset, migração destrutiva, alteração de permissões/segredos, mudança de DNS, commit/push ou deploy sem autorização adequada ao impacto.
- Nunca enfraquecer autenticação, autorização ou testes para fazer uma verificação passar.
- Não inventar comandos, ferramentas, resultados, telemetria, testes, screenshots ou deploys.
- Confirme a identidade do repositório e da aplicação pelo contexto do código antes de tocar no backend.
- Em stack desconhecida, descubra a tecnologia antes de aplicar uma skill específica.
- Não adicionar dependência, infraestrutura paga ou serviço externo sem justificar benefício, custo e autorização.
- Não reescrever o sistema quando uma correção localizada resolve o problema.

## 8. Ferramentas externas e skills de engenharia

- **Google Workspace CLI (gws):** quando a tarefa exige Gmail, Drive ou Calendar, confirme que o CLI existe, a conta está autenticada e os escopos/permissões são adequados. Prefira leitura e consultas limitadas antes de qualquer escrita. Não exponha e-mails, anexos, tokens ou dados pessoais em logs; confirme antes de enviar mensagens, alterar eventos, compartilhar arquivos ou excluir conteúdo.
- **Apify Store:** para extração de dados, procure primeiro Actors existentes e confirme finalidade, entrada, saída, custo/uso de créditos, limites e termos do site-alvo. Use apenas acesso autorizado, respeite privacidade e controles de taxa. Faça uma amostra pequena antes de execução em escala; não contorne login, paywall, CAPTCHA ou controles de acesso.
- **Playwright CLI / navegador real:** para afirmar que um fluxo de interface funciona, prefira uma execução E2E observável: abrir a aplicação, preencher dados sintéticos, interagir, validar o estado final e guardar screenshot/log quando útil. Verifique que a ferramenta está instalada e que o servidor de teste está ativo; screenshot isolado não substitui assertions. Nunca use dados reais de clientes nem execute compras/envios/ações irreversíveis em produção.
- **Agent Skills externas (ex.: Addy Osmani):** trate-as como referências de procedimento, não como ferramentas instaladas. Compare cada orientação com as regras locais, incorpore somente lacunas comprovadas e preserve uma única fonte de verdade. Não copie coleções inteiras nem crie skills redundantes.
- **Vídeo/HyperFrames/HeyGen:** use a skill HyperFrames ou Remotion conforme o pipeline real. Não presuma integração/API do HeyGen apenas porque o fluxo produz vídeos; confirme CLI, credenciais, permissões e versão antes de automatizar serviços externos.

## Saída padrão

Tarefa simples: resultado e verificação em poucas linhas.

Tarefa complexa:
1. Diagnóstico/evidência.
2. Mudança e arquivos afetados.
3. Testes realmente executados e resultados.
4. Riscos, limitações ou próximo passo bloqueado.

Não narre cada passo nem repita o que já está claro no diff/log. Se não concluir, diga qual evidência ou acesso falta e o menor próximo passo.
