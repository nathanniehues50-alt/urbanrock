# Mapa Geral do Sistema – UrbanRock

Este diagrama mostra toda a arquitetura operacional do UrbanRock:
fluxo do cliente, admin, fornecedores, backend, pagamentos e infraestrutura.

```mermaid
flowchart TB
  %% =============================
  %% FRONTEND (CLIENTE)
  %% =============================

  subgraph FRONTEND["🧑‍💻 Frontend / Cliente"]
    F_HOME[Home / Catálogo]
    F_PRODUTO[Página do Produto]
    F_CARRINHO[Carrinho]
    F_CHECKOUT[Checkout]
    F_CONTA[Minha Conta / Pedidos / Rastreio]
  end

  %% =============================
  %% BACKEND DJANGO
  %% =============================

  subgraph BACKEND["⚙️ Backend Django (Regras de Negócio)"]
    B_AUTH[Autenticação / Usuários]
    B_PEDIDOS[Pedidos e Status]
    B_PAGAMENTO[Processamento de Pagamento]
    B_ESTOQUE[Controle de Estoque]
    B_FRETE[Cálculo de Frete]
    B_RASTREIO[Lógica de Rastreamento]
  end

  %% =============================
  %% ADMIN
  %% =============================

  subgraph ADMIN["🏢 Painel Admin / Operação Interna"]
    A_DASH[Dashboard]
    A_PROD[Produtos / Categorias]
    A_PED[Pedidos / Atualização de Status]
    A_CLIENTES[Gestão de Clientes]
    A_MARKETING[Cupons e Promoções]
    A_REL[Relatórios]
  end

  %% =============================
  %% FORNECEDOR / LOGÍSTICA
  %% =============================

  subgraph FORNECEDOR["🚚 Fornecedores / Entregas"]
    FO_API[Fornecedor Integrado (API)]
    FO_MANUAL[Fornecedor Manual (Painel externo)]
    FO_ENVIO[Postagem / Transportadora]
  end

  %% =============================
  %% INFRA
  %% =============================

  subgraph INFRA["🛠️ Infraestrutura / Servidores"]
    S_NGINX[Nginx (HTTPS + Proxy Reverso)]
    S_GUNICORN[Gunicorn (WSGI)]
    S_DJANGO[Django App]
    S_DB[(Banco de Dados)]
    S_STATIC[Arquivos estáticos / mídia]
    S_EMAIL[Serviço de E-mail]
    S_ANALYTICS[Analytics / Métricas]
    S_FIREWALL[Firewall / Segurança]
    S_BACKUP[Backup Diário]
  end

  %% =============================
  %% CONEXÕES FRONTEND → BACKEND → INFRA
  %% =============================

  F_HOME --> F_PRODUTO --> F_CARRINHO --> F_CHECKOUT --> F_CONTA

  F_HOME --> S_NGINX
  F_PRODUTO --> S_NGINX
  F_CARRINHO --> S_NGINX
  F_CHECKOUT --> S_NGINX
  F_CONTA --> S_NGINX

  S_NGINX --> S_GUNICORN --> S_DJANGO

  %% Django liga para regras internas
  S_DJANGO --> BACKEND

  BACKEND --> S_DB
  BACKEND --> S_EMAIL
  BACKEND --> S_STATIC
  BACKEND --> S_ANALYTICS
  BACKEND --> S_FIREWALL
  S_DB --> S_BACKUP

  %% =============================
  %% BACKEND <-> ADMIN
  %% =============================

  A_DASH --> A_PROD --> B_ESTOQUE
  A_DASH --> A_PED --> B_PEDIDOS
  A_DASH --> A_CLIENTES --> B_AUTH
  A_MARKETING --> B_PEDIDOS
  A_REL --> S_DB

  %% =============================
  %% BACKEND <-> FORNECEDOR
  %% =============================

  B_PEDIDOS --> FO_API
  B_PEDIDOS --> FO_MANUAL
  FO_ENVIO --> B_RASTREIO
  B_RASTREIO --> F_CONTA

  %% PAGAMENTO / FRETE DIRETO
  F_CHECKOUT --> B_PAGAMENTO
  F_CHECKOUT --> B_FRETE
