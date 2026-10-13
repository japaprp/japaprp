---
name: application-security-auth
description: Revisar autenticação, autorização, sessões, cadastro, isolamento multi-tenant, segredos e vulnerabilidades web.
---

# Application Security & Identity

## Método
1. Identifique framework, middleware, rotas, modelos, políticas, provedores de auth e pontos de entrada.
2. Modele ativos, papéis, limites de confiança e dados sensíveis; verifique primeiro os fluxos afetados.
3. Valide autenticação e autorização no servidor para cada endpoint. Ocultar botão no frontend não é controle de acesso.
4. Teste IDOR/BOLA: trocar IDs de usuário, empresa, arquivo, reserva ou registro não pode permitir acesso cruzado.
5. Verifique isolamento multi-tenant em consultas, jobs, exports, cache, storage e realtime.
6. Revise validação server-side, SQL injection, XSS, CSRF conforme arquitetura, SSRF, uploads, rate limits, CORS, headers e logs.
7. Revise hash de senhas, expiração/revogação de sessão, cookies HttpOnly/Secure/SameSite quando aplicáveis, reset de senha e verificação de email.
8. Procure segredos em código, histórico, logs e artefatos sem expor valores. Recomende rotação quando houver vazamento.
9. Priorize por impacto e explorabilidade. Teste em ambiente autorizado, sem explorar sistemas de terceiros.

## Cadastro e autenticação
- Validar normalização, formato e unicidade no servidor e no banco.
- Evitar duplicidade sob concorrência com constraint única e tratamento idempotente.
- Cobrir signup, login, logout, sessão expirada, recuperação, troca de senha, conta desativada e permissões insuficientes.
- Não revelar se uma conta existe em fluxos de recuperação quando isso cria risco.
- Negar por padrão e aplicar menor privilégio. Não enfraquecer controles para fazer testes passar.
- Não alterar produção, permissões, segredos ou dados reais sem autorização.

## Entrega
Achado, evidência/arquivo/linha, severidade, impacto, correção mínima e teste de regressão. Diferencie falha confirmada de risco potencial.