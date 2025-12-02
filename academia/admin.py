from django.contrib import admin
from .models import Aluno, Curso, Matricula

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'data_ingresso')
    search_fields = ('nome', 'cpf')
    list_filter = ('data_ingresso',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'carga_horaria', 'valor_inscricao', 'status')
    list_filter = ('status',)
    search_fields = ('nome',)

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula', 'status_pagamento')
    list_filter = ('status_pagamento', 'curso')
    search_fields = ('aluno__nome', 'curso__nome')
    raw_id_fields = ('aluno', 'curso')
    actions = ['marcar_paga']

    def marcar_paga(self, request, queryset):
        total = queryset.update(status_pagamento='pago')
        self.message_user(request, f'{total} matrícula(s) marcada(s) como paga(s).')
    marcar_paga.short_description = 'Marcar como paga'
