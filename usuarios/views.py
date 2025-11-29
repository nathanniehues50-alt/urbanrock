# usuarios/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    EnderecoForm,
    RegistroForm,
    UsuarioForm,
    PerfilForm,
)
from .models import Endereco


# ============================================================
# REGISTRAR NOVO USUÁRIO
# ============================================================
def registrar(request):
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
def minha_conta(request):
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
def alterar_senha(request):
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
# ENDEREÇOS – CRUD COMPLETO
# ============================================================
@login_required
def endereco_novo(request):
    if request.method == "POST":
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.usuario = request.user
            endereco.save()
            messages.success(request, "Endereço adicionado com sucesso!")
            return redirect("minha_conta")
    else:
        form = EnderecoForm()

    contexto = {"form": form, "titulo": "Adicionar endereço"}
    return render(request, "usuarios/endereco_form.html", contexto)


@login_required
def endereco_editar(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)

    if request.method == "POST":
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(request, "Endereço atualizado com sucesso!")
            return redirect("minha_conta")
    else:
        form = EnderecoForm(instance=endereco)

    contexto = {"form": form, "titulo": "Editar endereço"}
    return render(request, "usuarios/endereco_form.html", contexto)


@login_required
def endereco_remover(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)

    if request.method == "POST":
        endereco.delete()
        messages.success(request, "Endereço removido com sucesso!")
        return redirect("minha_conta")

    return render(request, "usuarios/endereco_confirm_delete.html", {"endereco": endereco})


@login_required
def endereco_definir_padrao(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    endereco.padrao = True
    endereco.save()
    messages.success(request, "Endereço definido como padrão!")
    return redirect("minha_conta")
