# Fluxo do Cliente – UrbanRock (Baseado no Projeto Real)

```mermaid
flowchart LR

  %% =============================
  %% NAVEGAÇÃO PRINCIPAL DO CLIENTE
  %% =============================

  INICIO((Usuário entra no site))
  HOME["Home (view: home)"]
  LISTA["Lista de Produtos / Busca"]
  PRODUTO["Detalhe do Produto (view: produto_detalhe)"]
  CARRINHO["Carrinho de compras"]
  
  CHECK_LOGIN{"Usuário está logado?"}
  LOGIN["Login (usuarios/login)"]
  REGISTRO["Cadastro (usuarios/registrar)"]
  
  CHECKOUT["Checkout (endereços + confirmação)"]
  FRETE["Cálculo de frete"]
  PAGAMENTO["Pagamento (Pix / manual por enquanto)"]
  
  STATUS_PAG{"Pagamento aprovado?"}
  PEDIDO["Pedido criado (model: Pedido)"]
  ERRO_PAG["Erro no pagamento / recusado"]
  
  OBRIGADO["Página de confirmação"]
  
  CONTA["Minha Conta (usuarios/minha_conta)"]
  HISTORICO["Meus pedidos"]
  VER_PEDIDO["Detalhe do pedido"]
  RASTREIO["Rastreamento (quando implementado)"]

  %% =============================
  %% CONEXÕES
  %% =============================
  INICIO --> HOME
  HOME --> LISTA
  HOME --> CONTA
  
  LISTA --> PRODUTO
  PRODUTO --> CARRINHO
  PRODUTO --> LISTA

  CARRINHO --> CHECK_LOGIN
  CHECK_LOGIN -->|Não| LOGIN
  CHECK_LOGIN -->|Não tem conta| REGISTRO
  LOGIN --> CHECKOUT
  REGISTRO --> CHECKOUT
  CHECK_LOGIN -->|Sim| CHECKOUT

  CHECKOUT --> FRETE --> PAGAMENTO
  PAGAMENTO --> STATUS_PAG
  
  STATUS_PAG -->|Aprovado| PEDIDO --> OBRIGADO
  STATUS_PAG -->|Erro| ERRO_PAG --> CARRINHO

  CONTA --> HISTORICO --> VER_PEDIDO --> RASTREIO
