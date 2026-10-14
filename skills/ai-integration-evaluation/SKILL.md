---
name: ai-integration-evaluation
description: Integrar APIs e modelos de IA em aplicações com avaliação, saídas estruturadas, proteção contra prompt injection, privacidade, limites e controle de custo.
---

# AI Integration & Evaluation

Use para integrar APIs de modelos, recursos generativos, classificação, extração, transcrição, embeddings ou RAG. Confirme o provedor, SDK, versão e documentação atual antes de usar parâmetros ou endpoints específicos.

## Defina o problema antes do modelo
1. Identifique tarefa, usuários, impacto de erro, latência aceitável, orçamento e dados que podem sair do ambiente.
2. Estabeleça baseline e critérios de sucesso mensuráveis; não escolha modelo maior ou RAG por padrão.
3. Compare solução determinística, modelo pequeno, modelo mais capaz e recuperação de contexto quando isso puder mudar a decisão.
4. Defina formato de saída e schema antes de escrever prompts. Use saída estruturada e validação de schema quando suportadas.
5. Versione prompts, modelos/configurações relevantes e datasets de avaliação para permitir regressões reproduzíveis.

## Integração resiliente
- Guarde chaves no servidor/secret manager ou configuração segura; nunca em frontend, app móvel, repositório, screenshots ou logs.
- Defina timeouts, limites de tamanho, concorrência, rate limits, retry com backoff/jitter e tratamento de 429/5xx.
- Use idempotência ou deduplicação para tarefas que geram custos, enviam mensagens ou alteram dados.
- Defina limites de tokens/custo por tarefa e usuário, métricas de consumo e fallback seguro quando a API falhar.
- Trate texto, documentos, páginas, imagens e saídas do modelo como dados não confiáveis, não como instruções de sistema.
- Minimize dados pessoais; confirme retenção, consentimento, localização e políticas do provedor antes de enviar dados sensíveis.
- Não execute comandos, publique conteúdo ou altere dados externos com base apenas na saída de um modelo sem validação e autorização apropriadas.

## Avaliação antes de produção
1. Crie casos para caminho normal, entradas ambíguas, limites, formato inválido, prompt injection e falha do provedor.
2. Avalie qualidade com rubrica clara: correção, completude, aderência ao schema, latência, custo e risco.
3. Use exemplos representativos e dados sintéticos quando possível; separe teste de desenvolvimento de avaliação final.
4. Para RAG, avalie retrieval e resposta separadamente: relevância/recall do contexto, fidelidade às fontes, citações e comportamento quando não há evidência.
5. Compare mudanças de prompt/modelo com uma baseline antes de promover; não use um número arbitrário de casos como garantia universal.
6. Monitore erros, latência, consumo, recusas, feedback e drift sem registrar conteúdo sensível desnecessariamente.

## Limites e entrega
Não prometa determinismo quando a API é probabilística. Marque conteúdo não verificado, permita revisão humana para decisões de alto impacto e forneça caminho de fallback. Informe provedor/versão confirmados, schema, estratégia de avaliação, testes executados, custo esperado se medido e limitações conhecidas.
