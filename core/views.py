import datetime
import json
from django.http import HttpResponseForbidden, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Tanque, Usuario, HistoricoSensor
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
import re
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

def sair(request):
    logout(request)
    return redirect('index')

def cfg(request):
    return render (request, 'front/cfg.html')

def str_to_bool(value):
    return value.lower() == 'true'

@require_POST
def salvarcfg(request):
    usuario = request.user
    print("POST recebido:", request.POST)

    usuario.nome_fazenda = request.POST.get('nome_fazenda', '')
    usuario.endereco_fazenda = request.POST.get('endereco_fazenda', '')
    usuario.cidade = request.POST.get('cidade', '')
    usuario.estado = request.POST.get('estado', '')

    usuario.notificacoes_push = request.POST.get('notificacoes_push') == 'true'
    usuario.notificacoes_email = request.POST.get('notificacoes_email') == 'true'
    usuario.alertas_agua = request.POST.get('alerta_agua') == 'true'
    usuario.lembretes_alimentacao = request.POST.get('lembrete_alimentacao') == 'true'

    usuario.temperatura = request.POST.get('temperatura', 'C')
    usuario.formato_data = request.POST.get('formato_data', 'DD/MM/AAAA')
    usuario.moeda = request.POST.get('moeda', 'R$')
    usuario.idioma = request.POST.get('idioma', 'pt-BR')

    usuario.backup_automatico = request.POST.get('backup_auto') == 'true'
    usuario.frequencia_backup = request.POST.get('frequencia_backup', 'Semanal')

    usuario.autenticacao_dois_fatores = request.POST.get('dois_fatores') == 'true'

    usuario.tempo_auto_logout = int(request.POST.get('tempo_auto_logout', 30))

    usuario.save()
    return JsonResponse({'mensagem': 'Configurações salvas com sucesso!'})

def senha_forte(senha):
    return (
        len(senha) >= 6 and
        re.search(r"[A-Z]", senha) and
        re.search(r"[a-z]", senha) and
        re.search(r"\d", senha)
    )
#O TERMO DE USO DO SISTEMA TEM "VENDAS" LÁ
def index(request):
    logout(request)
    next_url = request.GET.get('next', 'dashboard')  
    if request.method == "POST":
        acao = request.POST.get("acao")

        # LOGIN
        if acao == "login":
            email_input = request.POST.get("email")
            senha_input = request.POST.get("senha")

            user = authenticate(request, email=email_input, password=senha_input)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
                
            else:
                messages.error(request, "Email ou senha inválidos.")

        # CADASTRO
        elif acao == "cadastro":
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            telefone = request.POST.get("telefone")
            preferencia = request.POST.get("notif")
            senha = request.POST.get("senha")
            repetir_senha = request.POST.get("repetir_senha")
            termos = request.POST.get("termos") == "on"

            if senha != repetir_senha:
                messages.error(request, "As senhas não coincidem.")
                return redirect("index")
            
            if not senha_forte(senha):
                messages.error(request, "A senha deve conter no mínimo 6 caracteres, incluindo letras maiúsculas, minúsculas e números.")
                return redirect("index")

            if not termos:
                messages.error(request, "Você deve aceitar os termos de uso.")
                return redirect("index")

            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "Email já cadastrado.")
                return redirect("index")

            user = Usuario.objects.create_user(
                username=email,
                email=email,
                password=senha,
                first_name=nome,
                telefone=telefone,
                preferencia_notificacao=preferencia,
                aceitou_termos=termos
            )
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect("index")

    return render(request, "front/index.html")


@login_required
def tank(request):
    usuario = request.user  

    tanques = Tanque.objects.filter(usuario=usuario)

    total = tanques.count()
    ativos = tanques.filter(situacao='Ativo').count()
    manutencao = tanques.filter(situacao='Manutenção').count()

    capacidade_total = 0
    for t in tanques:
        if t.comprimento and t.largura and t.altura:
            capacidade_total += (t.comprimento * t.largura * t.altura) / 1000

    context = {
        'tanques': tanques,
        'tem_tanques': total > 0,
        'total': total,
        'ativos': ativos,
        'manutencao': manutencao,
        'capacidade_total': round(capacidade_total, 2),  
    }
    return render(request, 'front/tank.html', context)





def pagina_erro_404(request):
    return render(request, 'front/pagina_erro_404.html')
######
@login_required
def dashboard(request):
    return render(request, 'front/dashboard.html')  

