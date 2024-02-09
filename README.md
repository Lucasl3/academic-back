# AcademIC - BACKED

Este é um guia passo a passo para configurar e executar o projeto.

## Pré-requisitos

- Python 3
- Docker
- Make (opcional)

## Configuração do Ambiente

1. Crie um ambiente virtual e ative-o.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências do projeto.

```bash
pip install -r requirements.txt
```

## Executando o Projeto

1. Inicie o banco de dados.

```bash
make db
```


2. Execute as migrações.

```bash
make migrate
```

3. Carregue os dados iniciais.

```bash
make data
```

4. Execute o servidor.

```bash
make run
```

5. Caso faça alguma mudança nos modelos, crie as migrações antes de persistir os dados no banco (antes do passo 2).

```bash
make makemigrations
```

Agora, você deve ser capaz de acessar o projeto em `localhost:8000`.


## Parando o Projeto

Para parar o projeto, você pode usar o seguinte comando:

```bash
make down
```

Isso irá parar e remover os contêineres do Docker.


OBS: Caso não queira instalar o make, olhe os comandos dentro do arquivo 'Makefile'.