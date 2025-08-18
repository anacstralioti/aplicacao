from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="url_index"),
    path('produtos', views.produtos, name="url_produtos"),
]