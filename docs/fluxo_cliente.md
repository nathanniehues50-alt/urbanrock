# Fluxo do Cliente – UrbanRock (Fluxo 100% baseado no seu código real)

```mermaid
flowchart LR

  %% =============================
  %% ROTAS PRINCIPAIS (urls reais)
  %% =============================

  INICIO((Usuário entra no site))
  HOME["Home<br/>(url: '/')"]
  BUSCA["Buscar produtos<br/>(url: '/buscar/')"]
  PRODUTO["Detalhe do Produto<br/>(url: '/produto/&lt;id&gt;/')"]

  %% CARRINHO
  CARRINHO["Carrinho<br/>(url: '/carrinho/')"]
  ADD["Adicionar ao carrinho<br/>(url: '/carrinho/adicionar/&lt;id&gt;/')"]
  ATUALIZAR["Atualizar carrinho<br/>(url: '/carrinho/atualizar/&lt;id&gt;/')"]
  REMOVER["Remover item<br/>(url: '/carrinho/remover/&lt;id&gt;/')"]
  CUPOM["Aplicar cupom<br/>(url: '/carrinho/cupom/')"]
  FRETE["Calcular frete<br/>(url: '/carrinho/frete/')"]

  %% LOGIN / CONTA
  CHECK_LOGIN{"Usuário está logado?"}
  LOGIN["Login<br/>(url: '/entrar/')"]
  REGISTRO["Registrar<br/>(url: '/usuario/registrar/')"]
  CONTA["Minha Conta<br/>(url: '/minha-conta/')"]

  %% ENDEREÇOS
  END_NOVO["Novo endereço<br/>(url: '/usuario/endereco/novo/')"]
  END_EDIT["Editar endereço<br/>(url: '/usuario/endereco/&lt;id&gt;/editar/')"]
  END_REMOVE["Remover endereço<br/>(url: '/usuario/endereco/&lt;id&gt;/remover/')"]
  END_PADRAO["Definir endereço padrão<br/>(url: '/usuario/endereco/&lt;id&gt;/definir-padrao/')"]

  ALTERAR_SENHA["Alterar senha<br/>(url: '/usuario/alterar-senha/')"]

  %% CHECKOUT / PEDIDO
  CHECKOUT["Checkout<br/>(url: '/checkout/')"]
  PAGAMENTO["Processar Pagamento<br/>(manualmente por enquanto)"]
  PEDIDO["Criar Pedido<br/>(model no app 'orders')"]
  CONFIRMACAO["Página de confirmação<br/>(url: '/confirmacao/&lt;pedido_id&gt;/')"]

  %% =============================
  %% FLUXO PRINCIPAL
  %% =============================

  INICIO --> HOME
  HOME --> BUSCA
  HOME --> PRODUTO

  BUSCA --> PRODUTO

  PRODUTO --> |Adicionar| ADD --> CARRINHO
  PRODUTO --> |Voltar| HOME

  CARRINHO --> ATUALIZAR --> CARRINHO
  CARRINHO --> REMOVER --> CARRINHO
  CARRINHO --> CUPOM --> CARRINHO
  CARRINHO --> FRETE --> CARRINHO

  %% CARRINHO → LOGIN → CHECKOUT
  CARRINHO --> CHECK_LOGIN
  CHECK_LOGIN --> |Não| LOGIN
  CHECK_LOGIN --> |Não tem conta| REGISTRO
  CHECK_LOGIN --> |Sim| CHECKOUT

  LOGIN --> CHECKOUT
  REGISTRO --> CHECKOUT

  CHECKOUT --> PAGAMENTO --> PEDIDO --> CONFIRMACAO


%% MINHA CONTA
HOME --> CONTA

CONTA["Minha Conta<br/>(url: '/minha-conta/')"]

CONTA --> END_NOVO
CONTA --> END_EDIT
CONTA --> END_REMOVE
CONTA --> END_PADRAO
CONTA --> ALTERAR_SENHA
