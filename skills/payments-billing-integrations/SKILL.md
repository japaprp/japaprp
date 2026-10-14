---
name: payments-billing-integrations
description: Integrar pagamentos, reembolsos e webhooks com idempotência, estados consistentes, reconciliação financeira e segurança.
---

# Payments & Billing Integrations

Use quando houver cobrança, checkout, assinatura, reembolso, split/repasse, carteira, cashback ou integração com PSP como Mercado Pago. Consulte a documentação atual do provedor e confirme o modo sandbox/produção antes de usar endpoints ou estados específicos.

## Fluxo financeiro correto
1. Modele o ciclo de vida explícito: criado, pendente, aprovado, recusado, cancelado, estornado e demais estados documentados pelo provedor.
2. Não considere retorno do navegador, query string ou tela de sucesso como prova de pagamento. Confirme o estado no servidor com o provedor e/ou webhook autenticado.
3. Use idempotência baseada na operação de negócio para evitar cobranças, reembolsos ou repasses duplicados em retry.
4. Armazene valores monetários em unidades inteiras mínimas (centavos quando aplicável) junto à moeda ISO 4217; nunca use ponto flutuante para cálculos financeiros.
5. Registre IDs externos, status, timestamps e transições auditáveis sem armazenar dados de cartão.
6. Para cashback, comissão, split ou saldo, defina origem do valor, regra de arredondamento, momento de liberação, estorno e reconciliação antes de implementar.

## Webhooks e processamento
- Verifique assinatura/autenticidade conforme a documentação do PSP.
- Persista eventos verificados antes de confirmar recebimento quando o fluxo exigir processamento assíncrono durável.
- Deduplique por identificador de evento/operação e tolere entregas repetidas ou fora de ordem.
- Faça o processamento recuperável e idempotente; mantenha falhas visíveis para reprocessamento seguro.
- Reconcilie periodicamente pedidos/transações locais com o estado do provedor e investigue divergências.
- Nunca confie apenas no frontend para preço, moeda, desconto, comissão, destinatário ou status.

## Segurança e testes
- Não receba nem armazene número completo de cartão, CVV ou dados sensíveis de autenticação; prefira checkout hospedado/tokenização oficial.
- Segredos ficam no backend e nunca em app móvel, frontend, logs ou repositório.
- Teste sucesso, recusa, autenticação adicional quando aplicável, timeout, webhook duplicado, evento atrasado, reembolso e divergência de valores no sandbox.
- Use contas e transações de teste; não execute cobrança real, reembolso real, alteração de payout ou mudança de produção sem autorização explícita.
- Verifique permissões, assinatura, rate limits, logs sem dados sensíveis e proteção contra IDOR/BOLA em pedidos e pagamentos.

## Entrega
Documente estados e transições, estratégia de idempotência, validação de webhook, reconciliação, testes realizados e limitações. Nunca declare o fluxo pronto só porque o checkout visual funciona.
