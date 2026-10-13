---
name: forms-crud-data-integrity
description: Implementar e depurar cadastros e operações CRUD com validação, duplicidade, estados de formulário, integridade e concorrência.
---

# Forms, CRUD & Data Integrity

## Fluxo
1. Siga o dado da UI até endpoint/handler, regra de domínio, persistência e resposta.
2. Preserve contratos e convenções existentes; evite validações contraditórias.
3. Defina campos obrigatórios, normalização, limites, regras cruzadas, mensagens acessíveis e política de duplicidade.
4. Valide no cliente para UX e no servidor para segurança; imponha invariantes críticas no banco.
5. Diferencie erros de rede, validação, conflito, sessão expirada, timeout e falha inesperada.
6. Evite submissões duplicadas; use constraints e idempotência no servidor quando necessário.
7. Em edição, diferencie campo ausente, null e string vazia conforme o contrato.
8. Para exclusão, confirme impacto; não exclua dados reais sem autorização.
9. Atualize UI/cache após confirmação ou implemente optimistic update com rollback.
10. Teste create/read/update/delete, validação, duplicidade, permissões, concorrência e falha parcial.

## Casos comuns
- Normalização e unicidade de email/telefone conforme o domínio.
- Datas, fuso horário, dinheiro e separadores pt-BR.
- IDs de outra conta/empresa.
- Duplo clique, retry após timeout e refresh após POST.
- Campo desabilitado que não é enviado e cache antigo.
- Erros de banco expostos diretamente.
- Lista vazia confundida com falha e spinner que nunca termina.

## Conclusão
O fluxo funciona ponta a ponta, persiste corretamente, respeita autorização, dá feedback claro, não duplica registros e tem teste de regressão. Relate evidências e limitações.