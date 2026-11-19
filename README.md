
# Sistema de Cadastro de Produtos

Projeto acadêmico desenvolvido para as disciplinas de
Projeto de Desenvolvimento de Software I e II.

## Objetivo

Desenvolver um sistema web para gerenciamento de produtos,
utilizando operações CRUD e banco de dados SQLite.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS

## Funcionalidades

1. Cadastrar produtos
2. Listar produtos
3. Pesquisar produtos por nome
4. Editar produtos
5. Excluir produtos

## Como executar

1. Instale o Python.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências:

   py -m pip install -r requirements.txt

4. Execute o sistema:

   py app.py

5. Acesse no navegador:

   http://127.0.0.1:5000

O banco de dados SQLite será criado automaticamente
na primeira execução.

## Banco de dados

Tabela: produtos

Campos:
- id
- nome
- preco
- quantidade
- categoria
