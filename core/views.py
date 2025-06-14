from django.shortcuts import render

# Create your views here.



def index(request):
    return render(request, 'front/index.html')

def tank(request):
    return render(request, 'front/tank.html')

def pagina_erro_404(request):
    return render(request, 'front/pagina_erro_404.html')

def historico_sensor(request):
    return render(request, 'front/historico_sensor.html')

def gerenciamento_sensor(request):
    return render(request, 'front/gerenciamento_sensor.html')

def dashboard(request):
    return render(request, 'front/dashboard.html')

def analise(request):
    return render(request, 'front/analise.html')