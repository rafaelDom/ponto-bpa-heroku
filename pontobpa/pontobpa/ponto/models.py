from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Marcacao(models.Model):
    id_usuario = models.CharField(max_length=40, unique=False)
    nome_usuario = models.CharField(max_length=100, unique=False)
    data_marcacao = models.DateTimeField(default=timezone.now, unique=True)

class MarcacoesPorDia(models.Model):
    id_usuario = ""
    dia_marcacoes = ""
    marcacoes = ()
    nome_funcionario = ""