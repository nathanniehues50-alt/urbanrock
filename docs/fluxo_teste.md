# Fluxograma de Teste – UrbanRock

```mermaid
flowchart LR
  INICIO((Usuário entra))
  HOME[Home]
  PRODUTO[Página do Produto]
  CARRINHO[Carrinho]
  CHECKOUT[Checkout]

  INICIO --> HOME
  HOME --> PRODUTO
  PRODUTO --> CARRINHO
  CARRINHO --> CHECKOUT