def gerenciamento_sensor(request):
    return render(request, 'front/gerenciamento_sensor.html')

def historico_sensor(request):
    return render(request, 'front/historico_sensor.html')

def analise(request):
    return render(request, 'front/analise.html')

def dashboard_content(request):
    return render(request, 'front/dashboard_content.html')
    
def histo_analise(request):
    return render(request, 'front/histo_analise.html')


@login_required(login_url='/index/')
def cadastro_tanque(request):
    usuario = request.user 
    print("Usuário autenticado?", usuario.is_authenticated)

    if request.method == 'POST':
        try:
            nome = request.POST.get('Nome_tanque')
            comprimento = float(request.POST.get('comprimento'))
            largura = float(request.POST.get('largura'))
            altura = float(request.POST.get('altura'))
            tipo = request.POST.get('tipo')
            especie = request.POST.get('especie_cultivada')
            situacao = request.POST.get('situacao')

            capacidade_maxima = request.POST.get('capacidade_maxima')
            capacidade_maxima = int(capacidade_maxima) if capacidade_maxima else None

            temperatura = request.POST.get('temperatura')
            temperatura = float(temperatura) if temperatura else None

            ph = request.POST.get('ph')
            ph = float(ph) if ph else None

            oxigenio = request.POST.get('oxigenio')
            oxigenio = float(oxigenio) if oxigenio else None

            tds = request.POST.get('tds')
            tds = float(tds) if tds else None

            amonia = request.POST.get('amonia')
            amonia = float(amonia) if amonia else None

            nitrito = request.POST.get('nitrito')
            nitrito = float(nitrito) if nitrito else None

            nitrato = request.POST.get('nitrato')
            nitrato = float(nitrato) if nitrato else None

            dureza_geral = request.POST.get('durezageral')
            dureza_geral = float(dureza_geral) if dureza_geral else None

            dureza_carbonatos = request.POST.get('durezacarbonatos')
            dureza_carbonatos = float(dureza_carbonatos) if dureza_carbonatos else None

            salinidade = request.POST.get('salinidade')
            salinidade = float(salinidade) if salinidade else None

            data_instalacao_str = request.POST.get('data_instalacao')
            data_instalacao = (
                datetime.datetime.strptime(data_instalacao_str, '%Y-%m-%d').date()
                if data_instalacao_str else None
            )

            localizacao = request.POST.get('localizacao') or ''
            fonte_agua = request.POST.get('fonte_agua') or ''

            tanque = Tanque.objects.create(
                usuario=usuario,
                nome=nome,
                comprimento=comprimento,
                largura=largura,
                altura=altura,
                capacidade_maxima=capacidade_maxima,
                tipo=tipo,
                especie_cultivada=especie,
                data_instalacao=data_instalacao,
                localizacao=localizacao,
                fonte_agua=fonte_agua,
                situacao=situacao,
                temperatura=temperatura,
                ph=ph,
                oxigenio=oxigenio,
                tds=tds,
                amonia=amonia,
                nitrito=nitrito,
                nitrato=nitrato,
                dureza_geral=dureza_geral,
                dureza_carbonatos=dureza_carbonatos,
                salinidade=salinidade,
            )
            print("Dados recebidos:", request.POST)

            return JsonResponse({'status': 'sucesso'})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return render(request, 'front/cadastro_tanque.html')





def detalhes_tanque_json(request, tanque_id):
    try:
        tanque = Tanque.objects.get(id=tanque_id)
    except Tanque.DoesNotExist:
        raise Http404("Tanque não encontrado")

    sensores = []  # preencha se necessário

    data = {
        "nome": tanque.nome,
        "tipo": tanque.tipo,
        "especie_cultivada": tanque.especie_cultivada,
        "comprimento": tanque.comprimento,
        "largura": tanque.largura,
        "altura": tanque.altura,
        "capacidade_maxima": tanque.capacidade_maxima,
        "localizacao": tanque.localizacao,
        "fonte_agua": tanque.fonte_agua,
        "situacao": tanque.situacao,
        "temperatura": tanque.temperatura,
        "ph": tanque.ph,
        "oxigenio": tanque.oxigenio,
        "tds": tanque.tds,
        "amonia": tanque.amonia,
        "nitrito": tanque.nitrito,
        "nitrato": tanque.nitrato,
        "dureza_geral": tanque.dureza_geral,
        "dureza_carbonatos": tanque.dureza_carbonatos,
        "salinidade": tanque.salinidade,
        "sensores": sensores,
    }

    return JsonResponse(data)

