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

class ParametrosPersonalizados(models.Model):
    tanque = models.OneToOneField(Tanque, on_delete=models.CASCADE, related_name="parametros_personalizados")

    ph_minimo = models.FloatField(null=True, blank=True)
    ph_maximo = models.FloatField(null=True, blank=True)
    amonia_minima = models.FloatField(null=True, blank=True)
    amonia_maxima = models.FloatField(null=True, blank=True)
    temperatura_minima = models.FloatField(null=True, blank=True)
    temperatura_maxima = models.FloatField(null=True, blank=True)
    oxigenio_dissolvido_minimo = models.FloatField(null=True, blank=True)
    oxigenio_dissolvido_maximo = models.FloatField(null=True, blank=True)
    tds_minimo = models.FloatField(null=True, blank=True)
    tds_maximo = models.FloatField(null=True, blank=True)
    nitrito_minimo = models.FloatField(null=True, blank=True)
    nitrito_maximo = models.FloatField(null=True, blank=True)
    nitrato_minimo = models.FloatField(null=True, blank=True)
    nitrato_maximo = models.FloatField(null=True, blank=True)
    dureza_geral_minima = models.FloatField(null=True, blank=True)
    dureza_geral_maxima = models.FloatField(null=True, blank=True)
    dureza_carbonatos_minima = models.FloatField(null=True, blank=True)
    dureza_carbonatos_maxima = models.FloatField(null=True, blank=True)
    salinidade_minima = models.FloatField(null=True, blank=True)
    salinidade_maxima = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Parâmetros personalizados de {self.tanque.nome}"





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
    


#banco de financeiro
class Transacao(models.Model):
    TIPO_CHOICES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    CATEGORIAS_DESPESA = [
        ('custo_variavel', 'Custos Variáveis'),
        ('custo_fixo', 'Custos Fixos'),
        ('despesa_operacional', 'Despesas Operacionais'),
    ]

    SUBCATEGORIAS_DESPESA = {
        'custo_variavel': [
            ('racal', 'Ração'),
            ('alevinos', 'Alevinos'),
            ('vacina_medicamentos', 'Vacina/Medicamentos'),
            ('energia_eletrica', 'Energia Elétrica'),
            ('transporte', 'Transporte'),
            ('insumos', 'Insumos'),
        ],
        'custo_fixo': [
            ('manut_equipamentos', 'Manutenção de equipamentos'),
            ('manut_instalacoes', 'Manutenção de instalações'),
        ],
        'despesa_operacional': [
            ('salarios_encargos', 'Salários/Encargos'),
            ('impostos_taxas', 'Impostos/Taxas'),
            ('desp_administrativas', 'Despesas administrativas'),
            ('outros', 'Outros'),
        ],
    }

    CATEGORIAS_RECEITA = [
        ('venda_peixes', 'Venda de Peixes'),
        ('consultoria', 'Consultoria'),
        ('outros', 'Outros'),
    ]

    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='transacoes')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    categoria = models.CharField(max_length=50)
    subcategoria = models.CharField(max_length=50, blank=True, null=True)

    descricao = models.TextField(blank=True, null=True)
    quantidade = models.FloatField(blank=True, null=True)
    preco_unitario = models.FloatField(blank=True, null=True)

    tanque = models.ForeignKey('Tanque', on_delete=models.SET_NULL, blank=True, null=True, related_name='transacoes')
    valor = models.FloatField()
    observacoes = models.TextField(blank=True, null=True)

    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.categoria} ({self.subcategoria}) - R$ {self.valor}"

    def get_categoria_display(self):
        if self.tipo == 'despesa':
            for key, label in self.CATEGORIAS_DESPESA:
                if key == self.categoria:
                    return label
        elif self.tipo == 'receita':
            for key, label in self.CATEGORIAS_RECEITA:
                if key == self.categoria:
                    return label
        return self.categoria

    def get_subcategoria_display(self):
        if self.tipo == 'despesa' and self.subcategoria:
            subcats = self.SUBCATEGORIAS_DESPESA.get(self.categoria, [])
            for key, label in subcats:
                if key == self.subcategoria:
                    return label
        return self.subcategoria
