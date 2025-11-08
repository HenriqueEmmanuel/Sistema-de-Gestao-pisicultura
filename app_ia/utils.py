import google.generativeai as genai
import base64
import os
from django.conf import settings

def analisar_imagem_ia(imagem):
    """Analisa imagem de tilápia usando o modelo Gemini."""
    # Configura a API com a chave carregada do .env
    genai.configure(api_key=settings.GEMINI_API_KEY)

    # Lê e converte a imagem
    imagem_bytes = imagem.read()
    imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')

    # Prepara o modelo
    modelo = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "Analise se a imagem enviada é um peixe. "
        "Se for um peixe garanta que seja uma tilápia e indentifique a especie dela. "
        "Verifique se há anomalias visuais como feridas, manchas, fungos, deformações ou palidez. "
        "Descreva o estado geral e indique se há possíveis sinais de doenças."
    )

    # Cria o input multimodal (texto + imagem)
    resposta = modelo.generate_content([
        prompt,
        {"mime_type": "image/jpeg", "data": imagem_bytes}
    ])

    return resposta.text if resposta else "Não foi possível analisar a imagem."
