# Desafio Vaga Estágio Dev Python :: 2026.1

**Autor:** Getulio Dantas

Sistema web para gerenciar alunos, cursos e matrículas da Academia Dev Python. Desenvolvido com Django, Django Rest Framework, PostgreSQL e Docker.

## O que precisa ter instalado

- Docker
- Docker Compose

## Como rodar

1. Clone o repositório:
```bash
git clone https://github.com/getulio20033-cmyk/Est-gio-.git
cd academia_dev_python
```

2. Suba os containers:
```bash
docker-compose up --build
```

Aguarde até aparecer a mensagem: `Starting development server at http://0.0.0.0:8000/`

## Acessando o sistema

- **Dashboard:** http://localhost:8000/
- **Admin do Django:** http://localhost:8000/admin/
- **API REST:** http://localhost:8000/api/

Para criar um usuário admin:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Endpoints da API

A API REST está disponível em `/api/` e possui os seguintes endpoints:

- `/api/alunos/` - CRUD completo de alunos
- `/api/cursos/` - CRUD completo de cursos
- `/api/matriculas/` - Criar matrícula
- `/api/matriculas/aluno/<id>/` - Listar matrículas de um aluno
- `/api/matriculas/<id>/marcar-paga/` - Marcar matrícula como paga
- `/api/relatorios/matriculas-por-curso/` - Total de matrículas por curso
- `/api/relatorios/total-devido-aluno/` - Total devido por aluno
- `/api/relatorios/pagamentos-pendentes-sql/` - Exemplo com SQL bruto

## Banco de Dados

O arquivo `meu_database.sql` contém o script SQL de criação das tabelas do banco de dados.

## Frontend

O frontend foi feito com Django Templates e possui:

- Dashboard com resumo geral do sistema
- Página de histórico detalhado do aluno com informações financeiras e cursos matriculados

## Estrutura do Projeto

```
academia_dev_python/
├── academia/           # App principal
│   ├── models.py      # Modelos (Aluno, Curso, Matricula)
│   ├── views.py       # Views da API e frontend
│   ├── serializers.py # Serializers do DRF
│   ├── admin.py       # Configuração do Django Admin
│   └── urls_*.py      # URLs da API e web
├── core/              # Configurações do Django
├── templates/         # Templates HTML
├── docker-compose.yml # Configuração Docker
├── Dockerfile         # Imagem Docker
├── requirements.txt   # Dependências Python
└── meu_database.sql   # Script SQL do banco
```

## Tecnologias Utilizadas

- Python 3.11
- Django 4.2
- Django Rest Framework
- PostgreSQL 15
- Docker & Docker Compose
