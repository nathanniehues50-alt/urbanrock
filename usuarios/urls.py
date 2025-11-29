# usuarios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("minha-conta/", views.minha_conta, name="minha_conta"),
    path("alterar-senha/", views.alterar_senha, name="alterar_senha"),

    path("endereco/novo/", views.endereco_novo, name="endereco_novo"),
    path("endereco/<int:pk>/editar/", views.endereco_editar, name="endereco_editar"),
    path("endereco/<int:pk>/remover/", views.endereco_remover, name="endereco_remover"),
    path("endereco/<int:pk>/definir-padrao/", views.endereco_definir_padrao, name="endereco_definir_padrao"),

    path("registrar/", views.registrar, name="registrar"),
]
