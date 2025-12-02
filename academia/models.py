from django.db import models
from django.utils.timezone import now
from datetime import date

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_ingresso = models.DateField(default=date.today)

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    def __str__(self):
        return self.nome

class Curso(models.Model):
    STATUS_CHOICES = (
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    )

    nome = models.CharField(max_length=100, unique=True)
    carga_horaria = models.IntegerField()
    valor_inscricao = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo')

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.nome

class Matricula(models.Model):
    STATUS_PAGAMENTO_CHOICES = (
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
    )

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='matriculas')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='matriculas')
    data_matricula = models.DateField(default=date.today)
    status_pagamento = models.CharField(max_length=10, choices=STATUS_PAGAMENTO_CHOICES, default='pendente')

    class Meta:
        verbose_name = "Matrícula"
        verbose_name_plural = "Matrículas"
        unique_together = ('aluno', 'curso')

    def __str__(self):
        return f"Matrícula de {self.aluno.nome} em {self.curso.nome}"
