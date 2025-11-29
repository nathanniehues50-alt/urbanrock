from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True)

    # Preço normal
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    # Preço promocional (opcional)
    preco_promocional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    estoque = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    imagem = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True
    )

    categoria = models.CharField(max_length=100, blank=True)
    destaque = models.BooleanField(default=False)

    # Ficha técnica / especificações (JSON)
    especificacoes = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.nome

    @property
    def desconto_percentual(self):
        """
        Retorna um inteiro com a % de desconto.
        Ex: 20 -> significa -20%
        """
        if self.preco_promocional and self.preco and self.preco > 0:
            desconto = (1 - (self.preco_promocional / self.preco)) * 100
            return round(desconto)
        return 0


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='imagens'
    )
    imagem = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"


class AvaliacaoProduto(models.Model):
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )
    nome = models.CharField(max_length=100, blank=True)
    nota = models.IntegerField()
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.produto.nome} ({self.nota}/5)"