#CRIAR O SISTEMA de AUTPO DESCOBERTA DE SENSORES ESP32 NA REDE WIFI DA PESSOA




def deletar_tanque(request, tanque_id):
    if request.method == "POST":
        tanque = get_object_or_404(Tanque, id=tanque_id)
        tanque.delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Método não permitido'}, status=405)



@login_required
@csrf_exempt
def atualizar_situacao_tanque(request):
    if request.method == 'POST':
        tanque_id = request.POST.get('id')
        nova_situacao = request.POST.get('situacao')

        try:
            tanque = Tanque.objects.get(id=tanque_id, usuario=request.user)
            tanque.situacao = nova_situacao
            tanque.save()

            tanques = Tanque.objects.filter(usuario=request.user)
            ativos = tanques.filter(situacao='Ativo').count()
            manutencao = tanques.filter(situacao='Manutenção').count()

            return JsonResponse({
                'success': True,
                'ativos': ativos,
                'manutencao': manutencao
            })
        except Tanque.DoesNotExist:
            return JsonResponse({'success': False, 'erro': 'Tanque não encontrado.'})
    return JsonResponse({'success': False, 'erro': 'Método inválido'})







def contadores_sensores(request):
    return JsonResponse({
        'total': 0,
        'ativos': 0,
        'esp32': 0,
        'alertas': 0
    })

def escanear_rede(request):
    dispositivos = [
        {'ip': '192.168.0.101'},
        {'ip': '192.168.0.102'},
    ]
    return JsonResponse({'dispositivos': dispositivos})




@login_required
def tanques_do_usuario(request):
    tanques = Tanque.objects.filter(usuario=request.user).values("id", "nome")
    return JsonResponse(list(tanques), safe=False)
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import HistoricoSensor
from django.contrib.auth.decorators import login_required

@login_required
def dados_sensores(request):
    parametro = request.GET.get("parametro")
    dias = int(request.GET.get("dias", 7))
    tanque_id = request.GET.get("tanque_id")

    if not parametro or not tanque_id:
        return JsonResponse({"error": "Parâmetro ou tanque não informado"}, status=400)

    try:
        data_limite = timezone.now() - timedelta(days=dias)

        dados = HistoricoSensor.objects.filter(
            parametro=parametro,
            tanque__id=tanque_id,
            tanque__usuario=request.user,
            data_hora__gte=data_limite
        ).order_by("data_hora")

        lista = [
            {
                "date": dado.data_hora.strftime("%d/%m/%Y %H:%M"),
                "value": dado.valor
            }
            for dado in dados
        ]

        return JsonResponse({"dados": lista})
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # imprime erro completo no terminal
        return JsonResponse({"error": str(e)}, status=500)









def configuracoes_tanque(request, tanque_id):
    tanque = get_object_or_404(Tanque, id=tanque_id)
    
    return render(request, 'front/configuracoes_tanque.html', {
        'tanque': tanque,
        
    })

def salvar_configuracoes_tanque(request, tanque_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tanque = Tanque.objects.get(id=tanque_id)

            tanque.nome = data.get("nome")
            tanque.tipo = data.get("tipo")
            tanque.especie_cultivada = data.get("especie_cultivada")
            tanque.fonte_agua = data.get("fonte_agua")
            tanque.data_instalacao = data.get("data_instalacao") or None
            tanque.localizacao = data.get("localizacao")
            tanque.capacidade_maxima = data.get("capacidade_maxima") or None
            tanque.comprimento = data.get("comprimento") or None
            tanque.largura = data.get("largura") or None
            tanque.altura = data.get("altura") or None
            tanque.situacao = data.get("situacao")
            tanque.temperatura = data.get("temperatura") or None
            tanque.ph = data.get("ph") or None
            tanque.oxigenio = data.get("oxigenio") or None
            tanque.tds = data.get("tds") or None
            tanque.amonia = data.get("amonia") or None
            tanque.nitrito = data.get("nitrito") or None
            tanque.nitrato = data.get("nitrato") or None
            tanque.dureza_geral = data.get("dureza_geral") or None
            tanque.dureza_carbonatos = data.get("dureza_carbonatos") or None
            tanque.salinidade = data.get("salinidade") or None

            tanque.save()

            return JsonResponse({"sucesso": True})
        except Exception as e:
            return JsonResponse({"sucesso": False, "erro": str(e)})

    return JsonResponse({"sucesso": False, "erro": "Requisição inválida"})