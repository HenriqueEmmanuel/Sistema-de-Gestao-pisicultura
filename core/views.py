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
    capacidade_total = sum(t.volume for t in tanques if t.volume)

    context = {
        'tanques': tanques,
        'tem_tanques': total > 0,
        'total': total,
        'ativos': ativos,
        'manutencao': manutencao,
        'capacidade_total': capacidade_total,
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

        tanque = Tanque(
            nome=request.POST.get('Nome_tanque'),
            volume=request.POST.get('volume'),
            capacidade_maxima=request.POST.get('capacidade_maxima') or None,
            tipo=request.POST.get('tipo'),
            especie_cultivada=request.POST.get('especie_cultivada'),
            data_instalacao=request.POST.get('data_instalacao') or None,
            localizacao=request.POST.get('localizacao'),
            fonte_agua=request.POST.get('fonte_agua'),
            situacao=request.POST.get('situacao'),
            temperatura=request.POST.get('temperatura') or None,
            ph=request.POST.get('ph') or None,
            oxigenio=request.POST.get('oxigenio') or None,
            usuario=usuario
        )
        tanque.save()
        return JsonResponse({'status': 'sucesso'})

    return render(request, 'front/cadastro_tanque.html')







#CRIAR O SISTEMA de AUTPO DESCOBERTA DE SENSORES ESP32 NA REDE WIFI DA PESSOA
