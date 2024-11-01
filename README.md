

Sistema de Reservas de Quadra de Tênis 🎾

Este projeto é um sistema de reservas de quadra de tênis desenvolvido com Python e Flask, com uma interface simples e visualmente agradável. O sistema permite que usuários façam e excluam reservas para uma quadra de tênis, visualizem as datas disponíveis e gerenciem seus agendamentos por meio de uma área de login.

Funcionalidades

- **Visualizar Disponibilidade**: Exibe os horários disponíveis para reserva da quadra.
- **Sistema de Login**: Usuários precisam se registrar e fazer login para acessar o sistema.
- **Marcação de Reserva**: Permite que o usuário faça reservas informando nome, CPF e horário.
- **Exclusão de Reserva**: Usuário pode cancelar uma reserva, se necessário.

Tecnologias Utilizadas

- **Back-end**: Flask, Flask-SQLAlchemy, Flask-Login
- **Banco de Dados**: SQLite (para desenvolvimento local)
- **Front-end**: HTML, CSS, JavaScript (simplificado e responsivo)

Pré-requisitos

- Python 3.6+
- pip (gerenciador de pacotes do Python)
- Ambiente virtual (opcional, mas recomendado)

Como Configurar o Ambiente

1. Clonar o repositório:

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
   ```

2. *riar e ativar o ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instalar as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar o Banco de Dados:

   Execute o script para criar as tabelas necessárias:

   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

Executando o Projeto

1. Iniciar o servidor Flask:

   ```bash
   flask run
   ```

2. Acessar o sistema:

   Abra o navegador e acesse `http://127.0.0.1:5000`.

Estrutura de Diretórios

```plaintext
nome-do-repositorio/
├── app/
│   ├── static/          # Arquivos CSS, JS, imagens
│   ├── templates/       # Arquivos HTML
│   ├── __init__.py      # Inicialização do aplicativo Flask
│   ├── models.py        # Modelos de banco de dados
│   ├── routes.py        # Rotas e lógica de navegação
│   └── ...
├── venv/                # Ambiente virtual (não enviar para o GitHub)
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo
```

Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar issues e pull requests para melhorias ou correções.
