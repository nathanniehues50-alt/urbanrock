from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacao/<int:pedido_id>/', views.confirmacao, name='pedido_confirmacao'),
    path("pagamento/iniciar/", views.iniciar_pagamento, name="iniciar_pagamento"),
    path("pagamento/retorno/", views.retorno_pagamento, name="retorno_pagamento"),
    path("pagamento/webhook/", views.webhook_gateway, name="webhook_gateway"),
]
