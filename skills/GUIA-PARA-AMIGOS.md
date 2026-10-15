# Pacote de Skills para IA — guia para iniciantes

Bem-vindo! Este pacote contém instruções especializadas que ajudam ferramentas de IA compatíveis a trabalhar com mais organização. Pense em cada **skill** como um manual de trabalho: explica à IA como abordar determinado tipo de tarefa. Uma skill, sozinha, não instala programas, não dá acesso a contas e não garante que uma tarefa será concluída.

## 1. Como começar, mesmo sem entender de programação

1. Extraia o arquivo ZIP para uma pasta.
2. Abra a pasta e leia este guia.
3. Abra sua ferramenta de IA/editor (por exemplo, uma ferramenta compatível com arquivos `SKILL.md`). A forma de instalar skills depende da ferramenta; siga a documentação dela e não suponha que basta copiar a pasta para qualquer aplicativo.
4. Se não souber qual skill escolher, comece por **engineering-brain-router** ou **skill-onboarding-profiler**. A primeira direciona uma tarefa técnica; a segunda entrevista você em linguagem simples para entender seu trabalho, tecnologias e nível.
5. Descreva o objetivo, o que já existe e o que não pode ser alterado. Peça primeiro diagnóstico e plano; autorize mudanças só depois de entender o que será feito.
6. Ao final, peça resumo do que foi alterado e quais testes realmente foram executados.

### Prompt inicial para copiar

> Use a skill `skill-onboarding-profiler`. Sou iniciante e quero que você entenda com o que trabalho, o que pretendo construir, quais ferramentas uso e meu nível de experiência. Faça poucas perguntas de cada vez, explique os termos técnicos e não presuma tecnologias. Depois recomende só as skills necessárias, explique por que e me dê um passo a passo. Não peça senhas, tokens nem chaves secretas.

## 2. O que cada skill faz

As explicações abaixo são resumos em linguagem simples. Consulte o arquivo `SKILL.md` de cada pasta para ver as instruções completas.

