from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cliente, Produto, Venda
from django.contrib import messages
from django.contrib.auth.models import User

# ---------- AUTENTICAÇÃO ----------

def cadastrar_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmar = request.POST['confirmar']

        # Verifica se as senhas coincidem
        if senha != confirmar:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('cadastro')

        # Verifica se o nome de usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe!')
            return redirect('cadastro')

        # Cria o novo usuário
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso! Faça login.')
        return redirect('login')

    return render(request, 'cadastro.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos!')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')


# ---------- DASHBOARD ----------
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})


# ---------- CLIENTES ----------
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        telefone = request.POST['telefone']
        email = request.POST['email']
        Cliente.objects.create(nome=nome, telefone=telefone, email=email)
        return redirect('lista_clientes')
    return render(request, 'cadastrar_cliente.html')


# ---------- PRODUTOS ----------
@login_required
def lista_produtos(request):
    produtos = Produto.objects.all().order_by('nome')
    return render(request, 'produtos.html', {'produtos': produtos})

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        preco = request.POST['preco']
        quantidade = int(request.POST['quantidade'])
        Produto.objects.create(nome=nome, preco=preco, quantidade=quantidade)
        return redirect('lista_produtos')
    return render(request, 'cadastrar_produto.html')


# ---------- VENDAS ----------
@login_required
def lista_vendas(request):
    vendas = Venda.objects.select_related('cliente', 'produto')
    return render(request, 'vendas.html', {'vendas': vendas})

@login_required
def cadastrar_venda(request):
    clientes = Cliente.objects.all()
    produtos = Produto.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        produto_id = request.POST['produto']
        quantidade = int(request.POST['quantidade'])

        cliente = Cliente.objects.get(id=cliente_id)
        produto = Produto.objects.get(id=produto_id)

        if produto.quantidade >= quantidade:
            produto.quantidade -= quantidade
            produto.save()
            Venda.objects.create(cliente=cliente, produto=produto, quantidade=quantidade)
            messages.success(request, 'Venda registrada com sucesso!')
        else:
            messages.error(request, 'Estoque insuficiente para esta venda.')

        return redirect('lista_vendas')

    return render(request, 'cadastrar_venda.html', {'clientes': clientes, 'produtos': produtos})

