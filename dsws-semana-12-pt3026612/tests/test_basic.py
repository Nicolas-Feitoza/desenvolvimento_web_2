import unittest
from flask import current_app
from app import create_app, db


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de teste."""
        self.app = create_app('testing')  # Cria o app com configuração de teste
        self.app_context = self.app.app_context()
        self.app_context.push()  # Abre o contexto da aplicação
        db.create_all()  # Cria o banco de dados para testes

    def tearDown(self):
        """Limpa o ambiente de teste."""
        db.session.remove()  # Remove as sessões do banco
        db.drop_all()  # Dropa todas as tabelas
        self.app_context.pop()  # Retira o contexto da aplicação

    def test_app_exists(self):
        """Verifica se o aplicativo está inicializado corretamente."""
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        """Verifica se o aplicativo está configurado para o ambiente de teste."""
        self.assertTrue(current_app.config['TESTING'])

    def test_homepage_status_code(self):
        """Verifica o status da página inicial."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_db_connection(self):
        """Verifica se o banco de dados está conectado corretamente."""
        self.assertIsNotNone(db.session)

    def test_user_model(self):
        """Verifica o modelo de usuário básico e sua criação."""
        from app.models import User

        # Criando um novo usuário
        user = User(username='testuser', prontuario='ABC1234567')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.prontuario, 'ABC1234567')

