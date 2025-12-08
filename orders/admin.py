from django.contrib import admin

from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("produto", "quantidade", "preco_unitario", "subtotal")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "status", "total", "criado_em", "estimativa_entrega")
    list_filter = ("status", "criado_em")
    search_fields = ("id", "usuario__username", "endereco__rua", "endereco__cep")
    readonly_fields = ("criado_em", "total")
    inlines = [ItemPedidoInline]

    # 🔽 Ações rápidas no admin para mudar status
    actions = ["marcar_pagamento_aprovado", "marcar_pedido_enviado", "marcar_pedido_entregue", "marcar_cancelado"]

    def marcar_pagamento_aprovado(self, request, queryset):
        queryset.update(status="pagamento_aprovado")
    marcar_pagamento_aprovado.short_description = "Marcar como pagamento aprovado"

    def marcar_pedido_enviado(self, request, queryset):
        queryset.update(status="pedido_enviado")
    marcar_pedido_enviado.short_description = "Marcar como pedido enviado"

    def marcar_pedido_entregue(self, request, queryset):
        queryset.update(status="pedido_entregue")
    marcar_pedido_entregue.short_description = "Marcar como pedido entregue"

    def marcar_cancelado(self, request, queryset):
        queryset.update(status="cancelado")
    marcar_cancelado.short_description = "Marcar como pedido cancelado"


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "produto", "quantidade", "subtotal")
    search_fields = ("pedido__id", "produto__nome")

