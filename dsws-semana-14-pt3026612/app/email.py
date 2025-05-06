import requests
import logging
from flask import current_app

# Configuração do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_verification_email(to, subject, body):
    data = {
        'from': f"Flasky <noreply@{current_app.config['MAILGUN_DOMAIN']}>",
        'to': to,
        'subject': f"{current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}",
        'html': body
    }
    try:
        logger.info("Enviando mensagem para %s", to)
        response = requests.post(
            current_app.config['MAILGUN_API_URL'],
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data=data
        )
        _handle_mailgun_response(response)

        # Se a resposta não for bem-sucedida, lançar uma exceção
        if response.status_code != 200:
            raise Exception(f"Falha ao enviar email: {response.text}")
        
    except requests.exceptions.RequestException as e:
        logger.exception("Erro ao tentar enviar mensagem devido a uma falha de solicitação HTTP.", exc_info=e)
        raise  # Levanta a exceção novamente após registrar
    except Exception as e:
        logger.exception("Erro inesperado ao enviar mensagem.", exc_info=e)
        raise  # Levanta a exceção novamente após registrar


def send_simple_message(to, subject, new_user):
    """
    Envia uma mensagem simples usando o serviço Mailgun.

    :param to: Endereço de e-mail do destinatário.
    :param subject: Assunto do e-mail.
    :param new_user: Nome ou detalhes do novo usuário a serem incluídos na mensagem.
    """
    # Dados do e-mail
    data = {
        'from': f"Flasky <noreply@{current_app.config['MAILGUN_DOMAIN']}>",
        'to': to,
        'subject': f"{current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}",
        'text': f"Novo usuário cadastrado: {new_user}",
    }
    try:
        logger.info("Enviando mensagem para %s", to)
        response = requests.post(
            current_app.config['MAILGUN_API_URL'],
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data=data
        )

        _handle_mailgun_response(response)

    except requests.exceptions.RequestException as e:
        logger.exception("Erro ao tentar enviar mensagem devido a uma falha de solicitação HTTP.", exc_info=e)
        raise  # Levanta a exceção novamente após registrar
    except Exception as e:
        logger.exception("Erro inesperado ao enviar mensagem.", exc_info=e)
        raise  # Levanta a exceção novamente após registrar


def send_email_with_gif(to, subject, body, gif_url):
    """
    Envia um e-mail com um GIF hospedado usando o serviço Mailgun.

    :param to: Endereço de e-mail do destinatário.
    :param subject: Assunto do e-mail.
    :param body: Texto do corpo do e-mail.
    :param gif_url: URL do GIF a ser incluído no e-mail.
    """
    try:
        logger.info("Enviando mensagem com GIF para %s", to)

        # Cria o HTML do e-mail com o GIF hospedado
        html_body = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Bem-vindo!</title>
            </head>
            <body>
                <p>{body}</p>
                <p>
                    <img src="{gif_url}" alt="Welcome GIF" />
                </p>
            </body>
        </html>
        """

        # Envia a solicitação POST ao Mailgun
        response = requests.post(
            current_app.config['MAILGUN_API_URL'],
            auth=('api', current_app.config['MAILGUN_API_KEY']),
            data={
                'from': f"Flasky <noreply@{current_app.config['MAILGUN_DOMAIN']}>",
                'to': to,
                'subject': f"{current_app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}",
                'html': html_body  # Define o corpo do e-mail como HTML
            }
        )

        _handle_mailgun_response(response)

    except requests.exceptions.RequestException as e:
        logger.exception("Erro ao tentar enviar mensagem devido a uma falha de solicitação HTTP.", exc_info=e)
        raise  # Levanta a exceção novamente após registrar
    except Exception as e:
        logger.exception("Erro inesperado ao enviar mensagem.", exc_info=e)
        raise  # Levanta a exceção novamente após registrar


def _handle_mailgun_response(response):
    """
    Manipula a resposta do Mailgun e registra mensagens de sucesso ou erro.

    :param response: Objeto de resposta HTTP do Mailgun.
    """
    if response.status_code == 200:
        logger.info("✅ Mensagem enviada com sucesso!")
    else:
        logger.error(f"⚠️ Falha ao enviar email. Código: {response.status_code}, Erro: {response.text}")
