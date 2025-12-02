-- Arquivo: meu_database.sql
-- SQL de criação do banco de dados para o desafio (PostgreSQL)

-- Tabela Aluno
CREATE TABLE academia_aluno (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_ingresso DATE NOT NULL
);

-- Tabela Curso
CREATE TABLE academia_curso (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    carga_horaria INTEGER NOT NULL,
    valor_inscricao NUMERIC(8, 2) NOT NULL,
    status VARCHAR(10) NOT NULL
);

-- Tabela Matricula
CREATE TABLE academia_matricula (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    data_matricula DATE NOT NULL,
    status_pagamento VARCHAR(10) NOT NULL,
    
    -- Chaves Estrangeiras
    FOREIGN KEY (aluno_id) REFERENCES academia_aluno (id) ON DELETE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES academia_curso (id) ON DELETE CASCADE,
    
    -- Restrição de unicidade: um aluno só pode se matricular uma vez em um curso
    UNIQUE (aluno_id, curso_id)
);

-- Índices para otimização de consultas
CREATE INDEX idx_aluno_cpf ON academia_aluno (cpf);
CREATE INDEX idx_curso_status ON academia_curso (status);
CREATE INDEX idx_matricula_status ON academia_matricula (status_pagamento);
