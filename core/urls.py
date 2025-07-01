from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tank/', views.tank, name='tank'),
    path('analise/', views.analise, name='analise'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('historico_sensor/', views.historico_sensor, name='historico_sensor'),
    path('gerenciamento_sensor/', views.gerenciamento_sensor, name='gerenciamento_sensor'),
    path('dashboard/content/', views.dashboard_content, name='dashboard_content'),
    path('cadastro_tanque/', views.cadastro_tanque, name='cadastro_tanque'),
    path('histo_analise/', views.histo_analise, name='histo_analise'),
    path('detalhes-tanque-json/<int:tanque_id>/', views.detalhes_tanque_json, name='detalhes_tanque_json'),

]
