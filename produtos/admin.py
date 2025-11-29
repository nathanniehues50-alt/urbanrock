from django.contrib import admin
from .models import Produto, ProdutoImagem, AvaliacaoProduto


class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    inlines = [ProdutoImagemInline]
    fields = [
        'nome', 'descricao',
        'preco', 'preco_promocional',
        'estoque', 'imagem',
        'categoria', 'destaque',
        'especificacoes',
    ]


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(ProdutoImagem)
admin.site.register(AvaliacaoProduto)
