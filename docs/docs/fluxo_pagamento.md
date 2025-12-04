# Fluxo de pagamento – UrbanRock

Objetivo: descrever como o site UrbanRock vai integrar com
um gateway de pagamento (Mercado Pago, PagBank, Stripe, etc.).

A ideia e sempre a mesma:

- Checkout cria um `Pedido` com status "aguardando_pagamento"
- Sistema cria um registro de `TransacaoPagamento`
- Cliente e redirecionado para o gateway
- Gateway chama:
  - URL de retorno (cliente volta para o site)
  - URL de notificacao (webhook, confirmacao real)
- Sistema atualiza `Pedido` e `TransacaoPagamento` conforme o status.

---

## 1. Diagrama geral do fluxo

```mermaid
flowchart LR

    subgraph Cliente
        C1[Cliente no checkout]
        C2[Cliente na tela do gateway]
        C3[Cliente volta para o site]
    end

    subgraph Site[UrbanRock]
        CH[View checkout]
        PG_INIT[View iniciar_pagamento]
        PG_RETURN[View retorno_pagamento]
        PG_STATUS[Atualiza Pedido e Transacao]
    end

    subgraph Gateway[Gateway de pagamento]
        GW_FORM[Pagina de pagamento]
        GW_WEBHOOK[Webhook -> callback]
    end

    %% Sequencia principal

    C1 --> CH
    CH --> PG_INIT

    %% Site cria pedido e transacao
    PG_INIT -->|Cria Pedido (aguardando_pagamento)| PG_STATUS
    PG_STATUS -->|Redireciona para URL do gateway| C2
    C2 --> GW_FORM

    %% Cliente paga ou cancela no gateway
    GW_FORM -->|Paga ou cancela| GW_WEBHOOK
    GW_FORM -->|Redirect de volta| PG_RETURN
    PG_RETURN --> C3

    %% Webhook informa status real
    GW_WEBHOOK -->|POST notificacao| PG_STATUS
    PG_STATUS -->|Atualiza Pedido: pago, cancelado, expirado| Site

