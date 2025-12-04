flowchart TB

    %% Lado Esquerdo – Cliente
    subgraph Cliente
        Visitante[Visitante]
        ClienteLogado[Cliente logado]
    end

    %% Frontend
    subgraph Frontend
        Home[home]
        Buscar[buscar_produtos]
        ProdutoDet[produto_detalhe]
        Carrinho[carrinho]
        Checkout[checkout]
        AreaCliente[area do cliente]
    end

    %% Backend / Lógica
    subgraph Backend
        SessaoCart[Sessão cart]
        CriarPedido[View criar pedido]
        Pagamento[Gateway de pagamento]
    end

    %% Dados / Banco
    subgraph Dados
        ProdutoModel[Model Produto]
        PedidoModel[Model Pedido]
        ItemPedidoModel[Model ItemPedido]
        UsuarioModel[Model Usuario]
    end

    %% Admin
    subgraph Admin
        AdminPainel[Painel admin]
        AdminOps[Gerenciar produtos e pedidos]
    end

    %% Infra
    subgraph Infra
        GitHub[Repositório GitHub]
        Deploy[Fluxo de teste e deploy]
        Servidor[Servidor produção]
    end

    %% --------- FLUXO PRINCIPAL ---------

    Visitante --> Home
    Visitante --> Buscar
    Home --> ProdutoDet
    Buscar --> ProdutoDet
    ProdutoDet --> Carrinho
    Carrinho --> Checkout

    Checkout --> Pagamento
    Pagamento --> CriarPedido

    CriarPedido --> PedidoModel
    CriarPedido --> ItemPedidoModel

    Home --> ProdutoModel
    Buscar --> ProdutoModel
    ProdutoDet --> ProdutoModel

    ClienteLogado --> AreaCliente
    AreaCliente --> PedidoModel
    AreaCliente --> UsuarioModel

    AdminPainel --> AdminOps
    AdminOps --> ProdutoModel
    AdminOps --> PedidoModel

    GitHub --> Deploy
    Deploy --> Servidor
    Servidor --> Home
