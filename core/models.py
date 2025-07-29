from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


    #Tabela de usuario
class Usuario(AbstractUser):
    NOTIFICACAO_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Email e SMS', 'Email e SMS'),
    ]

    TEMPERATURA_CHOICES = [
        ('C', 'Celsius (°C)'),
        ('F', 'Fahrenheit (°F)'),
    ]

    DATA_CHOICES = [
        ('DD/MM/AAAA', 'DD/MM/AAAA'),
        ('MM/DD/AAAA', 'MM/DD/AAAA'),
        ('AAAA/MM/DD', 'AAAA/MM/DD'),
    ]

    MOEDA_CHOICES = [
        ('R$', 'Real (R$)'),
        ('$', 'Dólar ($)'),
        ('€', 'Euro (€)'),
    ]

    IDIOMA_CHOICES = [
        ('pt-BR', 'Português (Brasil)'),
        ('en-US', 'English (US)'),
        ('es', 'Español'),
    ]

    BACKUP_CHOICES = [
        ('Diário', 'Diário'),
        ('Semanal', 'Semanal'),
        ('Mensal', 'Mensal'),
    ]

    telefone = models.CharField(max_length=20, blank=True)
    preferencia_notificacao = models.CharField(max_length=20, choices=NOTIFICACAO_CHOICES, blank=True)
    aceitou_termos = models.BooleanField(default=False)

    nome_fazenda = models.CharField(max_length=100, blank=True)
    endereco_fazenda = models.CharField(max_length=255, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)

    notificacoes_push = models.BooleanField(default=False)
    notificacoes_email = models.BooleanField(default=False)
    alertas_agua = models.BooleanField(default=False)
    lembretes_alimentacao = models.BooleanField(default=False)

    temperatura = models.CharField(max_length=1, choices=TEMPERATURA_CHOICES, default='C')
    formato_data = models.CharField(max_length=12, choices=DATA_CHOICES, default='DD/MM/AAAA')
    moeda = models.CharField(max_length=3, choices=MOEDA_CHOICES, default='R$')
    idioma = models.CharField(max_length=10, choices=IDIOMA_CHOICES, default='pt-BR')

    backup_automatico = models.BooleanField(default=False)
    frequencia_backup = models.CharField(max_length=10, choices=BACKUP_CHOICES, default='Semanal')

    autenticacao_dois_fatores = models.BooleanField(default=False)
    tempo_auto_logout = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.email








    #Tabela do Cadastro de tanques (Cadastro_tanques.html)
class Tanque(models.Model):
    TIPO_CHOICES = [
        ('Escavado', 'Escavado'),
        ('Tanque-rede', 'Tanque-rede'),
        ('Alvenaria', 'Alvenaria'),
        ('Fibra de vidro', 'Fibra de vidro'),
        ('Outro', 'Outro'),
    ]

    ESPECIE_CHOICES = [
        ('Tilápia do Nilo (Oreochromis niloticus)', 'Tilápia do Nilo'),
        ('Tilápia Azul (Oreochromis aureus)', 'Tilápia Azul'),
        ('Tilápia de Moçambique (Oreochromis mossambicus)', 'Tilápia de Moçambique'),
        ('Tilápia de Zanzibar (Oreochromis hornorum)', 'Tilápia de Zanzibar'),
        ('Outro', 'Outro'),
    ]

    FONTE_CHOICES = [
        ('Nascente', 'Nascente'),
        ('Poço artesiano', 'Poço artesiano'),
        ('Rio', 'Rio'),
        ('Abastecimento público', 'Abastecimento público'),
        ('Outro', 'Outro'),
    ]

    SITUACAO_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Manutenção', 'Manutenção'),
        ('Inativo', 'Inativo'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tanques")
    nome = models.CharField(max_length=100)

    comprimento = models.FloatField()
    largura = models.FloatField()
    altura = models.FloatField()

    capacidade_maxima = models.PositiveIntegerField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    especie_cultivada = models.CharField(max_length=80, choices=ESPECIE_CHOICES)
    data_instalacao = models.DateField(null=True, blank=True)
    localizacao = models.CharField(max_length=255, blank=True)
    fonte_agua = models.CharField(max_length=30, choices=FONTE_CHOICES, blank=True)
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES)

    temperatura = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    oxigenio = models.FloatField(null=True, blank=True)
    tds = models.FloatField(null=True, blank=True)
    amonia = models.FloatField(null=True, blank=True)
    nitrito = models.FloatField(null=True, blank=True)
    nitrato = models.FloatField(null=True, blank=True)
    dureza_geral = models.FloatField(null=True, blank=True)
    dureza_carbonatos = models.FloatField(null=True, blank=True)
    salinidade = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.nome} ({self.tipo})"






class HistoricoSensor(models.Model):
    PARAMETROS = [
        ('temperatura', 'Temperatura'),
        ('ph', 'pH'),
        ('amonia', 'Amônia'),
        ('oxigenio', 'Oxigênio'),
        ('tds', 'TDS'),
        ('nitrito', 'Nitrito'),
        ('nitrato', 'Nitrato'),
        ('dureza_geral', 'Dureza Geral'),
        ('dureza_carbonatos', 'Dureza Carbonatos'),
        ('salinidade', 'Salinidade'),
    ]

    tanque = models.ForeignKey(Tanque, on_delete=models.CASCADE, related_name="historicos")
    parametro = models.CharField(max_length=30, choices=PARAMETROS)
    valor = models.FloatField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parametro} - {self.valor} ({self.data_hora.strftime('%d/%m/%Y')})"