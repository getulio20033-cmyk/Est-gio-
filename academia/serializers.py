from rest_framework import serializers
from .models import Aluno, Curso, Matricula

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'email', 'cpf', 'data_ingresso']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'nome', 'carga_horaria', 'valor_inscricao', 'status']

class MatriculaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.ReadOnlyField(source='aluno.nome')
    curso_nome = serializers.ReadOnlyField(source='curso.nome')

    class Meta:
        model = Matricula
        fields = ['id', 'aluno', 'aluno_nome', 'curso', 'curso_nome', 'data_matricula', 'status_pagamento']
        read_only_fields = ['aluno_nome', 'curso_nome']

class MatriculaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ['status_pagamento']

class RelatorioMatriculasCursoSerializer(serializers.Serializer):
    curso_nome = serializers.CharField(max_length=100)
    total_matriculas = serializers.IntegerField()

class RelatorioTotalDevidoAlunoSerializer(serializers.Serializer):
    aluno_nome = serializers.CharField(max_length=100)
    total_devido = serializers.DecimalField(max_digits=10, decimal_places=2)

class RelatorioPagamentosPendentesSerializer(serializers.Serializer):
    total_pendente = serializers.IntegerField()
