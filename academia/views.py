from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, F
from django.db import connection
from django.shortcuts import render
from django.views import View

from .models import Aluno, Curso, Matricula
from .serializers import (
    AlunoSerializer, CursoSerializer, MatriculaSerializer, MatriculaUpdateSerializer,
    RelatorioMatriculasCursoSerializer, RelatorioTotalDevidoAlunoSerializer, RelatorioPagamentosPendentesSerializer
)

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class MatriculaCreateView(APIView):
    def post(self, request):
        serializer = MatriculaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatriculasAlunoListView(APIView):
    def get(self, request, aluno_pk):
        try:
            aluno = Aluno.objects.get(pk=aluno_pk)
        except Aluno.DoesNotExist:
            return Response({"detail": "Aluno não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        matriculas = Matricula.objects.filter(aluno=aluno)
        serializer = MatriculaSerializer(matriculas, many=True)
        return Response(serializer.data)

class MatriculaMarcarPagaView(APIView):
    def patch(self, request, pk):
        try:
            matricula = Matricula.objects.get(pk=pk)
        except Matricula.DoesNotExist:
            return Response({"detail": "Matrícula não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        data = {'status_pagamento': 'pago'}
        serializer = MatriculaUpdateSerializer(matricula, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RelatorioMatriculasCursoView(APIView):
    def get(self, request):
        relatorio = Curso.objects.annotate(
            total_matriculas=Count('matriculas')
        ).values('nome', 'total_matriculas').order_by('-total_matriculas')

        data = [{'curso_nome': item['nome'], 'total_matriculas': item['total_matriculas']} for item in relatorio]
        serializer = RelatorioMatriculasCursoSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)

class RelatorioTotalDevidoAlunoView(APIView):
    def get(self, request):
        relatorio = Aluno.objects.filter(
            matriculas__status_pagamento='pendente'
        ).annotate(
            total_devido=Sum('matriculas__curso__valor_inscricao')
        ).values('nome', 'total_devido').order_by('-total_devido')

        data = [{'aluno_nome': item['nome'], 'total_devido': item['total_devido']} for item in relatorio]
        serializer = RelatorioTotalDevidoAlunoSerializer(data=data, many=True)
        serializer.is_valid()
        return Response(serializer.data)

class RelatorioPagamentosPendentesRawSQLView(APIView):
    def get(self, request):
        sql_query = """
            SELECT
                COUNT(T1.id) AS total_pendente
            FROM
                academia_matricula T1
            INNER JOIN
                academia_curso T2 ON T1.curso_id = T2.id
            WHERE
                T1.status_pagamento = 'pendente'
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            row = cursor.fetchone()

        data = {'total_pendente': row[0]}
        serializer = RelatorioPagamentosPendentesSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.data)

class HomeView(View):
    def get(self, request):
        context = {
            'total_alunos': Aluno.objects.count(),
            'cursos_ativos': Curso.objects.filter(status='ativo').count(),
            'matriculas_pagas': Matricula.objects.filter(status_pagamento='pago').count(),
            'matriculas_pendentes': Matricula.objects.filter(status_pagamento='pendente').count(),
        }
        return render(request, 'academia/dashboard.html', context)

class HistoricoAlunoView(View):
    def get(self, request, aluno_pk):
        try:
            aluno = Aluno.objects.get(pk=aluno_pk)
        except Aluno.DoesNotExist:
            return render(request, 'academia/aluno_nao_encontrado.html', status=404)

        matriculas = Matricula.objects.filter(aluno=aluno).select_related('curso')
        total_devido = matriculas.filter(status_pagamento='pendente').aggregate(
            total=Sum('curso__valor_inscricao')
        )['total'] or 0
        total_pago = matriculas.filter(status_pagamento='pago').aggregate(
            total=Sum('curso__valor_inscricao')
        )['total'] or 0

        context = {
            'aluno': aluno,
            'matriculas': matriculas,
            'total_devido': total_devido,
            'total_pago': total_pago,
        }
        return render(request, 'academia/historico_aluno.html', context)
