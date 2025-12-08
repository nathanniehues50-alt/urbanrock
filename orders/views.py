# orders/views.py
from typing import Any, Dict, Optional
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from usuarios.models import Endereco
from produtos.views import montar_carrinho
from .models import Pedido, ItemPedido, TransacaoPagamento


# ============================================================
# FUNÇÃO AUXILIAR — LIMPAR CARRINHO NA SESSÃO
# ============================================================
def _limpar_carrinho(sessao: Dict[str, Any]) -> None:
    """
    Limpa os dados de carrinho, cupom e frete da sessão do usuário.

    Mantém toda a lógica de limpeza em um único lugar
    para evitar código duplicado e facilitar manutenção.
    """
    sessao["cart"] = {}
    sessao["cupom_codigo"] = None
    sessao["desconto_valor"] = "0"
    sessao["frete_valor"] = "0"
    sessao["frete_desc"] = "Não calculado"
    sessao.modified = True


# ============================================================
# CHECKOUT — CRIAÇÃO DO PEDIDO
# ============================================================
@login_required
@transaction.atomic
def checkout(request: HttpRequest) -> HttpResponse:
    """
    Fluxo de checkout da UrbanRock.

    Responsabilidades:
    - Carregar o carrinho (mesma lógica da tela do carrinho)
    - Garantir que o carrinho não esteja vazio
    - Listar endereços do usuário para seleção
    - Permitir voltar do cadastro de endereço com um endereço já selecionado
    - Validar endereço escolhido
    - Criar Pedido e ItemPedido de forma atômica (tudo ou nada)
    - Limpar carrinho da sessão após criar o pedido
    - Redirecionar para a página de confirmação
    """
    # 1) Monta o carrinho com a lógica unificada
    carrinho_ctx = montar_carrinho(request)

    itens = carrinho_ctx["itens"]
    subtotal: Decimal = carrinho_ctx["subtotal"]
    cupom_codigo = carrinho_ctx["cupom_codigo"]
    desconto_valor: Decimal = carrinho_ctx["desconto_valor"]
    frete_valor: Decimal = carrinho_ctx["frete_valor"]
    frete_desc = carrinho_ctx["frete_desc"]
    total: Decimal = carrinho_ctx["total"]

    # 2) Se o carrinho estiver vazio, volta para a página do carrinho
    if not itens:
        return redirect("carrinho")

    # 3) Endereços do usuário
    enderecos = Endereco.objects.filter(usuario=request.user)
    erro_endereco: Optional[str] = None
    endereco_selecionado_id: Optional[int] = None

    # 4) GET → pode vir com ?endereco_id=XX (acabou de cadastrar endereço novo)
    if request.method == "GET":
        endereco_get = request.GET.get("endereco_id")
        if endereco_get:
            try:
                endereco_selecionado_id = int(endereco_get)
            except ValueError:
                endereco_selecionado_id = None

    # 5) POST → tentar criar o pedido
    if request.method == "POST":
        # Se não tem NENHUM endereço ainda, manda pra tela de novo endereço
        if not enderecos.exists():
            return redirect("endereco_novo")

        endereco_id_str = request.POST.get("endereco_id")

        # Guarda o id selecionado para manter marcado no template em caso de erro
        try:
            endereco_selecionado_id = int(endereco_id_str) if endereco_id_str else None
        except ValueError:
            endereco_selecionado_id = None

        try:
            endereco = enderecos.get(id=endereco_id_str)
        except (Endereco.DoesNotExist, ValueError, TypeError):
            erro_endereco = "Selecione um endereço válido para entrega."
        else:
            # 6) Cria o pedido (tudo dentro de transaction.atomic)
            pedido = Pedido.objects.create(
                usuario=request.user,
                endereco=endereco,
                total=total,
                status="aguardando_pagamento",
                # Se o model tiver mais campos (frete, desconto etc.), adicionar aqui.
            )

            # 7) Cria os itens do pedido (alta performance com bulk_create)
            itens_pedido: list[ItemPedido] = []
            for item in itens:
                itens_pedido.append(
                    ItemPedido(
                        pedido=pedido,
                        produto=item["produto"],
                        quantidade=item["quantidade"],
                        preco_unitario=item["preco_unitario"],
                        subtotal=item["subtotal"],  # mesma chave usada no carrinho
                    )
                )
            ItemPedido.objects.bulk_create(itens_pedido)

            # 8) Limpa o carrinho e dados auxiliares da sessão
            _limpar_carrinho(request.session)

            # 9) Redireciona para página de confirmação do pedido
            return redirect("pedido_confirmacao", pedido_id=pedido.id)

    # 10) GET inicial ou POST com erro de endereço → renderiza tela de checkout
    contexto = {
        "enderecos": enderecos,
        "itens": itens,
        "subtotal": subtotal,
        "cupom_codigo": cupom_codigo,
        "desconto_valor": desconto_valor,
        "frete_valor": frete_valor,
        "frete_desc": frete_desc,
        "total": total,
        "erro_endereco": erro_endereco,
        "endereco_selecionado_id": endereco_selecionado_id,
    }

    return render(request, "orders/checkout.html", contexto)