| Skill | Para que serve | Quando usar |
|---|---|---|
| `engineering-brain-router` | É o orientador central: ajuda a escolher o método e as skills certas para uma tarefa. | Quando o pedido é amplo, confuso ou envolve várias áreas. |
| `skill-onboarding-profiler` | Faz perguntas simples para descobrir sua área, objetivo, experiência e tecnologias; depois recomenda as skills adequadas. | No primeiro contato, especialmente se você não é técnico ou não sabe a linguagem usada. |
| `repo-reverse-engineering` | Entende como um projeto existente está organizado antes de mexer nele. | Quando recebeu um código pronto ou não sabe onde uma função está. |
| `targeted-debugging-performance` | Investiga a causa provável de um erro ou lentidão sem sair mudando tudo. | Quando algo parou de funcionar, está lento ou dá erro. |
| `testing-regression-quality` | Ajuda a verificar se o sistema funciona e se uma correção não quebrou outra coisa. | Antes de entregar, publicar ou depois de corrigir um bug. |
| `code-review-minimal-change` | Revisa mudanças procurando problemas importantes e prefere correções pequenas. | Antes de aceitar mudanças de código ou revisar um pull request. |
| `api-engineering-contracts` | Organiza contratos de APIs e webhooks que seu sistema oferece ou precisa manter. | Quando está desenhando uma API própria ou mudando seu contrato. |
| `public-api-integration` | Ensina a consumir APIs públicas/de terceiros com autenticação, paginação, limites, retries e segurança. | Quando o app precisa usar dados ou recursos de outro serviço. |
| `application-deployment-hosting` | Ajuda a escolher onde hospedar e colocar site, API ou backend no ar, com domínio, HTTPS, custos e rollback. | Quando quer publicar um projeto e confirmar que está funcionando em produção. |
| `mobile-flutter-engineering` | Orienta a construção e manutenção de aplicativos móveis em Flutter/Dart. | Para apps Android/iOS que usam Flutter. |
| `ai-integration-evaluation` | Ajuda a integrar modelos de IA e avaliar respostas, qualidade, privacidade, custo e latência. | Quando seu produto usa IA, prompts, busca com documentos ou RAG. |
| `ai-token-budget` | Ajuda a economizar contexto, tokens e créditos da IA. | Quando a ferramenta consome muitos créditos ou lê arquivos demais. |
| `application-security-auth` | Trata login, permissões, sessões e separação dos dados de cada usuário. | Quando há contas, informações privadas ou diferentes tipos de usuário. |
| `infrastructure-database-engineering` | Orienta bancos de dados, migrações, monitoramento, recuperação e operações SSH seguras. | Quando precisa administrar infraestrutura, banco ou servidor remoto. |
| `spreadsheet-data-engineering` | Trabalha com Excel, CSV, fórmulas, transformação e conferência de dados. | Para limpar, combinar, validar ou gerar planilhas e relatórios. |
| `visual-asset-engineering` | Organiza, integra e otimiza imagens e outros assets visuais para sites e aplicativos. | Para preparar imagens, ícones, thumbnails e recursos responsivos. |
| `game-development-engineering` | Orienta engenharia de jogos, gameplay, engines, builds e desempenho. | Para desenvolver ou depurar um jogo; identifica a engine e sua versão antes de recomendar código. |
| `forms-crud-data-integrity` | Ajuda com cadastros, formulários, criação/edição/exclusão e consistência dos dados. | Para telas de cadastro, painel administrativo e operações sobre registros. |
| `premium-distinctive-web-design` | Ajuda a criar interfaces web claras, distintas e usáveis, considerando experiência e acessibilidade. | Para criar ou melhorar telas e sites. |
| `web-motion-design` | Planeja animações de interface com propósito, scroll storytelling, transições e microinterações, com foco em acessibilidade e desempenho. | Quando quer movimento refinado dentro da própria página, sem produzir um arquivo de vídeo. |
| `vercel-react-performance` | Trata desempenho específico de aplicações React/Next.js. | Quando o projeto realmente usa React/Next.js e existe uma necessidade de performance. |
| `supabase-postgres-specialist` | Foca em Supabase e PostgreSQL, incluindo políticas de acesso a linhas (RLS). | Quando o banco é Supabase/PostgreSQL; não copie comandos diretamente para MySQL. |
| `payments-billing-integrations` | Trata pagamentos, reembolsos, cashback, webhooks e conferência financeira. | Em checkout, cobranças ou saldos financeiros. Exige cuidado extra com ambiente de teste e transações reais. |
| `product-discovery-delivery` | Ajuda a transformar uma ideia em escopo, MVP, critérios de aceite e plano de lançamento. | Antes de começar um projeto ou decidir o que fazer primeiro. |
| `mcp-tooling-engineering` | Ajuda a criar ferramentas e integrações que agentes de IA podem usar via MCP. | Quando está construindo ferramentas para um agente, e não apenas usando um chat. |
| `external-workspace-data-tools` | Orienta o uso seguro de integrações de trabalho e extração de dados por ferramentas compatíveis. | Quando há uma integração real disponível e autorizada; não dá acesso automaticamente. |
| `content-commerce-distribution` | Planeja vídeos curtos, conteúdo comercial, links de afiliado e adaptação entre plataformas. | Para divulgar produtos e conteúdo em redes sociais. |
| `app-showreel-launch-film` | Planeja showreels, demonstrações de apps, filmes de lançamento e motion highlights com storyboard e revisão visual. | Para apresentar ou lançar um aplicativo em vídeo; combina com Remotion quando for renderizar por código. |
| `remotion-video-engineering` | Orienta vídeos criados por código com Remotion. | Para vídeos programáticos baseados em componentes/código. |
| `hyperframes-video-pipeline` | Ajuda com composição e fluxo de produção de vídeo usando HyperFrames. | Quando o projeto já usa HyperFrames. |
| `rea-assisted-analysis` | Apoia um fluxo específico de análise assistida chamado REA. | Quando seu trabalho já utiliza esse método. |
| `templates/PROJECT_CONTEXT.md` | É um formulário-modelo para registrar o contexto importante de um projeto. | Para evitar ter que explicar a arquitetura e decisões a cada sessão. |
| `tests/ROUTER_EVALS.md` | Contém cenários para conferir se o roteador recomenda as skills corretas. | Para quem mantém o pacote ou testa a seleção automática; não é uma skill de uso diário. |

