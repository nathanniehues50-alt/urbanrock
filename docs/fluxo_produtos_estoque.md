## 1. Diagrama geral (estado atual)

```mermaid
flowchart LR
    Admin[Admin cadastra produto] --> ProdutoBD[Produto na base]

    ProdutoBD --> Home[View home]
    ProdutoBD --> Busca[View buscar_produtos]
    ProdutoBD --> Detalhe[View produto_detalhe]

    Home --> ClienteVe[Cliente visualiza produtos]
    Busca --> ClienteVe
    Detalhe --> ClienteVe

    ClienteVe --> AdicionaCarrinho[adicionar_ao_carrinho]
    AdicionaCarrinho --> SessaoCart[Sessao cart]

    SessaoCart --> CarrinhoView[carrinho e montar_carrinho]
    CarrinhoView --> Checkout[Fluxo checkout pedido]

    ProdutoBD -. estoque nao usado .-> EstoqueLogica[Sem logica de estoque]
