# Fluxo de Checkout e Criação de Pedido – UrbanRock (alinhado ao código real)

```mermaid
flowchart LR

  %% ENTRADA: CARRINHO → CHECKOUT
  CARRINHO["Carrinho<br/>(url: '/carrinho/')"]
  BTN_CHECKOUT["Botão 'Finalizar compra'"]
  CHECKOUT_GET["GET /checkout/<br/>(orders.checkout)"]

  %% MONTAR CONTEXTO
  MONTAR_CARRINHO["montar_carrinho(request)<br/>pega itens, subtotal, cupom, frete, total"]
  VERIFICA_VAZIO{"Carrinho está vazio?"}
  REDIR_CARRINHO["redirect('carrinho')"]

  CARREGA_END["Endereços do usuário<br/>(Endereco.objects.filter(usuario))"]

  %% TELA CHECKOUT
  RENDER_CHECKOUT["Renderiza 'orders/checkout.html'<br/>com enderecos, itens, subtotal, frete, total, erro_endereco"]

  %% POST: CONFIRMAR
  CHECKOUT_POST["POST /checkout/"]
  SEM_ENDERECO{"Usuário tem endereços cadastrados?"}
  REDIR_NOVO_END["redirect('endereco_novo')"]

  VALIDA_END{"endereco_id válido?"}
  ERRO_END["erro_endereco = 'Selecione um endereço válido'" ]

  CRIA_PEDIDO["Cria Pedido<br/>(Pedido.objects.create)"]
  CRIA_ITENS["Cria ItemPedido para cada item<br/>do carrinho atual"]
  LIMPA_SESSAO["Limpa 'cart', 'cupom', 'frete' da sessão"]
  REDIR_CONF["redirect('pedido_confirmacao', pedido_id)"]

  CONF_GET["GET /confirmacao/&lt;pedido_id&gt;/<br/>(orders.confirmacao)"]
  MOSTRA_CONF["Renderiza 'orders/confirmacao.html'<br/>(dados do pedido)"]

  %% FLUXO

  CARRINHO --> BTN_CHECKOUT --> CHECKOUT_GET
  CHECKOUT_GET --> MONTAR_CARRINHO --> VERIFICA_VAZIO
  VERIFICA_VAZIO --> |Sim| REDIR_CARRINHO
  VERIFICA_VAZIO --> |Não| CARREGA_END --> RENDER_CHECKOUT

  RENDER_CHECKOUT --> CHECKOUT_POST
  CHECKOUT_POST --> SEM_ENDERECO
  SEM_ENDERECO --> |Não| REDIR_NOVO_END
  SEM_ENDERECO --> |Sim| VALIDA_END

  VALIDA_END --> |Inválido| ERRO_END --> RENDER_CHECKOUT
  VALIDA_END --> |Válido| CRIA_PEDIDO --> CRIA_ITENS --> LIMPA_SESSAO --> REDIR_CONF --> CONF_GET --> MOSTRA_CONF
