from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tank/', views.tank, name='tank'),
    path('analise/', views.analise, name='analise'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historico_sensor/', views.historico_sensor, name='historico_sensor'),
    path('pagina_erro_404/', views.pagina_erro_404, name='pagina_erro_404'),
    path('gerenciamento_sensor/', views.gerenciamento_sensor, name='gerenciamento_sensor'),
]
