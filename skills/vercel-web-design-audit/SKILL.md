---
name: vercel-web-design-audit
description: Auditar interfaces web para acessibilidade, UX, formulários, estados, navegação, responsividade e performance visual.
---

# Web Design & Interface Audit

**Referência pública:** [vercel-labs/agent-skills — web-design-guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines). Use a versão oficial para checklist completo e atualizado; esta adaptação orienta a auditoria no projeto.

## Auditoria por risco
1. Inspecione primeiro a página, componente ou fluxo indicado. Não audite todo o site se o escopo é um componente.
2. Verifique semântica HTML, nomes acessíveis, labels, teclado, foco visível, ordem de tabulação e contraste.
3. Confira formulários: autocomplete, validação, mensagens junto ao campo, preservação de dados e prevenção de submissão duplicada.
4. Confira estados de loading, vazio, erro, sucesso, offline e permissão negada.
5. Verifique responsividade real, alvos de toque, menus, modais, scroll e teclado virtual em telas pequenas.
6. Respeite prefers-reduced-motion; evite animações que bloqueiem interação ou causem enjoo.
7. Confira imagens com dimensões, alt text, lazy loading quando apropriado e formatos eficientes.
8. Garanta que navegação/estado compartilhável reflita URL quando necessário; trate idioma, datas, moeda e números de acordo com locale.
9. Verifique console, requests, layout shifts e tamanho de bundle se houver ferramentas.
10. Classifique achados por severidade e esforço; corrija primeiro bloqueadores, falhas de acesso e erros de formulário.

## Formato do relatório
Achado | evidência/elemento | impacto para usuário | severidade | correção mínima | como validar.

Não declare conformidade WCAG total a partir de uma inspeção superficial; identifique o escopo e as verificações efetivamente realizadas.