from django.db import models
from django.contrib.auth.models import User

from produtos.models import Produto
from usuarios.models import Endereco


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("aguardando_pagamento", "Aguardando pagamento"),   # status inicial
        ("pagamento_aprovado", "Pagamento aprovado"),
        ("pedido_enviado", "Pedido enviado"),
        ("pedido_entregue", "Pedido entregue"),
        ("cancelado", "Cancelado"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )

    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="aguardando_pagamento",
    )

    # 🆕 “Encomende em” / previsão de entrega
    estimativa_entrega = models.DateField(
        null=True,
        blank=True,
        help_text="Data estimada de entrega do pedido.",
    )

    observacoes = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

    @property
    def endereco_resumo(self):
        e = self.endereco
        return (
            f"{e.nome_destinatario}, {e.rua}, {e.numero}, "
            f"{e.bairro}, {e.cidade}-{e.estado}, CEP {e.cep}"
        )


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="itens",
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
    )

    quantidade = models.PositiveIntegerField()

    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"

# orders/models.py
from django.db import models

# ... aqui já devem estar os models Pedido, ItemPedido, etc.


class TransacaoPagamento(models.Model):
    """
    Registra as tentativas de pagamento de um pedido.
    Fica bem flexível pra usar Mercado Pago / PagBank / Stripe.
    """

    GATEWAY_CHOICES = [
        ("mercado_pago", "Mercado Pago"),
        ("pagbank", "PagBank"),
        ("stripe", "Stripe"),
    ]

    STATUS_LOCAL_CHOICES = [
        ("iniciado", "Iniciado"),
        ("pendente", "Pendente"),
        ("pago", "Pago"),
        ("falhou", "Falhou"),
        ("cancelado", "Cancelado"),
    ]

    pedido = models.ForeignKey(
        "Pedido",
        on_delete=models.CASCADE,
        related_name="transacoes",
    )

    gateway = models.CharField(
        max_length=30,
        choices=GATEWAY_CHOICES,
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status_local = models.CharField(
        max_length=20,
        choices=STATUS_LOCAL_CHOICES,
        default="iniciado",
    )

    # ID da transação no gateway (ex: preference_id do Mercado Pago)
    gateway_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    # Opcional: guardar o payload cru do gateway (webhook, etc.)
    payload_raw = models.JSONField(
        blank=True,
        null=True,
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return f"Transação {self.id} - Pedido {self.pedido_id} - {self.gateway} - {self.status_local}"
