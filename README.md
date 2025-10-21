# clinic-crud-api

Este projeto é uma API para gerenciamento de pacientes, profissionais e consultas médicas, construída com FastAPI, SQLAlchemy e Pydantic. Permite criar, atualizar, listar e consultar recursos, garantindo validação de dados e integração com banco de dados.

*versão do python: 3.12.0*

## Backend - Funcionalidades
**Pacientes**

* Criar, atualizar, deletar e consultar informações de pacientes
* Campos: nome, data de nascimento, gênero, cpf, email, convênio, número da carteirinha do convênio, contato de emergência, doador de órgãos

**Profissionais (Médicos/Terapeutas)**
* Criar, atualizar, deletar e consultar provedores
* Campos: nome, especialidade, turno de trabalho, número da licença

**Consultas**
* Criar, atualizar, listar e consultar agendamentos

* Campos: paciente, provedor, data/hora, status, motivo, observações

**Usuários**
* Autenticação básica com OAuth2 e token JWT
* Criação de contas de usuários administrativos

**Modelagem do banco de dados**
![Modelagem](/db_model.png "Modelagem")

## Front-end
*Em breve*

## Executando o Projeto com Docker

Antes de tudo, clone este repositório:
```bash
git clone https://github.com/alice7lima/clinic-crud-api.git
```

O projeto possui três serviços: back-end, banco de dados e front-end, estes estão declarados no docker-compose. Antes de executar o projeto, certifique-se de preencher o arquivo `.env` com suas variáveis de ambiente, seguindo o padrão indicado no arquivo `.env-example`.

Para subir os containers dos serviços, execute o comando abaixo no diretório raiz do projeto:
```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`, e a documentação interativa (Swagger) do FastAPI poderá ser acessada em `http://localhost:8000/docs`.

Acesse o banco utilizando a ferramenta de sua preferência, informando as credenciais declaradas no `.env`.
