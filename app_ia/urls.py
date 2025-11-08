from django.urls import path
from . import views

urlpatterns = [
    path('analise-ia/', views.analise_ia, name='analise_ia'),
    path('historico-analise/', views.historico_analise, name='historico_analise'),

]
