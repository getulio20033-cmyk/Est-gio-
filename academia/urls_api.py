from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AlunoViewSet, CursoViewSet, MatriculaCreateView, MatriculasAlunoListView,
    MatriculaMarcarPagaView, RelatorioMatriculasCursoView, RelatorioTotalDevidoAlunoView,
    RelatorioPagamentosPendentesRawSQLView
)

router = DefaultRouter()
router.register(r'alunos', AlunoViewSet)
router.register(r'cursos', CursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Matrículas
    path('matriculas/criar/', MatriculaCreateView.as_view(), name='matricula-criar'),
    path('matriculas/aluno/<int:aluno_pk>/', MatriculasAlunoListView.as_view(), name='matriculas-aluno'),
    path('matriculas/<int:pk>/marcar-paga/', MatriculaMarcarPagaView.as_view(), name='matricula-marcar-paga'),
    # Relatórios
    path('relatorios/matriculas-curso/', RelatorioMatriculasCursoView.as_view(), name='relatorio-matriculas-curso'),
    path('relatorios/total-devido-aluno/', RelatorioTotalDevidoAlunoView.as_view(), name='relatorio-total-devido-aluno'),
    path('relatorios/pagamentos-pendentes-sql/', RelatorioPagamentosPendentesRawSQLView.as_view(), name='relatorio-pagamentos-pendentes-sql'),
]
