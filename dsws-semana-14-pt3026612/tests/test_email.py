import unittest
from bs4 import BeautifulSoup # Utilizado para fazer parsing de HTML e extrair dados de páginas web
from unittest.mock import patch, MagicMock
from app import email
from . import TestCase

class TestEmailModule(TestCase):

    def setUp(self):
        # Configura o aplicativo Flask para os testes
        self.app.config['MAILGUN_API_URL'] = 'https://api.mailgun.net/v3/example.com/messages'
        self.app.config['MAILGUN_API_KEY'] = 'test-key'
        self.app.config['MAILGUN_DOMAIN'] = 'example.com'
        self.app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
        self.to = 'test@zohomail.com'
        self.subject = 'Test Subject'
        self.body = 'This is a test email body.'
        self.gif_url = 'https://example.com/welcome.gif'

    @patch('app.email.requests.post')
    def test_send_verification_email_success(self, mock_post):
        with self.app.app_context():
            # Configura o mock para simular uma resposta de sucesso
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            email.send_verification_email(self.to, self.subject, self.body)

            # Verifica se a função post foi chamada corretamente
            mock_post.assert_called_once_with(
                self.app.config['MAILGUN_API_URL'],
                auth=('api', self.app.config['MAILGUN_API_KEY']),
                data={
                    'from': f"Flasky <noreply@{self.app.config['MAILGUN_DOMAIN']}>",
                    'to': self.to,
                    'subject': f"{self.app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {self.subject}",
                    'html': self.body
                }
            )

    @patch('app.email.requests.post')
    def test_send_verification_email_failure(self, mock_post):
        with self.app.app_context():
            # Configura o mock para simular uma resposta de erro
            mock_response = MagicMock()
            mock_response.status_code = 500
            mock_response.text = "Error sending email"
            mock_post.return_value = mock_response

            with self.assertRaises(Exception):
                email.send_verification_email(self.to, self.subject, self.body)

            # Verifica se a resposta de erro foi manipulada
            mock_post.assert_called_once()

    @patch('app.email.requests.post')
    def test_send_email_with_gif(self, mock_post):
        with self.app.app_context():
            # Configura o mock para simular uma resposta de sucesso
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            email.send_email_with_gif(self.to, self.subject, self.body, self.gif_url)

             # Verifica se o post foi chamado corretamente
            mock_post.assert_called_once()

            # Pega os argumentos da chamada
            actual_call = mock_post.call_args
            actual_html = actual_call[1]['data']['html']

            # Normaliza o HTML real e o esperado
            normalized_html = f"""
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Bem-vindo!</title>
                </head>
                <body>
                    <p>{self.body}</p>
                    <p>
                        <img src="{self.gif_url}" alt="Welcome GIF" />
                    </p>
                </body>
            </html>
            """

            # Usando BeautifulSoup para comparar HTML, ignorando diferenças de formatação
            assert str(BeautifulSoup(actual_html, 'html.parser')) == str(BeautifulSoup(normalized_html, 'html.parser'))

    @patch('app.email.requests.post')
    def test_send_simple_message(self, mock_post):
        with self.app.app_context():
            # Configura o mock para simular uma resposta de sucesso
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            email.send_simple_message(self.to, self.subject, "New User")

            # Verifica se a função post foi chamada corretamente
            mock_post.assert_called_once_with(
                self.app.config['MAILGUN_API_URL'],
                auth=('api', self.app.config['MAILGUN_API_KEY']),
                data={
                    'from': f"Flasky <noreply@{self.app.config['MAILGUN_DOMAIN']}>",
                    'to': self.to,
                    'subject': f"{self.app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {self.subject}",
                    'text': "Novo usuário cadastrado: New User"
                }
            )

if __name__ == '__main__':
    unittest.main()
