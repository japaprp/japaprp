---
name: api-engineering-contracts
description: Projetar, integrar e testar APIs com contratos claros, compatibilidade, autenticação, resiliência e segurança de integrações.
---

# API Engineering & Contract Governance

Use para criar ou alterar APIs REST/GraphQL/webhooks, integrar serviços externos ou definir contratos entre frontend, backend e serviços. Descubra primeiro a stack e os padrões já usados no projeto.

## Contrato antes da implementação
1. Identifique consumidores, casos de uso, dados expostos, autenticação, autorização e impacto de falha.
2. Para APIs públicas ou com vários consumidores, mantenha contrato legível por máquina (OpenAPI, schema GraphQL, AsyncAPI ou equivalente) como referência revisável.
3. Defina nomes, tipos, formatos de data/hora, IDs, paginação, filtros, ordenação, envelope de erro e códigos HTTP consistentes.
4. Separe campos obrigatórios, opcionais, anuláveis e ausentes. Não altere o significado de um campo sem avaliar compatibilidade.
5. Trate remoção, renomeação ou mudança semântica como potencial breaking change; defina versão, migração e depreciação quando necessário.
6. Não adicione versionamento, gateway, SDK ou microserviços por padrão se a escala e os consumidores não justificarem a complexidade.

## Segurança e integridade
- Autenticação não substitui autorização. Verifique permissões e escopo de tenant no servidor para cada recurso.
- Valide entrada no limite de confiança e normalize os dados de forma consistente; não confie no cliente nem em payloads externos.
- Aplique limites de tamanho, rate limiting, paginação limitada, timeouts e limites de concorrência proporcionais ao uso.
- Não exponha stack traces, tokens, dados privados ou detalhes internos em respostas e logs.
- Para operações repetíveis que causam efeitos colaterais, defina idempotência e tratamento de concorrência.
- Para webhooks: valide assinatura/origem segundo o provedor, deduplique eventos, persista o recebimento com segurança, aceite repetição e ordem variável, e processe de modo recuperável.
- Para chamadas externas, defina timeout, retry com backoff e jitter, classificação de erros e fallback. Não repita automaticamente operações não idempotentes sem proteção.

## Testes e compatibilidade
1. Teste happy path, validação, autenticação/autorização, limites, paginação, erros, timeout e indisponibilidade do provedor.
2. Use testes de contrato e integração para confirmar que cliente, servidor e documentação concordam.
3. Teste chamadas duplicadas, eventos repetidos, payloads inválidos e mudanças de schema quando relevantes.
4. Verifique se um HTTP 200 contém resposta válida e semanticamente correta; status isolado não prova sucesso.
5. Use dados sintéticos e ambientes de teste. Não faça carga ou mutações em produção sem autorização.
6. Execute testes realmente disponíveis e relate os não executados sem inventar resultados.

## Entrega
Registre endpoints/contratos afetados, decisões de compatibilidade, autenticação e autorização relevantes, testes executados, riscos restantes e plano de migração se houver breaking change. Prefira a menor solução que mantenha o contrato correto e seguro.
