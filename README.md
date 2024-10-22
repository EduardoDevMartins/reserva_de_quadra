Sistema de Reservas de Quadra de Tênis


Este é um sistema de reservas de quadras de tênis desenvolvido com Flask, que permite aos usuários agendar horários para jogar. O sistema é projetado para facilitar o gerenciamento de reservas, garantindo que os usuários possam verificar a disponibilidade de horários e realizar reservas de forma prática e eficiente.

Funcionalidades:
Autenticação de Usuários: Usuários podem se registrar e fazer login para gerenciar suas reservas.
Reservas de Horários: Possibilidade de agendar reservas de quadras com até 2 dias de antecedência.
Limitação de Reservas: Usuários podem ter no máximo duas reservas ativas simultaneamente.
Verificação de Disponibilidade: O sistema verifica se o horário escolhido já está reservado.
Interface Amigável: Uma interface intuitiva para facilitar a navegação e agendamento.

Tecnologias Utilizadas:
Flask: Framework para desenvolvimento web em Python.
SQLite: Banco de dados leve para armazenar as informações de reservas.
HTML/CSS: Para a construção da interface do usuário.
JavaScript: Para validações no lado do cliente e interações dinâmicas.

Como Usar:
Clone este repositório.
Instale as dependências com pip install -r requirements.txt.
Configure o banco de dados e execute a aplicação.
Acesse localhost/reserva para começar a fazer reservas!

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou um pull request.
