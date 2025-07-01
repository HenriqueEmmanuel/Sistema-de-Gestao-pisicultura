import datetime
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Tanque, Usuario
from django.contrib.auth.decorators import login_required


#O TERMO DE USO DO SISTEMA TEM "VENDAS" LÁ
def index(request):
    if request.method == "POST":
        acao = request.POST.get("acao")

        # LOGIN
        if acao == "login":
            email_input = request.POST.get("email")
            senha_input = request.POST.get("senha")

            try:
                usuario = Usuario.objects.get(email=email_input)
                if check_password(senha_input, usuario.senha):
                    request.session['usuario_id'] = usuario.id
                    return redirect("dashboard")
                else:
                    messages.error(request, "Senha incorreta.")
            except Usuario.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")

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
                return redirect("front/index")

            if not termos:
                messages.error(request, "Você deve aceitar os termos de uso.")
                return redirect("front/index")

            if Usuario.objects.filter(email=email).exists():
                messages.error(request, "Email já cadastrado.")
                return redirect("front/index")

            usuario = Usuario(
                nome=nome,
                email=email,
                telefone=telefone,
                preferencia_notificacao=preferencia,
                senha=make_password(senha),
                aceitou_termos=termos
            )
            usuario.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect("index")

    return render(request, "front/index.html")



def tank(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('front/index')
    
    usuario = Usuario.objects.get(id=usuario_id)
    tanques = Tanque.objects.filter(usuario=usuario)

    total = tanques.count()
    ativos = tanques.filter(situacao='Ativo').count()
    manutencao = tanques.filter(situacao='Manutenção').count()

    capacidade_total = 0
    for t in tanques:
        if t.comprimento and t.largura and t.altura:
            # volume em litros = (comprimento * largura * altura) / 1000
            capacidade_total += (t.comprimento * t.largura * t.altura) / 1000

    context = {
        'tanques': tanques,
        'tem_tanques': total > 0,
        'total': total,
        'ativos': ativos,
        'manutencao': manutencao,
        'capacidade_total': round(capacidade_total, 2),  # arredondar para 2 casas decimais
    }
    return render(request, 'front/tank.html', context)





def pagina_erro_404(request):
    return render(request, 'front/pagina_erro_404.html')
######
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

def cadastro_tanque(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponseForbidden("Você precisa estar logado.")
        return redirect('front/index')

    if request.method == 'POST':
        usuario = Usuario.objects.get(id=usuario_id)

        try:
            # Campos obrigatórios
            nome = request.POST.get('Nome_tanque')
            comprimento = float(request.POST.get('comprimento'))
            largura = float(request.POST.get('largura'))
            altura = float(request.POST.get('altura'))
            tipo = request.POST.get('tipo')
            especie = request.POST.get('especie_cultivada')
            situacao = request.POST.get('situacao')

            # Campos opcionais com conversão segura
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



# views.py
from django.http import JsonResponse, Http404
from .models import Tanque

def detalhes_tanque_json(request, tanque_id):
    try:
        tanque = Tanque.objects.get(id=tanque_id)
    except Tanque.DoesNotExist:
        raise Http404("Tanque não encontrado")

    sensores = []  # Ajuste aqui para pegar sensores relacionados, se tiver modelo Sensores
    # Exemplo se sensores forem uma relação:
    # sensores = list(tanque.sensores.all().values('nome', 'tipo'))

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

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def deletar_tanque(request, tanque_id):
    if request.method == "POST":
        try:
            tanque = get_object_or_404(Tanque, id=tanque_id)
            tanque.delete()
            return JsonResponse({"status": "ok", "mensagem": "Tanque excluído com sucesso!"})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)
    else:
        return JsonResponse({"status": "erro", "mensagem": "Método não permitido"}, status=405)