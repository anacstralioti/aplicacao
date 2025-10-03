from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="url_index"),
    path('produtos', views.produtos, name="url_produtos"),
    path('cad_produto', views.cad_produto, name="url_cad_produto"),
    path('atualizar_produto/<int:id>', views.atualizar_produto, name="url_atualizar_produto"),
    path('apagar_produto/<int:id>', views.apagar_produto, name="url_apagar_produto"),
    path('entrar', views.entrar, name="url_entrar"),
    path('cad_user', views.cad_user, name="url_cad_user"),
    path('sair', views.sair, name="url_sair"),
    path('cad_cliente', views.cad_cliente, name="url_cad_cliente"),
    path('cad_perfil', views.cad_perfil, name="url_cad_perfil"),
    path('cad_venda', views.cad_venda, name="url_cad_venda"),
    path('cad_itemvenda', views.cad_itemvenda, name="url_cad_itemvenda"),
    path('dashboard', views.dashboard, name='url_dashboard'),
]