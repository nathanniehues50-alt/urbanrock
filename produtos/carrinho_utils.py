from decimal import Decimal
from produtos.models import Produto


def montar_itens_carrinho(request):
    """
    Lê o carrinho da sessão e devolve:
    - itens: lista com os mesmos campos usados no carrinho.html
    - subtotal: Decimal com o total
    """

    sessao = request.session.get('carrinho', {})
    itens = []
    subtotal = Decimal('0.00')

    for produto_id, dados in sessao.items():
        produto = Produto.objects.get(id=produto_id)
        quantidade = int(dados.get('quantidade', 1))

        preco_unit = produto.preco_promocional or produto.preco
        sub = preco_unit * quantidade
        subtotal += sub

        itens.append({
            'produto': produto,
            'variacao': dados.get('variacao'),
            'preco_unitario': preco_unit,
            'quantidade': quantidade,
            'subtotal': sub,
        })

    return itens, subtotal
