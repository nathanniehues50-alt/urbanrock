# orders/views.py
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from usuarios.models import Endereco
from .models import Pedido, ItemPedido
from produtos.views import montar_carrinho


@login_required
def checkout(request):
    # Monta o carrinho com a mesma lógica da tela do carrinho
    carrinho_ctx = montar_carrinho(request)

    itens = carrinho_ctx["itens"]
    subtotal = carrinho_ctx["subtotal"]
    cupom_codigo = carrinho_ctx["cupom_codigo"]
    desconto_valor = carrinho_ctx["desconto_valor"]
    frete_valor = carrinho_ctx["frete_valor"]
    frete_desc = carrinho_ctx["frete_desc"]
    total = carrinho_ctx["total"]

    # Se o carrinho estiver vazio, volta pra página do carrinho
    if not itens:
        return redirect("carrinho")

    # Endereços do usuário
    enderecos = Endereco.objects.filter(usuario=request.user)
    erro_endereco = None

    if request.method == "POST":
        # Se não tem NENHUM endereço ainda, manda pra tela de novo endereço
        if not enderecos.exists():
            return redirect("endereco_novo")

        endereco_id = request.POST.get("endereco_id")

        try:
            endereco = enderecos.get(id=endereco_id)
        except (Endereco.DoesNotExist, ValueError, TypeError):
            erro_endereco = "Selecione um endereço válido para entrega."
        else:
            # Cria o pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                endereco=endereco,
                total=total,
                # opcional: estimativa_entrega=...
            )

            # Cria os itens do pedido
            for item in itens:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item["produto"],
                    quantidade=item["quantidade"],
                    preco_unitario=item["preco_unitario"],
                    subtotal=item["subtotal"],
                )

            # Limpar carrinho e dados de frete/cupom da sessão
            sessao = request.session
            sessao["cart"] = {}
            sessao["cupom_codigo"] = None
            sessao["desconto_valor"] = "0"
            sessao["frete_valor"] = "0"
            sessao["frete_desc"] = "Não calculado"
            sessao.modified = True

            # Redireciona para página de confirmação
            return redirect("pedido_confirmacao", pedido_id=pedido.id)

    # GET ou POST com erro_endereco → renderiza tela de checkout
    return render(
        request,
        "orders/checkout.html",
        {
            "enderecos": enderecos,
            "itens": itens,
            "subtotal": subtotal,
            "cupom_codigo": cupom_codigo,
            "desconto_valor": desconto_valor,
            "frete_valor": frete_valor,
            "frete_desc": frete_desc,
            "total": total,
            "erro_endereco": erro_endereco,
        },
    )


@login_required
def confirmacao(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "orders/confirmacao.html", {"pedido": pedido})
