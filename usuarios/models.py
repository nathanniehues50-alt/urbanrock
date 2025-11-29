# usuarios/models.py
from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    """Informações básicas do usuário para área Minha Conta."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil"
    )
    nome_completo = models.CharField(
        "Nome completo",
        max_length=150,
        blank=True
    )
    foto = models.ImageField(
        "Foto de perfil",
        upload_to="perfis/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome_completo or self.user.get_username()


class Endereco(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enderecos')

    nome_destinatario = models.CharField('Nome do destinatário', max_length=150)
    cep = models.CharField('CEP', max_length=9)
    estado = models.CharField('Estado', max_length=2)
    cidade = models.CharField('Cidade', max_length=100)
    bairro = models.CharField('Bairro', max_length=100)
    rua = models.CharField('Rua', max_length=150)
    numero = models.CharField('Número', max_length=20)
    complemento = models.CharField('Complemento', max_length=100, blank=True)
    referencia = models.CharField('Referência', max_length=100, blank=True)

    padrao = models.BooleanField('Endereço principal', default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['-padrao', '-criado_em']

    def __str__(self):
        return f'{self.nome_destinatario} - {self.cidade}/{self.estado}'
