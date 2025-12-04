# Mapa geral do sistema UrbanRock

Este documento mostra a **visão macro** do sistema.

Fluxos detalhados:

- [Fluxo do cliente](fluxo_cliente.md)
- [Fluxo de checkout e pedido](fluxo_checkout_pedido.md)
- [Fluxo de produtos e estoque](fluxo_produtos_estoque.md)
- [Fluxo de teste e deploy](fluxo_teste.md)

---

## 1. Mapa macro do sistema

```mermaid
flowchart LR
    %% --- AGRUPAMENTOS ---

    subgraph Cliente
        Visitante[Visitante]
        ClienteLogado[Cliente logado]
    end

    subgraph FrontSite
        Home[View home]
        Buscar[View buscar_produtos]
        ProdutoDet[View produto_detalhe]
        Carrinho[View carrinho]
        Checkout[View checkout]
        AreaCliente[View area do cliente]
    end

    subgraph Backend
        SessaoCart[Sessao cart]
        PedidoView[View criar pedido]
        Pagamento[Gateway pagamento]
    end

    subgraph Dados
        TabelaProduto[Model Produto]
        TabelaPedido[Model Pedido]
        TabelaItemPedido[Model ItemPedido]
        TabelaUsuario[Model Usuario]
    end

    subgraph Admin
        AdminPainel[Painel admin]
        Operacoes[Gerenciar produtos e pedidos]
    end

    subgraph Infra
        Dev[Dev local]
        GitHub[Repositorio GitHub]
        CI[Fluxo teste e deploy]
        Servidor[Servidor producao]
    end

    %% --- FLUXO CLIENTE NO SITE ---

    Visitante --> Home
    Visitante --> Buscar

    Home --> ProdutoDet
    Buscar --> ProdutoDet

    ProdutoDet --> Carrinho
    Carrinho --> Checkout

    %% Sessao de carrinho
    Carrinho --> SessaoCart
    Checkout --> SessaoCart

    %% Checkout e pedido
    Checkout --> Pagamento
    Pagamento --> PedidoView

    PedidoView --> TabelaPedido
    PedidoView --> TabelaItemPedido

    %% Relacao com produtos
    Home --> TabelaProduto
    Buscar --> TabelaProduto
    ProdutoDet --> TabelaProduto

    %% Area do cliente
    ClienteLogado --> AreaCliente
    AreaCliente --> TabelaPedido
    AreaCliente --> TabelaUsuario

    %% Admin / operacao
    AdminPainel --> Operacoes
    Operacoes --> TabelaProduto
    Operacoes --> TabelaPedido

    %% Infraestrutura e deploy
    Dev --> GitHub
    GitHub --> CI
    CI --> Servidor
    Servidor --> FrontSite
