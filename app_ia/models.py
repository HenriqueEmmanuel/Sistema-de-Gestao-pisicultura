from django.db import models

# Create your models here.
from django.conf import settings

class AnaliseIA(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='analises_ia/')
    resultado = models.TextField()
    saudavel = models.BooleanField(default=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análise {self.id} - {'Saudável' if self.saudavel else 'Anômala'}"
