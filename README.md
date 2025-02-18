# Bank API

Este é o README para o projeto Bank API. Siga os passos abaixo para configurar e rodar o projeto em sua máquina local.

## Pré-requisitos

- [Python](https://www.python.org/) (versão 3.8 ou superior)
- [Poetry](https://python-poetry.org/) (gerenciador de dependências e pacotes para Python)
- [Docker](https://www.docker.com/) (para containerização)
- [Git](https://git-scm.com/) (para clonar o repositório)

## Passo a passo

### 1. Clone o repositório

```bash
git clone https://github.com/eduviictor/bank_api.git
cd bank_api
```

### 2. Instale as dependências

```bash
poetry install
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto copiando o conteúdo de `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` conforme necessário.

### 4. Utilize Docker

Para rodar o projeto utilizando Docker, siga os passos abaixo:

1. Suba o ambiente Docker:

    ```bash
    make up
    ```

2. Para derrubar o ambiente Docker:

    ```bash
    make down
    ```

O servidor estará rodando em `http://localhost:8000`.

## Seeds

Ao rodar o Docker, um seed é criado automaticamente. Este seed inclui um usuário padrão com as credenciais `admin:admin` e algumas contas de pagamento. Para mais detalhes, consulte o arquivo `/scripts/seeds.py`. Lá vai ter exatamente qual id você utilizar na requisição dependendo do que for fazer.

## Testes

Para rodar os testes, utilize o comando:

```bash
make test
```

Para rodar os testes com o coverage, utilize o comando:

```bash
make test-coverage
```

Para verificar o coverage abra o arquivo `/htmlcov/index.html` no seu navegador.

## Documentação

Para verificar a documentação do projeto, acesse:

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)


## Insomnia

Na pasta `/docs` existe um arquivo chamado `bank-api.json` que pode ser importado no Insomnia.
