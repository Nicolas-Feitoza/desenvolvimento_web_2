import unittest
from app.models import User, Role
import time
from . import TestCase

class ModelTestCase(TestCase):
    def setUp(self):
        super().setUp()
        # Dados iniciais
        self.role = Role(name='Admin')
        self.user = User(id = 2, username='testuser', prontuario='12345', email='test@example.com', role=self.role)
        self.user.password = 'testpassword'

    def test_role_creation(self):
        self.role.save()
        self.assertIsNotNone(Role.query.filter_by(name='Admin').first())

    def test_user_creation(self):
        self.user.save()
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.verify_password('testpassword'))

    def test_unique_constraints(self):
        self.role.save()
        self.user.save()
        with self.assertRaises(RuntimeError):
            duplicate_user = User(username='testuser', prontuario='12345', email='test@example.com', role=self.role)
            duplicate_user.save()

    def test_password_hashing(self):
        self.user.save()
        self.assertTrue(self.user.verify_password('testpassword'))
        self.assertFalse(self.user.verify_password('wrongpassword'))

    def test_token_generation_and_confirmation(self):
        # Salvar usuário no banco de dados
        self.user.save()
        # Gerar token de confirmação
        token = self.user.generate_confirmation_token()
        print(f"Token gerado para ID {self.user.id}: {token}")
        # Verificar confirmação válida
        confirmation = self.user.confirm(token)
        print(f"Confirmação bem-sucedida: {confirmation}")
        self.assertTrue(confirmation)
        # Verificar que o usuário está confirmado
        print(f"Usuário confirmado: {self.user.confirmed}")
        self.assertTrue(self.user.confirmed)
        # Testar confirmação com token inválido
        invalid_token = 'token-invalido'
        invalid_confirmation = self.user.confirm(invalid_token)
        self.assertFalse(invalid_confirmation)
        print("Token invalidado")
        # Testar confirmação com token expirado (altere o max_age em app/models para testar)
        expired_token = self.user.generate_confirmation_token(expiration=3)  # Expira em 1 segundo
        time.sleep(10)  # Aguarde até o token expirar
        expired_confirmation = self.user.confirm(expired_token)
        print(f"Resultado da confirmação com token expirado: {expired_confirmation}")
        self.assertFalse(expired_confirmation)




if __name__ == '__main__':
    unittest.main()
