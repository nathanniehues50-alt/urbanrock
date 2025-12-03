# produtos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from decimal import Decimal
from .models import Produto, AvaliacaoProduto

# ====================================================
# ------------------ FUNÇÕES DO CARRINHO --------------
# ====================================================

def buscar_produtos(request):
    termo = request.GET.get("q", "")

    produtos = Produto.objects.filter(nome__icontains=termo)

    return render(request, "produtos/buscar.html", {"produtos": produtos, "termo": termo})

def _get_cart(session):
    """Retorna o carrinho existente na sessão ou cria um novo."""
    return session.setdefault("cart", {})


def carrinho(request):
    """Página do carrinho com subtotal, frete e cupom."""
    cart = _get_cart(request.session)

    itens = []
    subtotal = Decimal("0")

    for product_id, item_data in cart.items():
        produto = get_object_or_404(Produto, id=product_id)
        quantidade = item_data.get("quantidade", 1)

        preco_unitario = produto.preco
        subtotal_item = preco_unitario * quantidade
        subtotal += subtotal_item

        itens.append({
            "produto": produto,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "subtotal": subtotal_item,
            "variacao": item_data.get("variacao"),
        })

    # Descontos e frete
    cupom_codigo = request.session.get("cupom_codigo")
    desconto_valor = Decimal(str(request.session.get("desconto_valor", "0")))
    frete_valor = Decimal(str(request.session.get("frete_valor", "0")))
    frete_desc = request.session.get("frete_desc", "Não calculado")

    total = subtotal - desconto_valor + frete_valor

    return render(request, "carrinho.html", {
        "itens": itens,
        "subtotal": subtotal,
        "cupom_codigo": cupom_codigo,
        "desconto_valor": desconto_valor,
        "frete_valor": frete_valor,
        "frete_desc": frete_desc,
        "total": total,
    })


@require_POST
def adicionar_ao_carrinho(request, produto_id):
    cart = _get_cart(request.session)
    produto = get_object_or_404(Produto, id=produto_id)

    quantidade = request.POST.get("quantidade", 1)
    try:
        quantidade = int(quantidade)
    except:
        quantidade = 1

    item = cart.setdefault(str(produto_id), {})
    item["quantidade"] = item.get("quantidade", 0) + quantidade

    variacao = request.POST.get("variacao")
    if variacao:
        item["variacao"] = variacao

    request.session.modified = True
    return redirect("carrinho")


@require_POST
def atualizar_carrinho(request, produto_id):
    cart = _get_cart(request.session)
    quantidade = request.POST.get("quantidade")

    try:
        quantidade = int(quantidade)
    except:
        quantidade = 1

    if quantidade <= 0:
        cart.pop(str(produto_id), None)
    else:
        item = cart.setdefault(str(produto_id), {})
        item["quantidade"] = quantidade

    request.session.modified = True
    return redirect("carrinho")


@require_POST
def remover_do_carrinho(request, produto_id):
    cart = _get_cart(request.session)
    cart.pop(str(produto_id), None)
    request.session.modified = True
    return redirect("carrinho")


@require_POST
def aplicar_cupom(request):
    codigo = request.POST.get("cupom", "").strip().upper()

    if codigo == "DESCONTO10":
        request.session["cupom_codigo"] = codigo
        request.session["desconto_valor"] = Decimal("10")
    else:
        request.session["cupom_codigo"] = None
        request.session["desconto_valor"] = Decimal("0")

    request.session.modified = True
    return redirect("carrinho")


@require_POST
def calcular_frete(request):
    cep = request.POST.get("cep", "").strip()

    if cep:
        request.session["frete_valor"] = Decimal("19.90")
        request.session["frete_desc"] = f"Frete padrão para {cep} (5 a 7 dias úteis)"
    else:
        request.session["frete_valor"] = Decimal("0")
        request.session["frete_desc"] = "CEP inválido"

    request.session.modified = True
    return redirect("carrinho")


# ====================================================
# ------------------- HOME / INICIAL ------------------
# ====================================================

def home(request):
    """
    Página inicial com:
    - carrosséis por categoria
    - carrossel geral fallback
    - lista de produtos
    - destaques
    """

    # Lista fixa de categorias exibidas na home
    categorias_home = [
        ("eletronicos", "Eletrônicos"),
        ("casa-cozinha", "Casa & Cozinha"),
        ("moda", "Moda"),
        ("esportes", "Esportes & Lazer"),
        ("mercado", "Mercado"),
        ("promocoes", "Promoções"),
    ]

    carrosseis = []

    for slug, titulo in categorias_home:
        produtos_categoria = Produto.objects.filter(categoria__iexact=slug)[:12]
        if produtos_categoria.exists():
            carrosseis.append({
                "slug": slug,
                "titulo": titulo,
                "produtos": produtos_categoria,
            })

    # Fallback: pelo menos 1 carrossel
    if not carrosseis:
        produtos_geral = Produto.objects.all()[:12]
        if produtos_geral.exists():
            carrosseis.append({
                "slug": "destaques",
                "titulo": "Produtos em destaque",
                "produtos": produtos_geral,
            })

    # 🔥 COLETAR TODOS OS IDs JÁ EXIBIDOS NOS CARROSSEIS
    ids_exibidos = []
    for sec in carrosseis:
        ids_exibidos += list(sec["produtos"].values_list("id", flat=True))

    destaques = Produto.objects.filter(destaque=True)[:6]

    # 🔥 "EXPLORAR MAIS PRODUTOS" SEM REPETIR O QUE JÁ SAIU NOS CARROSSEIS
    produtos_recém_qs = Produto.objects.all().order_by("-id")
    if ids_exibidos:
        produtos_recém_qs = produtos_recém_qs.exclude(id__in=ids_exibidos)
    produtos_recém = produtos_recém_qs[:12]

    return render(request, "home.html", {
        "carrosseis": carrosseis,
        "destaques": destaques,
        "produtos": produtos_recém,
    })


# ====================================================
# ----------------- DETALHES DO PRODUTO --------------
# ====================================================

def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    avaliacoes = produto.avaliacoes.all().order_by("-criado_em")
    total_avaliacoes = avaliacoes.count()

    media_nota = round(
        sum(a.nota for a in avaliacoes) / total_avaliacoes, 1
    ) if total_avaliacoes else 0

    if request.method == "POST":
        nome = request.POST.get("nome") or "Anônimo"
        nota = int(request.POST.get("nota", 5))
        comentario = request.POST.get("comentario", "").strip()

        if 1 <= nota <= 5 and comentario:
            AvaliacaoProduto.objects.create(
                produto=produto,
                nome=nome,
                nota=nota,
                comentario=comentario
            )
            return redirect("produto_detalhe", produto_id=produto_id)

    return render(request, "produto_detalhe.html", {
        "produto": produto,
        "avaliacoes": avaliacoes,
        "total_avaliacoes": total_avaliacoes,
        "media_nota": media_nota,
    })
