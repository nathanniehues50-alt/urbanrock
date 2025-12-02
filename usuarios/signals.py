# usuarios/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil(sender, instance, created, **kwargs):
    """
    Sempre que um usuário for criado, cria o Perfil.
    Quando o usuário for salvo, garante que o perfil existe.
    """
    if created:
        Perfil.objects.create(
            user=instance,
            nome_completo=instance.get_full_name() or instance.username
        )
    else:
        # Se por algum motivo não tiver perfil ainda, cria
        Perfil.objects.get_or_create(
            user=instance,
            defaults={
                "nome_completo": instance.get_full_name() or instance.username
            }
        )
