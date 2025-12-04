# Fluxo do Cliente – UrbanRock (Alinhado ao Projeto Real)

```mermaid
flowchart LR

  %% =============================
  %% NAVEGAÇÃO PRINCIPAL DO CLIENTE
  %% =============================

  INICIO((Usuário entra no site))
  HOME["Home / Catálogo<br/>(url: '/', app: produtos)"]
  LISTA["Lista de Produtos / Busca<br/>(mesma home por enquanto)"]
  PRODUTO["Detalhe do Produto<br/>(url: '/produto/&lt;id&gt;/')"]
  CARRINHO["Carrinho de compras"]

  %% AUTENTICAÇÃO / CONTA
  CHECK_LOGIN{"Usuário está logado?"}
  LOGIN["Login<br/>(url: '/entrar/', name='login')"]
  REGISTRO["Cadastro<br/>(url: '/usuario/registrar/')"]
  CONTA["Minha Conta<br/>(url: '/minha-conta/', view: minha_conta)"]

  %% CHECKOUT / PEDIDO
  CHECKOUT["Checkout<br/>(endereços + confirmação)"]
  FRETE["Cálculo de frete<br/>(a implementar)"]
  PAGAMENTO["Pagamento<br/>(Pix / manual – a implementar)"]

  STATUS_PAG{"Pagamento aprovado?"}
  PEDIDO["Pedido criado<br/>(app: orders / model Pedido)"]
  ERRO_PAG["Pagamento recusado / erro"]

  OBRIGADO["Página de confirmação<br/>(pós-pedido)"]

  HISTORICO["Meus pedidos<br/>(lista de pedidos do usuário)"]
  VER_PEDIDO["Detalhe do pedido"]
  RASTREIO["Rastreamento<br/>(quando implementado)"]

  %% =============================
  %% FLUXO PRINCIPAL
  %% =============================

  INICIO --> HOME
  HOME --> LISTA
  HOME --> CONTA

  LISTA --> PRODUTO
  PRODUTO --> CARRINHO
  PRODUTO --> LISTA

  %% CARRINHO → CHECKOUT (COM LOGIN)
  CARRINHO --> CHECK_LOGIN
  CHECK_LOGIN --> |Não| LOGIN
  CHECK_LOGIN --> |Não tem conta| REGISTRO
  CHECK_LOGIN --> |Sim| CHECKOUT

  LOGIN --> CHECKOUT
  REGISTRO --> CHECKOUT

  %% CHECKOUT → FRETE → PAGAMENTO
  CHECKOUT --> FRETE --> PAGAMENTO
  PAGAMENTO --> STATUS_PAG

  STATUS_PAG --> |Aprovado| PEDIDO --> OBRIGADO
  STATUS_PAG --> |Erro| ERRO_PAG --> CARRINHO

  %% MINHA CONTA / HISTÓRICO / RASTREIO
  CONTA --> HISTORICO --> VER_PEDIDO --> RASTREIO
