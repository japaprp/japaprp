---
name: testing-regression-quality
description: Planejar e executar testes unitários, integração, ponta a ponta, acessibilidade e regressão orientados a risco.
---

# Testing & Regression Quality

1. Descubra scripts e ferramentas reais em manifests, CI e documentação; não invente comandos.
2. Defina comportamento esperado e critérios de aceitação reproduzíveis.
3. Comece pelo teste mais estreito que reproduz o defeito; amplie conforme o risco.
4. Execute verificações baratas primeiro: lint/typecheck, teste focado, suíte relacionada e suíte completa quando viável.
5. Registre comando, resultado, duração e limitações. Nunca diga que todos os testes passaram se só executou parte.

## Camadas
- Unitários: regras, limites, normalização, cálculos, estados vazios e erros.
- Integração: banco de teste, migrations, contratos API, transações e serviços externos simulados.
- E2E: cadastro, login, permissões, CRUD e fluxos críticos de negócio.
- UI: loading, vazio, erro, sucesso, teclado, responsividade, foco, contraste e validação.
- Segurança: anônimo, papel insuficiente, tenant diferente e reenvio de requisição.
- Concorrência: submissões simultâneas, duplo clique, retries e duplicatas.

## Qualidade
- Testes determinísticos; controle relógio e aleatoriedade.
- Use dados sintéticos e limpeza segura.
- Evite mocks excessivos e testes frágeis acoplados à implementação.
- Quando viável, prove que o teste falha antes da correção e passa depois.

## Gate de entrega
Revise diff, efeitos colaterais, logs, lint/types/testes e rollback. Liste explicitamente testes não executados e o motivo.