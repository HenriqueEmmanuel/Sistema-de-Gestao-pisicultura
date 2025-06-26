from django.shortcuts import render

# Create your views here.
from .models import bancodedados  # quando criuar o banco coloca aqui



def index(request):
    return render(request, 'front/index.html')

def tank(request):
    return render(request, 'front/tank.html')
    tanques = Tanque.objects.all()
    context = {'tem_tanques': tanques.exists(), 'tanques': tanques}
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

def cadastro_tanque(request):
    return render(request, 'front/cadastro_tanque.html')






#CRIAR O SISTEMA de AUTPO DESCOBERTA DE SENSORES ESP32 NA REDE WIFI DA PESSOA
