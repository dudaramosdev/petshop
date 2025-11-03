from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

    def estoque_baixo(self):
        return self.quantidade < 5


class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    data_venda = models.DateTimeField(auto_now_add=True)

    def valor_total(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f"{self.cliente.nome} - {self.produto.nome}"
