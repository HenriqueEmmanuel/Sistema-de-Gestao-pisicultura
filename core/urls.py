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
    path('deletar-tanque/<int:tanque_id>/', views.deletar_tanque, name='deletar_tanque'),
    path('logout/', views.sair, name='logout'),
    path("atualizar-situacao/<int:tanque_id>/", views.atualizar_situacao_tanque, name="atualizar_situacao"),
    path('atualizar-situacao/', views.atualizar_situacao_tanque, name='atualizar_situacao'),
    ## essas urls ainda estão em    teste de vbaixo
    path('api/contadores-sensores/', views.contadores_sensores, name='contadores_sensores'),
    path('api/escanear-rede/', views.escanear_rede, name='escanear_rede'),
    path('tanque/<int:tanque_id>/configuracoes/', views.configuracoes_tanque, name='configuracoes_tanque'),
    path('tanque/<int:tanque_id>/salvar/', views.salvar_configuracoes_tanque, name='salvar_configuracoes_tanque'),
    path('tanque/<int:tanque_id>/salvar-configuracoes/', views.salvar_configuracoes_tanque, name='salvar_configuracoes_tanque'),
    path('api/dados-sensores/', views.dados_sensores, name='dados_sensores'),
    path('api/tanques-do-usuario/', views.tanques_do_usuario, name='tanques_do_usuario'),
    path('cfg/', views.cfg, name='cfg'),
    path('salvarcfg/', views.salvarcfg, name='salvarcfg'),#
    path('transacoes/', views.transacoes, name='transacoes'),
    path('fluxo_caixa/', views.fluxo_caixa, name='fluxo_caixa'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('observacoes/', views.observacoes, name='observacoes'),
    path('indicadores/', views.indicadores, name='indicadores'),
    path('nova_transacao/', views.nova_transacao, name='nova_transacao'),
    path('salvar_parametros_modal/<int:tanque_id>/', views.salvar_parametros_modal, name='salvar_parametros_modal'),
    path('salvar_parametros_personalizados/<int:tanque_id>/', views.salvar_parametros_personalizados, name='salvar_parametros_personalizados'),
    path('get_parametros_personalizados/<int:tanque_id>/', views.get_parametros_personalizados, name='get_parametros_personalizados'),
    path('salvar_configuracoes_tanque/<int:tanque_id>/', views.salvar_configuracoes_tanque, name='salvar_configuracoes_tanque'),
    path('exportar-transacoes/', views.exportar_transacoes, name='exportar_transacoes'),
    path('api/sensordata/', views.receive_sensor_data, name='receive_sensor_data'),

]
