flowchart LR

    %% CLIENTE
    subgraph Cliente
        C1[Checkout]
        C2[Pagamento no gateway]
        C3[Retorno ao site]
    end

    %% SITE
    subgraph Site[UrbanRock]
        CH[View checkout]
        PG_INIT[Iniciar pagamento]
        PG_RETURN[Retorno]
        PG_STATUS[Atualizar status]
    end

    %% GATEWAY
    subgraph Gateway
        GW_PAGE[Pagina de pagamento]
        GW_WEBHOOK[Webhook]
    end

    %% FLUXO PRINCIPAL
    C1 --> CH
    CH --> PG_INIT

    %% Criacao do pedido e transacao
    PG_INIT --> PG_STATUS
    PG_STATUS --> C2
    C2 --> GW_PAGE

    %% Cliente volta
    GW_PAGE --> PG_RETURN
    PG_RETURN --> C3

    %% Webhook confirma status real
    GW_PAGE --> GW_WEBHOOK
    GW_WEBHOOK --> PG_STATUS
