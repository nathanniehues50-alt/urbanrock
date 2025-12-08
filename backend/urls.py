# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from usuarios import views as usuarios_views

urlpatterns = [
    # Painel admin
    path('admin/', admin.site.urls),

    # Rotas da loja (produtos, home, busca, etc)
    path('', include('produtos.urls')),

    # Rotas de usuário (cadastro, login, endereços…)
    path('usuario/', include('usuarios.urls')),

    # Rotas de pedidos (checkout, confirmação, pagamento…)
    path('pedido/', include('orders.urls')),


    # LOGIN
    path(
        'entrar/',
        auth_views.LoginView.as_view(template_name='usuarios/login.html'),
        name='login'
    ),

    # LOGOUT
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

    # Minha conta
    path(
        'minha-conta/',
        usuarios_views.minha_conta,
        name='minha_conta'
    ),
]

# Media (em modo DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