## 3. Como escolher sem complicar

Use **uma skill principal** e, se necessário, até duas complementares. Mais skills não significa necessariamente resultado melhor.

Exemplos:
- “Não sei por que meu site dá erro”: comece com `targeted-debugging-performance`; use `repo-reverse-engineering` se for preciso entender o projeto primeiro.
- “Quero criar um app, mas só tenho a ideia”: comece com `product-discovery-delivery`; use o perfilador para descobrir requisitos e nível.
- “Quero login seguro”: use `application-security-auth`; acrescente testes quando for validar o fluxo.
- “Quero consumir uma API pública”: use `public-api-integration`; confirme documentação, autenticação, quotas, termos e tratamento de falhas.
- “Quero colocar meu site ou backend no ar”: use `application-deployment-hosting`; compare limites e custos atuais e valide URL, HTTPS e rota principal.
- “Quero aceitar pagamentos”: use `payments-billing-integrations` e peça um plano de testes antes de habilitar transações reais.
- “Quero melhorar um site”: use `premium-distinctive-web-design`; use a skill de React/Next.js somente se essa for a tecnologia do site.
- “Quero publicar vídeos de produtos”: use `content-commerce-distribution`; acrescente Remotion ou HyperFrames apenas se realmente usar essas ferramentas.
- “Preciso organizar ou conferir uma planilha”: use `spreadsheet-data-engineering` e preserve o original.
- “Quero preparar imagens para meu site/app”: use `visual-asset-engineering`; use uma ferramenta de imagem quando precisar criar ou editar a imagem em si.
- “Quero criar um jogo”: use `game-development-engineering` e confirme a engine e a plataforma antes de implementar.

## 4. O que informar à IA

Você não precisa saber todos os termos. Informe o que souber:
- **Trabalho/área:** o que faz no dia a dia.
- **Objetivo:** qual resultado quer alcançar.
- **Projeto atual:** ideia, site, app, planilha, automação ou código existente.
- **Ferramentas:** programas e serviços que já usa.
- **Tecnologias:** linguagem, framework e banco, se souber.
- **Limites:** orçamento, prazo, dispositivo, hospedagem e o que não pode ser interrompido.
- **Experiência:** iniciante, intermediário ou avançado.

Se não souber a linguagem, diga isso. Peça à IA que examine os arquivos disponíveis e apresente evidências. Não compartilhe senhas, chaves de API, tokens, documentos pessoais ou dados reais de clientes.

## 5. Limites importantes

- Skills são instruções; não substituem programas, contas, permissões ou conhecimentos específicos.
- O suporte depende do aplicativo de IA e de como ele carrega skills. Confirme o método de instalação na documentação da ferramenta.
- Uma skill não garante que testes foram executados. Peça o nome do comando, resultado e limitações; não aceite “testado” sem evidência.
- Faça cópia de segurança quando apropriado e peça diagnóstico antes de grandes mudanças.
- Não autorize publicação, exclusão, mudanças de produção ou transações financeiras sem entender o impacto.
- Este pacote é um conjunto de guias autorais. Não contém todos os agentes do projeto externo Agency Agents nem substitui as ferramentas originais.

Boa jornada! Comece pequeno, entenda o plano e evolua uma etapa de cada vez.
