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
## Gate de evidência e prontidão

- Compare comportamento implementado com os critérios de aceitação reais; não acrescente requisitos cosméticos que não foram combinados.
- Para interface, use screenshot para evidência visual e assertions/resultado persistido para evidência funcional. Screenshot de formulário preenchido não comprova envio nem persistência.
- Revise a implementação real e os resultados de teste; diferencie **PASS**, **FAIL** e **NÃO TESTADO**. Ausência de ferramenta/evidência é uma limitação de cobertura, não automaticamente um defeito do produto.
- Não atribua notas numéricas nem declare “pronto para produção” sem rubrica explícita, escopo testado e evidência proporcional ao risco.
- Relate apenas defeitos reproduzíveis ou discrepâncias demonstráveis. Registre gaps de cobertura e riscos remanescentes sem fabricar problemas.
- Use um gate mais rigoroso para autenticação, pagamentos, dados privados e release; não bloqueie por preferências visuais subjetivas.

## E2E com navegador real (Playwright)

Use Playwright quando o risco ou o pedido exigir comprovação do comportamento visível no navegador; não o torne obrigatório para toda alteração.

1. Confirme no projeto a instalação, versão, scripts, configuração e disponibilidade do navegador. Consulte a ajuda da versão instalada em vez de inventar comandos de CLI.
2. Inicie a aplicação no ambiente de teste documentado e espere por uma condição de prontidão verificável, não por um atraso arbitrário.
3. Use contas e dados sintéticos; isole o estado entre testes e limpe apenas dados criados pelo próprio teste.
4. Exercite o fluxo de ponta a ponta e faça assertions sobre URL, campos, mensagens, estado persistido e erros de console/rede relevantes. Um clique sem assertion não prova sucesso.
5. Capture screenshot/traces/logs quando ajudarem a diagnosticar ou demonstrar o resultado; proteja dados pessoais e segredos antes de anexar artefatos.
6. Separe testes locais/staging de produção. Não finalize compras, envie mensagens reais, altere dados reais nem execute ações irreversíveis sem autorização explícita.
7. Relate o comando realmente executado, ambiente, resultado e limitações. Se Playwright não estiver instalado ou o navegador não puder ser iniciado, marque o E2E como não executado; não simule evidência.
