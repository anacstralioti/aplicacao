from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="url_index"),
    path('produtos', views.produtos, name="url_produtos"),
    path('cad_produto', views.cad_produto, name="url_cad_produto"),
    path('atualizar_produto/<int:id>', views.atualizar_produto, name="url_atualizar_produto"),
    path('apagar_produto/<int:id>', views.apagar_produto, name="url_apagar_produto"),
    path('entrar', views.entrar, name="url_entrar"),
]