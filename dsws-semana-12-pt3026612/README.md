# Flasky - Gerenciador de Usuários e Notificações por E-mail
Uma aplicação web desenvolvida com Flask, hospedada no PythonAnywhere, que gerencia usuários e envia notificações por e-mail utilizando o serviço Mailgun.

## 📋 Funcionalidades

- Cadastro de Usuários
- Verificação de Duplicidade
- Notificações por E-mail
- Listagem de Usuários

## 🛠 Tecnologias Utilizadas

- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Python-dotenv
- Mailgun
- Bootstrap
- PythonAnywhere

## ⚙️ Configuração no PythonAnywhere

1. Configuração Inicial

- Crie uma conta ou acesse sua conta no [PythonAnywhere](https://www.pythonanywhere.com/).
- Configure o ambiente virtual e instale as dependências:

```bash
mkvirtualenv flasky_env --python=python3.x
pip install -r requirements.txt
```

2. Estrutura do Projeto

Garanta que as pastas e arquivos estejam organizados como segue no diretório do PythonAnywhere:

flasky/

├── app/

│   └── __init__.py       # Configuração da aplicação Flask
 
│   └── email.py          # Função de envio de e-mails

│   └── models.py         # Modelos de banco de dados

│   └── main/

│   └──── __init__.py   # Inicialização do blueprint principal

│   └──── errors.py     # Tratamento de erros personalizados

│   └──── forms.py      # Formulários da aplicação

│   └──── views.py      # Controladores de rotas e lógica

├── static/

│   └── css/

│   └──── styles.css

│   └── js/

|   └──── common.js

├── templates/

│   └── 404.html          # Página de erro 404

│   └── 500.html          # Página de erro 500

│   └── base.html         # Template base da aplicação

│   └── index.html        # Página inicial

├── tests/

│   └── __init__.py       # Inicialização dos testes

│   └── test_example.py   # Teste de exemplo (renomear para seus testes)

├── venv/                 # Ambiente virtual Python (não commitado)

├── requirements.txt      # Dependências do projeto

├── config.py             # Configurações da aplicação

├── flasky.py             # Arquivo principal para execução

├── .env                  # Variáveis de ambiente (não commitado)

├── README.md             # Documentação do projeto




3. Configuração das Variáveis de Ambiente
   


No arquivo *.env*, configure as credenciais do Mailgun e outros parâmetros necessários:

 ```
FLASKY_ADMIN=seu_email@exemplo.com
MAILGUN_API_KEY=sua_api_key
MAILGUN_API_URL=https://api.mailgun.net/v3/seu_dominio/messages
MAILGUN_DOMAIN=seu_dominio
MAILGUN_FROM=noreply@seu_dominio
```

4. Configuração do Servidor no PythonAnywhere

Configure o Web App no PythonAnywhere:

- Selecione o caminho para o WSGI, apontando para flasky.py.
- Configure o virtualenv criado.
- Reinicie o servidor após salvar as configurações. 

💻 Execução Local

Para executar o projeto localmente:

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure o arquivo *.env*.

Execute o servidor de desenvolvimento: 

```bash
flask run
```

Acesse a aplicação em seu localhost.

## 🔧 Funcionalidades Futuras

- Adicionar autenticação e autorização para administradores.
- Implementar paginação na listagem de usuários.
- Enviar notificações personalizadas para os usuários. 

## 📝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request no repositório.

## 🙋 Autor

Adaptado por Nicolas Feitoza.
Hospedado no [PythonAnywhere](https://www.pythonanywhere.com/).
