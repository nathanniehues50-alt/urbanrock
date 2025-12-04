# Fluxo de Produtos & Estoque – UrbanRock

Este documento descreve como funciona **hoje** o ciclo de vida de um produto
no sistema UrbanRock, com base no código real:

- Modelo `Produto` e relacionados
- Como o produto aparece no site
- Como entra no carrinho
- O que acontece (ou não) com o estoque

> ⚠ Importante: no estado atual do sistema, o campo `estoque`
> **ainda não é usado na lógica do carrinho/pedido**.  
> Ele existe no banco, mas não há baixa/validação.

---

## 1. Diagrama geral (estado atual)

```mermaid
flowchart LR
    Admin[Admin cadastra Produto (Django Admin)] --> ProdutoBD[(Tabela Produto)]

    ProdutoBD --> Home[View home()]
    ProdutoBD --> Busca[View buscar_produtos()]
    ProdutoBD --> Detalhe[View produto_detalhe()]

    Home --> ClienteVe[Cliente vê produtos]
    Busca --> ClienteVe
    Detalhe --> ClienteVe

    ClienteVe --> AdicionaCarrinho[adicionar_ao_carrinho()]
    AdicionaCarrinho --> SessaoCart["Sessão: dict cart"]

    SessaoCart --> CarrinhoView[carrinho() / montar_carrinho()]
    CarrinhoView --> Checkout[Fluxo de checkout/pedido (docs/fluxo_checkout_pedido.md)]

    %% Estoque (hoje)
    ProdutoBD -. campo estoque NÃO usado .-> EstoqueLogica[Sem lógica de estoque ainda]
