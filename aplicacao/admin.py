from django.contrib import admin
from .models import Produto

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'qtde')

admin.site.register(Produto, ProdutoAdm)