# ============================================================
# CONFIRMAÇÃO DO PEDIDO
# ============================================================
@login_required
def confirmacao(request: HttpRequest, pedido_id: int) -> HttpResponse:
    """
    Tela de confirmação de pedido.

    - Garante que o pedido é do usuário logado
    - Busca os itens diretamente no banco
    - Envia 'pedido' e 'itens' para o template
    """
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    # Busca os itens do pedido direto no banco (independente de related_name)
    itens = (
        ItemPedido.objects
        .filter(pedido=pedido)
        .select_related("produto")
        .order_by("id")
    )

    contexto = {
        "pedido": pedido,
        "itens": itens,
    }
    return render(request, "orders/confirmacao.html", contexto)


# ============================================================
# INICIAR PAGAMENTO
# ============================================================
@login_required
def iniciar_pagamento(request: HttpRequest) -> HttpResponse:
    """
    Inicia o fluxo de pagamento para um Pedido já criado.

    Espera receber um 'pedido_id' (por POST ou GET).

    Responsabilidades:
    - Localizar o Pedido do usuário logado
    - Criar uma TransacaoPagamento vinculada ao Pedido
    - (Futuro) Chamar o gateway real e obter a URL de pagamento
    - Redirecionar o cliente para o "gateway" (por enquanto, simulado)
    """
    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
    else:
        pedido_id = request.GET.get("pedido_id")

    if not pedido_id:
        return redirect("home")

    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    # 1) Criar Transacao de Pagamento (sem chamar gateway ainda)
    transacao = TransacaoPagamento.objects.create(
        pedido=pedido,
        gateway="mercado_pago",  # pode trocar depois
        valor=pedido.total,
        status_local="iniciado",
    )

    # 2) Simular ID do gateway (no futuro, este ID vem da API)
    transacao.gateway_payment_id = f"FAKE-{pedido.id}"
    transacao.save()

    # 3) Simular redirecionamento para o gateway:
    url_retorno = reverse("retorno_pagamento")
    return redirect(f"{url_retorno}?pedido={pedido.id}")


# ============================================================
# RETORNO DO PAGAMENTO (APÓS GATEWAY)
# ============================================================
@login_required
def retorno_pagamento(request: HttpRequest) -> HttpResponse:
    """
    O cliente foi redirecionado de volta pelo gateway.

    Esta view NÃO confirma o pagamento sozinha.
    Ela apenas mostra o estado atual salvo no banco.
    Quem confirma de verdade é o webhook (gateway -> servidor).
    """
    pedido_id = request.GET.get("pedido")
    if not pedido_id:
        return render(
            request,
            "pagamento_retorno.html",
            {"erro": "Pedido não encontrado."},
        )

    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    transacao = pedido.transacoes.last()

    contexto = {
        "pedido": pedido,
        "transacao": transacao,
    }
    return render(request, "pagamento_retorno.html", contexto)


# ============================================================
# WEBHOOK DO GATEWAY DE PAGAMENTO
# ============================================================
@csrf_exempt
def webhook_gateway(request: HttpRequest) -> HttpResponse:
    """
    Endpoint chamado pelo gateway de pagamento (Webhook).

    Exemplo de corpo (POST):
    payment_id=FAKE-10
    status=approved

    Esta view:
    - Localiza a TransacaoPagamento pelo payment_id
    - Atualiza status_gateway e status_local
    - Atualiza o status do Pedido vinculado
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método inválido"}, status=400)

    payment_id = request.POST.get("payment_id")
    status_gateway = request.POST.get("status")

    if not payment_id:
        return JsonResponse({"error": "Sem payment_id"}, status=400)

    transacao = TransacaoPagamento.objects.filter(
        gateway_payment_id=payment_id
    ).first()

    if not transacao:
        return JsonResponse({"error": "Transação não encontrada"}, status=404)

    # Atualiza status da transação
    transacao.status_gateway = status_gateway

    # Mapeia status do gateway para status interno da loja
    if status_gateway == "approved":
        transacao.status_local = "pago"
        transacao.pedido.status = "pago"

    elif status_gateway in ["rejected", "cancelled"]:
        transacao.status_local = "cancelado"
        transacao.pedido.status = "cancelado"

    else:
        transacao.status_local = "pendente"
        transacao.pedido.status = "aguardando_pagamento"

    transacao.pedido.save()
    transacao.save()

    return JsonResponse({"status": "ok"})
