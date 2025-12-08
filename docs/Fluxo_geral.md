flowchart LR
    %% ============================
    %% NÍVEL ALTO: NAVEGAÇÃO GERAL
    %% ============================

    A[Visitante] --> B[Home<br/>view: produtos.home<br/>url: /]
    A --> R[Registrar<br/>view: registrar<br/>url: /registrar]
    A --> L[Login<br/>Django auth]

    B --> S[Buscar produtos<br/>view: buscar_produtos]
    B --> PD[Detalhe do produto<br/>view: produto_detalhe]
    PD --> CARR_ADD[Adicionar ao carrinho<br/>view: adicionar_ao_carrinho]

    CARR_ADD --> CARR[Carrinho<br/>view: carrinho]

    CARR -->|Continuar comprando| B
    CARR -->|Ir para checkout| CHK[Checkout<br/>view: orders.checkout]

    %% ÁREA MINHA CONTA
    L --> MC[Minha conta<br/>view: minha_conta<br/>url: /minha-conta]
    R --> MC
    MC --> PESSOAL[Dados pessoais<br/>UsuarioForm + PerfilForm]
    MC --> END_LIST[Listar endereços<br/>usuario.enderecos]
    MC --> END_NEW[+ Novo endereço<br/>view: endereco_novo]
    END_LIST --> END_EDIT[Editar endereço<br/>view: endereco_editar]
    END_LIST --> END_DEL[Remover endereço<br/>view: endereco_remover]
    END_LIST --> END_PADRAO[Marcar como padrão<br/>view: endereco_definir_padrao]

    %% PEDIDOS
    CHK --> CONF[Confirmar pedido<br/>cria Pedido + ItemPedido]
    CONF --> PCONF[Página de confirmação<br/>view: orders.confirmacao]
    PCONF --> PAG_BTN[Ir para pagamento<br/>view: orders.iniciar_pagamento]
    PAG_BTN --> PG_RETORNO[Retorno pagamento<br/>view: orders.retorno_pagamento]

    %% PAGAMENTO EXTERNO
    PAG_BTN --> GATEWAY[(Gateway Externo<br/>ex: Mercado Pago)]
    GATEWAY --> WEBHOOK[Webhook<br/>view: orders.webhook_gateway]
    WEBHOOK --> ATUALIZA_PEDIDO[Atualiza status Pedido<br/>pago/cancelado/pendente]
    ATUALIZA_PEDIDO --> PG_RETORNO
