from django.db import models


class Produto(models.Model):
    nome = models.CharField("Nome", max_length=200, null= True)
    preco = models.DecimalField("Preço", decimal_places=2, max_digits=8, null= True)
    qtde = models.PositiveIntegerField("Quantidade", default=0, null= True)
    def __str__(self):
        return self.nome