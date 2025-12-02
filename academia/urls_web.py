from django.urls import path
from .views import HomeView, HistoricoAlunoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('aluno/<int:aluno_pk>/historico/', HistoricoAlunoView.as_view(), name='historico-aluno'),
]
