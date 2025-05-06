import unittest
from app.auth.forms import (
    LoginForm, RegistrationForm
)
from app.models import User
from . import TestCase

class AuthFormsTestCase(TestCase):
    def test_valid_login_form(self):
        """Teste para validação de um formulário de login válido."""
        form = LoginForm(email="test@zohomail.com", password="password123")
        self.assertTrue(form.validate())

    def test_invalid_login_email_format(self):
        """Teste para validar erro de formato de email no LoginForm."""
        form = LoginForm(email="invalidemail", password="password123")
        self.assertFalse(form.validate())
        self.assertIn('Insira um e-mail válido.', form.email.errors)

    def test_unique_email_registration(self):
        """Teste para verificar erro de e-mail duplicado no RegistrationForm."""
        user = User(email="test@zohomail.com", username="testuser", prontuario="ABC1234567")
        user.save()

        form = RegistrationForm(
            email="test@zohomail.com",
            username="newuser",
            prontuario="DEF1234567",
            password="password123",
            password2="password123"
        )
        self.assertFalse(form.validate())
        self.assertIn('Este e-mail já está registrado.', form.email.errors)

    def test_valid_registration_form(self):
        """Teste para validar o funcionamento correto de RegistrationForm."""
        form = RegistrationForm(
            email="newuser@zohomail.com",
            username="newuser",
            prontuario="DEF1234567",
            password="password123",
            password2="password123"
        )
        self.assertTrue(form.validate())

    def test_prontuario_format_validation(self):
        """Teste para validar o formato do prontuário."""
        form = RegistrationForm(
            email="user@zohomail.com",
            username="user",
            prontuario="123INVALID",
            password="password123",
            password2="password123"
        )
        self.assertFalse(form.validate())
        self.assertIn(
            'O prontuário deve ter 3 letras seguidas de 7 números. Exemplo: ABC1234567',
            form.prontuario.errors
        )

    def test_zoho_email_validation(self):
        """Teste para validar o domínio de e-mail @zohomail.com."""
        form = RegistrationForm(
            email="user@gmail.com",
            username="user",
            prontuario="ABC1234567",
            password="password123",
            password2="password123"
        )
        self.assertFalse(form.validate())
        self.assertIn(
            'Por favor, use um e-mail @zohomail.com.',
            form.email.errors
        )

if __name__ == "__main__":
    unittest.main()
