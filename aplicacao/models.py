from django.db import models
from phone_field import PhoneField


class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200, null= True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8, null= True)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null= True)
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField("Nome", max_length=200, unique = True)
    email = models.EmailField("Email", max_length=200, unique = True)
    def __str__(self):
        return self.nome, self.email

class Perfil(models.Model):        
    cliente = models.OneToOneField("Cliente", on_delete=models.CASCADE, related_name="perfil")
    endereco = models.CharField("Endereço", max_length=200)
    telefone = PhoneField("Telefone", blank=True)
    def __str__(self):
        return self.endereco, self.telefone

class Venda(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    produto = models.ManyToManyField("Produto", through="ItemVenda")
    data = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.data

class ItemVenda(models.Model):
    venda = models.ForeignKey("Venda", on_delete=models.CASCADE)
    produto = models.ForeignKey("Produto", on_delete=models.CASCADE)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null= True)
    def __str__(self):
        return self.qtde
