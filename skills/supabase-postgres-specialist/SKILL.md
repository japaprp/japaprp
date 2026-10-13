---
name: supabase-postgres-specialist
description: Aplicar práticas especializadas de PostgreSQL/Supabase para schema, RLS, migrations, índices, conexões e segurança. Use apenas quando o projeto usar Supabase/PostgreSQL.
---

# Supabase & PostgreSQL Specialist

**Referência pública:** [supabase/agent-skills — supabase-postgres-best-practices](https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices). Skill própria resumida; consulte o repositório original para regras detalhadas e atualizadas.

## Gatilho
Não aplicar a MySQL/MariaDB ou a outro provedor sem adaptar a sintaxe e as garantias. Confirme a stack e a versão antes de agir.

## Checklist
1. Leia migrations, schema e políticas existentes antes de mudar tabelas.
2. Para tabelas expostas pela API, confirme RLS habilitada e políticas alinhadas ao modelo de acesso; não copie a mesma política para todas as tabelas sem entender o domínio.
3. Teste leitura e escrita com usuários e papéis diferentes, inclusive tentativa de acessar linhas de outro usuário/tenant.
4. Nunca use metadados editáveis pelo usuário como fonte confiável de autorização.
5. Nunca exponha service-role/segredos no frontend ou em variáveis públicas.
6. Revise permissões de views e funções privilegiadas; não use SECURITY DEFINER como atalho para resolver permissão.
7. Para lentidão, inspecione EXPLAIN/ANALYZE, índices, cardinalidade, consultas repetidas e tamanho do resultado antes de alterar schema.
8. Revise pool/conexões, locks, transações, migrations e rollback.
9. Teste policies e migrations com dados sintéticos; não altere produção sem plano e autorização.
10. Consulte documentação e changelog atuais para comportamentos específicos do Supabase; não confie apenas em memória do modelo.

## Entrega
Descreva policy/schema afetado, cenário de acesso, evidência, teste executado, rollback e limitações. Diferencie validação feita de suposição.