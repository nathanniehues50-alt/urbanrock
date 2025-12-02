# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Endereco, Perfil


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            "nome_destinatario",
            "cep",
            "estado",
            "cidade",
            "bairro",
            "rua",
            "numero",
            "complemento",
            "referencia",
            "padrao",
        ]
        widgets = {
            "nome_destinatario": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome de quem vai receber",
            }),
            "cep": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "00000-000",
            }),
            "estado": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "cidade": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "bairro": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "rua": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "numero": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "complemento": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "referencia": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "padrao": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }


class RegistroForm(UserCreationForm):
    first_name = forms.CharField(
        label="Nome",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "password1", "password2"]
        labels = {
            "username": "Usuário",
            "password1": "Senha",
            "password2": "Confirmar senha",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email


class UsuarioForm(forms.ModelForm):
    """Atualização dos dados básicos do usuário (Django User)."""
    class Meta:
        model = User
        fields = ["first_name", "email"]
        labels = {
            "first_name": "Nome",
            "email": "E-mail",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class PerfilForm(forms.ModelForm):
    """Atualização de dados adicionais do perfil (seu modelo Perfil)."""
    class Meta:
        model = Perfil
        fields = ["nome_completo", "foto"]
        labels = {
            "nome_completo": "Nome completo para entregas",
            "foto": "Foto de perfil",
        }
        widgets = {
            "nome_completo": forms.TextInput(attrs={"class": "form-control"}),
            # file input já vem com widget próprio, não precisa mexer
        }
