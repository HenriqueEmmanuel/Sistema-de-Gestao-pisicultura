from django.core.mail import send_mail
from twilio.rest import Client
import os

def verificar_limites_e_enviar_alerta(usuario, tanque, dados):
    """
    Verifica todos os parâmetros (padrões ou personalizados) e envia alerta se algo estiver fora do limite.
    """
    limites_padrao = {
        "ph": (6.5, 8.0),
        "temperatura": (26, 30),
        "tds": (500, 1500),
        "amonia": (0, 0.5),
        "oxigeniodissolvido": (5, 9),
        "nitrito": (0, 0.3),
        "nitrato": (0, 50),
        "dureza1": (50, 150),
        "dureza2": (50, 150),
        "salinidade": (0, 5),
    }

    parametros = [
        ("ph", "pH", tanque.phminimo, tanque.phmaximo),
        ("temperatura", "Temperatura (°C)", tanque.temperaturaminima, tanque.temperaturamaxima),
        ("tds", "TDS (ppm)", tanque.tdsminimo, tanque.tdsmaximo),
        ("amonia", "Amônia (mg/L)", tanque.amoniaminima, tanque.amoniamaxima),
        ("oxigeniodissolvido", "Oxigênio Dissolvido (mg/L)", tanque.oxigeniodissolvidominimo, tanque.oxigeniodissolvidomaximo),
        ("nitrito", "Nitrito (NO2-) (mg/L)", tanque.nitritominimo, tanque.nitritomaximo),
        ("nitrato", "Nitrato (NO3-) (mg/L)", tanque.nitratominimo, tanque.nitratomaximo),
        ("dureza1", "Dureza Geral (mg/L)", tanque.dureza1minima, tanque.dureza1maxima),
        ("dureza2", "Dureza de Carbonatos (mg/L)", tanque.dureza2minima, tanque.dureza2maxima),
        ("salinidade", "Salinidade (ppt)", tanque.salinidademinima, tanque.salinidademaxima),
    ]

    alertas = []

    for chave, nome, minimo, maximo in parametros:
        valor = dados.get(chave)
        if valor is None:
            continue

        limite_min = minimo if minimo is not None else limites_padrao[chave][0]
        limite_max = maximo if maximo is not None else limites_padrao[chave][1]

        if valor < limite_min or valor > limite_max:
            alertas.append(f"{nome}: {valor} (limite ideal: {limite_min}–{limite_max})")

    if not alertas:
        return  # tudo normal

    # Monta a mensagem do alerta
    mensagem = (
        f"⚠️ Alerta de parâmetros fora do ideal - Tanque {tanque.nome}\n\n"
        f"Usuário: {usuario.username}\n\n"
        + "\n".join(alertas)
    )

    # Envia e-mail se o usuário escolheu
    if getattr(usuario, "preferencia_notificacao", None) == "email" and usuario.email:
        send_mail(
            subject=f"⚠️ Alerta no tanque {tanque.nome}",
            message=mensagem,
            from_email=None,
            recipient_list=[usuario.email],
            fail_silently=True,
        )

    # Envia SMS se o usuário escolheu
    if getattr(usuario, "preferencia_notificacao", None) == "sms" and getattr(usuario, "telefone", None):
        try:
            client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
            client.messages.create(
                body=mensagem,
                from_="+1234567890",
                to=usuario.telefone
            )
        except Exception as e:
            print("Erro ao enviar SMS:", e)
