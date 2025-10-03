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
    rua = models.CharField("Rua", max_length=200, blank=True)
    numero = models.PositiveIntegerField("Quantidade", default=0, null= True)
    cep = models.CharField("CEP", max_length=10, blank=True)
    bairro = models.CharField("Bairro", max_length=50, blank=True)
    cidade = models.CharField("Cidade", max_length=50, blank=True)
    complemento = models.CharField("Complemento", max_length=50, blank=True)
    telefone = PhoneField("Telefone", blank=True)
    def __str__(self):
        return self.rua, self.numero, self.cep, self.bairro, self.cidade, self.complemento, self.telefone

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

class Avaliacao(models.Model):
    id_evaluation = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    profile_name = models.CharField(max_length=255, null=True, blank=True)
    review_helpfulness = models.CharField(max_length=20, null=True, blank=True)
    review_score= models.FloatField()
    review_time = models.IntegerField()
    review_summary = models.CharField(max_length=255, null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - Score: {self.review_score}"
