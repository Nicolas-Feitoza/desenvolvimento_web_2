import unittest
from app import create_app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SERVER_NAME'] = 'nicolassf.pythonanywhere.com'
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # Cria tabelas para o teste
        self.client = self.app.test_client()

        @self.app.before_request
        def before_request():
            db.session.rollback()  # Garante isolamento dos testes

        @self.app.teardown_request
        def teardown_request(exception=None):
            db.session.remove()  # Remove a sessão após cada requisição/teste

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Remove tabelas após o teste
        self.app_context.pop()

