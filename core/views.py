import datetime
import json
from django.http import HttpResponseForbidden, JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Tanque, Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

def sair(request):
    logout(request)
    return redirect('index')



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
    print("Usuário autenticado?", request.user.is_authenticated)

    if request.method == 'POST':
        try:
            nome = request.POST.get('Nome_tanque')
            comprimento = float(request.POST.get('comprimento'))
            largura = float(request.POST.get('largura'))
            altura = float(request.POST.get('altura'))
            tipo = request.POST.get('tipo')
            especie = request.POST.get('especie_cultivada')
            situacao = request.POST.get('situacao')
        #opicionais
            capacidade_maxima = request.POST.get('capacidade_maxima')
            capacidade_maxima = int(capacidade_maxima) if capacidade_maxima else None

            temperatura = request.POST.get('temperatura')
            temperatura = float(temperatura) if temperatura else None

            ph = request.POST.get('ph')
            ph = float(ph) if ph else None

            oxigenio = request.POST.get('oxigenio')
            oxigenio = float(oxigenio) if oxigenio else None

            data_instalacao_str = request.POST.get('data_instalacao')
            data_instalacao = (
                datetime.datetime.strptime(data_instalacao_str, '%Y-%m-%d').date()
                if data_instalacao_str else None
            )


            localizacao = request.POST.get('localizacao') or ''
            fonte_agua = request.POST.get('fonte_agua') or ''

            # Criação do tanque
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
            )

            return JsonResponse({'status': 'sucesso'})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return render(request, 'front/cadastro_tanque.html')





def detalhes_tanque_json(request, tanque_id):
    try:
        tanque = Tanque.objects.get(id=tanque_id)
    except Tanque.DoesNotExist:
        raise Http404("Tanque não encontrado")

    sensores = []  

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














def configuracoes_tanque(request, tanque_id):
    tanque = get_object_or_404(Tanque, id=tanque_id)
    
    return render(request, 'front/configuracoes_tanque.html', {
        'tanque': tanque,
        
    })

@csrf_exempt
def salvar_configuracoes_tanque(request, tanque_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            tanque = get_object_or_404(Tanque, id=tanque_id)

            # Atualiza os campos
            tanque.nome = data.get('nome', tanque.nome)
            tanque.tipo = data.get('tipo', tanque.tipo)
            tanque.especie = data.get('especie', tanque.especie)
            tanque.fonte_agua = data.get('fonte_agua', tanque.fonte_agua)
            tanque.data_instalacao = data.get('data_instalacao') or tanque.data_instalacao

            # Converte para float para evitar erros com valores vazios
            try:
                tanque.comprimento = float(data.get('comprimento', tanque.comprimento))
            except (TypeError, ValueError):
                pass
            try:
                tanque.largura = float(data.get('largura', tanque.largura))
            except (TypeError, ValueError):
                pass
            try:
                tanque.altura = float(data.get('altura', tanque.altura))
            except (TypeError, ValueError):
                pass

            tanque.situacao = data.get('situacao', tanque.situacao)

            tanque.save()

            # Você pode querer atualizar também os parâmetros da água aqui, se desejar.

            return JsonResponse({'sucesso': True})
        except Exception as e:
            return JsonResponse({'sucesso': False, 'erro': str(e)})
    else:
        return JsonResponse({'erro': 'Método não permitido'}, status=405)