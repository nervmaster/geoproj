from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Minerio(models.Model):
    minerio = models.CharField(max_length = 64)

class Chapa(models.Model):
    minerio = models.ForeignKey(Minerio)
    lamina = models.CharField(max_length = 32)
    codigo = models.CharField(max_length = 32)
    textura = models.CharField(max_length = 32)
    aumento = models.IntegerField()
    cor = models.CharField(max_length = 32)
    tamanho = models.CharField(max_length = 32)
    posicao_x = models.FloatField()
    posicao_y = models.FloatField()
    relevo = models.CharField(max_length = 128)
    formato_cristal = models.CharField(max_length = 128)
    clivagem = models.BooleanField()
    fratura = models.BooleanField()
    minerios_contato = models.CharField(max_length = 128)
    extincao = models.CharField(max_length = 64)
    comentario = models.CharField(max_length = 512)
    
class Fotos(models.Model):
    chapa = models.ForeignKey(Chapa)
    imagem = models.FileField(upload_to='minerios')
    angulo = models.FloatField()
    luz = models.BooleanField()

