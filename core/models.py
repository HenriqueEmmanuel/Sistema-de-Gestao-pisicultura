from django.db import models

# Create your models here.


    #Tabela de usuario
class Usuario(models.Model):
    NOTIFICACAO_CHOICES = [
        ('Email', 'Email'),
        ('SMS', 'SMS'),
        ('Email e SMS', 'Email e SMS'),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    preferencia_notificacao = models.CharField(max_length=20, choices=NOTIFICACAO_CHOICES)
    senha = models.CharField(max_length=128)  # criptografada
    aceitou_termos = models.BooleanField(default=False)

    def __str__(self):
        return self.nome








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

    def __str__(self):
        return f"{self.nome} ({self.tipo})"
