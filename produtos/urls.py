from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Buscar produtos
    path('buscar/', views.buscar_produtos, name='buscar_produtos'),

    # Detalhe do produto
    path('produto/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),

    # Carrinho
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/atualizar/<int:produto_id>/', views.atualizar_carrinho, name='atualizar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),

    # Cupom e frete
    path('carrinho/cupom/', views.aplicar_cupom, name='aplicar_cupom'),
    path('carrinho/frete/', views.calcular_frete, name='calcular_frete'),
]
