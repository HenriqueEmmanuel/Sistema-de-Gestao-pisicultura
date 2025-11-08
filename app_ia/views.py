from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
import os, tempfile

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
                {"mime_type": "image/jpeg", "data": img_file.read()},
            ])

        texto = resultado.text if resultado else "Não foi possível obter uma resposta."


        # --- 👇 Aqui entra a lógica inteligente de detecção de saúde ---
        texto_lower = texto.lower()

        padroes_saudaveis = [
            "não há anomalias",
            "sem anomalias",
            "não foram observadas anomalias",
            "nenhum sinal de anomalia",
            "aparenta estar saudável",
            "peixe saudável",
            "em boa condição física",
            "sem sinais de anomalia",
            "não há sinais de anomalias",
            "não apresenta anomalias",
            "não são observadas anomalias",
            "aparenta ser saudável",
            "aparenta estar em boas condições"
        ]

        # Verifica se existe algum padrão saudável no texto
        if any(frase in texto_lower for frase in padroes_saudaveis):
            saudavel = True
        else:
            # Se não houver padrões saudáveis, analisa presença isolada de "anomalia"
            # mas ignora frases negativas (ex: "não há anomalia")
            if "anomalia" in texto_lower:
                if "não há" in texto_lower or "sem anomalia" in texto_lower or "não foram observadas" in texto_lower:
                    saudavel = True
                else:
                    saudavel = False
            else:
                # Se nem menciona anomalias, assume saudável
                saudavel = True

        from .models import AnaliseIA

        AnaliseIA.objects.create(
        usuario=request.user,
        imagem=imagem, 
        resultado=texto,
        saudavel=('anomalia' not in texto.lower())
        )

        return JsonResponse({"resultado": texto})
    
    
    return render(request, "analise_ia.html")












from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AnaliseIA

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
