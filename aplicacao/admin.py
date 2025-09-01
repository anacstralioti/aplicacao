from django.contrib import admin
from .models import Produto, Cliente, Perfil

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'qtde')

class ClienteAdm(admin.ModelAdmin):
    list_display = ('nome', 'email')

class PerfilAdm(admin.ModelAdmin):
    list_display = ('cliente', 'rua', 'numero', 'cidade', 'telefone')

admin.site.register(Produto, ProdutoAdm)
admin.site.register(Cliente, ClienteAdm)
admin.site.register(Perfil, PerfilAdm)