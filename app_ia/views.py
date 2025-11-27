from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os, tempfile
from django.contrib.auth.decorators import login_required
from .models import AnaliseIA

def analise_ia(request):
    if request.method == "POST" and request.FILES.get("imagem"):
        imagem = request.FILES["imagem"]

        temp_dir = tempfile.gettempdir()
        caminho_temp = os.path.join(temp_dir, imagem.name)

        with open(caminho_temp, "wb") as f:
            for chunk in imagem.chunks():
                f.write(chunk)

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash")

        with open(caminho_temp, "rb") as img_file:
            resultado = model.generate_content([
                "Analise a imagem e descreva se há sinais de anomalias visuais na tilápia.",
                {"mime_type": "image/jpeg", "data": img_file.read()}
            ])

        texto = resultado.text if resultado else "Não foi possível obter uma resposta."
        texto_lower = texto.lower()

        padroes_anomalia = [
            "exoftalmia",
            "pop-eye",
            "olho saltado",
            "escamas levantadas",
            "perda de escamas",
            "manchas brancas",
            "fungo",
            "fúngica",
            "parasit",
            "lesões",
            "deformidade",
            "infecção",
            "saúde comprometida",
            "doença"
        ]

        padroes_saudaveis = [
            "não há anomalias",
            "sem anomalias",
            "nenhum sinal de anomalia",
            "aparenta estar saudável",
            "peixe saudável",
            "em boa condição física",
            "não apresenta anomalias",
            "em boas condições"
        ]

        anomalia_detectada = any(p in texto_lower for p in padroes_anomalia)

        if not anomalia_detectada:
            saudavel = any(frase in texto_lower for frase in padroes_saudaveis)
        else:
            saudavel = False  

        AnaliseIA.objects.create(
            usuario=request.user,
            imagem=imagem,
            resultado=texto,
            saudavel=saudavel
        )

        try:
            os.remove(caminho_temp)
        except:
            pass

        return JsonResponse({
            "resultado": texto,
            "saudavel": saudavel,
            "anomalia_detectada": anomalia_detectada
        })

    return render(request, "analise_ia.html")










@login_required
def historico_analise(request):
    analises = AnaliseIA.objects.filter(usuario=request.user).order_by('-data')
    

    total = analises.count()
    saudaveis = analises.filter(saudavel=True).count()
    anomalias = analises.filter(saudavel=False).count()

    contexto = {
        'analises': analises,
        'total': total,
        'saudaveis': saudaveis,
        'anomalias': anomalias,
    }
    return render(request, 'front/historico_analise.html', contexto)
