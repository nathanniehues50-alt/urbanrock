# usuarios/views.py
from typing import Optional

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import EnderecoForm, PerfilForm, RegistroForm, UsuarioForm
from .models import Endereco


# ============================================================
# REGISTRAR NOVO USUÁRIO
# ============================================================
def registrar(request: HttpRequest) -> HttpResponse:
    """Cadastro de novo usuário da loja."""
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loga automaticamente
            messages.success(request, "Conta criada com sucesso! Bem-vindo(a) 😄")
            return redirect("home")
    else:
        form = RegistroForm()

    return render(request, "usuarios/registrar.html", {"form": form})


# ============================================================
# MINHA CONTA (DASHBOARD)
# ============================================================
@login_required
def minha_conta(request: HttpRequest) -> HttpResponse:
    """Dashboard do cliente: dados pessoais + endereços."""
    usuario = request.user
    perfil = usuario.perfil  # criado via signal

    if request.method == "POST":
        u_form = UsuarioForm(request.POST, instance=usuario)
        p_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect("minha_conta")
    else:
        u_form = UsuarioForm(instance=usuario)
        p_form = PerfilForm(instance=perfil)

    enderecos = usuario.enderecos.all().order_by("-padrao", "id")

    contexto = {
        "u_form": u_form,
        "p_form": p_form,
        "enderecos": enderecos,
    }

    return render(request, "usuarios/minha_conta.html", contexto)


# ============================================================
# ALTERAR SENHA DO CLIENTE
# ============================================================
@login_required
def alterar_senha(request: HttpRequest) -> HttpResponse:
    """Tela para o cliente alterar a própria senha."""
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # mantém logado
            messages.success(request, "Senha alterada com sucesso!")
            return redirect("minha_conta")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "usuarios/alterar_senha.html", {"form": form})


# ============================================================
# ENDEREÇOS – FUNÇÃO AUXILIAR
# ============================================================
def _get_next_url_name(request: HttpRequest, default: str = "minha_conta") -> str:
    """
    Recupera o "nome" da URL de retorno (next) para depois de salvar/editar/remover endereço.
    Ex.: "checkout", "minha_conta".
    """
    return request.GET.get("next") or request.POST.get("next") or default


# ============================================================
# ENDEREÇOS – CRUD COMPLETO
# ============================================================
@login_required
def endereco_novo(request: HttpRequest) -> HttpResponse:
    """
    Criação de novo endereço.

    - Se vier ?next=checkout, depois de salvar volta para o checkout
      já com o novo endereço selecionado.
    - Caso contrário, volta para 'minha_conta'.
    - Se for o primeiro endereço, marca como padrão.
    """
    next_name = _get_next_url_name(request, default="minha_conta")

    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco: Endereco = form.save(commit=False)
            endereco.usuario = request.user

            # 🔥 Garante que o APELIDO seja salvo mesmo se o form não tiver o campo
            apelido = None
            if "apelido" in form.cleaned_data:
                apelido = form.cleaned_data.get("apelido")
            else:
                apelido = request.POST.get("apelido", "").strip()

            if apelido:
                endereco.apelido = apelido

            # Se for o primeiro endereço, define como padrão
            if not request.user.enderecos.exists():
                if hasattr(endereco, "padrao"):
                    endereco.padrao = True

            endereco.save()
            messages.success(request, "Endereço adicionado com sucesso! ✅")

            # Se veio do checkout, volta para o checkout com o novo endereço selecionado
            if next_name == "checkout":
                checkout_url = reverse("checkout")
                return redirect(f"{checkout_url}?endereco_id={endereco.id}")

            # Caso contrário, volta para a página indicada
            return redirect(next_name)
    else:
        form = EnderecoForm()

    contexto = {
        "form": form,
        "titulo": "Adicionar endereço",
        "next": next_name,
    }
    return render(request, "usuarios/endereco_form.html", contexto)


@login_required
def endereco_editar(request: HttpRequest, pk: int) -> HttpResponse:
    """Edição de endereço existente do usuário."""
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    next_name = _get_next_url_name(request, default="minha_conta")

    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            endereco = form.save(commit=False)

            # 🔥 Atualiza o apelido também
            apelido = None
            if "apelido" in form.cleaned_data:
                apelido = form.cleaned_data.get("apelido")
            else:
                apelido = request.POST.get("apelido", "").strip()

            endereco.apelido = apelido or None

            endereco.save()
            messages.success(request, "Endereço atualizado com sucesso!")

            if next_name == "checkout":
                checkout_url = reverse("checkout")
                return redirect(f"{checkout_url}?endereco_id={endereco.id}")
            return redirect(next_name)
    else:
        form = EnderecoForm(instance=endereco)

    contexto = {
        "form": form,
        "titulo": "Editar endereço",
        "next": next_name,
    }
    return render(request, "usuarios/endereco_form.html", contexto)


@login_required
def endereco_remover(request: HttpRequest, pk: int) -> HttpResponse:
    """Remoção de endereço do usuário."""
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    next_name = _get_next_url_name(request, default="minha_conta")

    if request.method == "POST":
        endereco.delete()
        messages.success(request, "Endereço removido com sucesso!")
        return redirect(next_name)

    contexto = {
        "endereco": endereco,
        "next": next_name,
    }
    return render(request, "usuarios/endereco_confirm_delete.html", contexto)


@login_required
def endereco_definir_padrao(request: HttpRequest, pk: int) -> HttpResponse:
    """
    Define um endereço como padrão.

    - Garante que apenas um endereço fique como padrão.
    """
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    next_name = _get_next_url_name(request, default="minha_conta")

    if request.method == "POST":
        Endereco.objects.filter(usuario=request.user, padrao=True).exclude(pk=pk).update(
            padrao=False
        )
        if hasattr(endereco, "padrao"):
            endereco.padrao = True
            endereco.save(update_fields=["padrao"])

        messages.success(request, "Endereço definido como padrão!")
        return redirect(next_name)

    contexto = {
        "endereco": endereco,
        "next": next_name,
    }
    return render(request, "usuarios/endereco_confirm_padrao.html", contexto)
