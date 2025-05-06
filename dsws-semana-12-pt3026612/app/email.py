import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def send_simple_message(to, subject, new_user):
    """
    Envia uma mensagem simples usando o serviço Mailgun.
    """
    # Verifica se as configurações do Mailgun estão presentes
    if not current_app.config.get('MAILGUN_API_KEY') or not current_app.config.get('MAILGUN_API_URL'):
        logger.warning('⚠️ Mailgun não configurado corretamente. Mensagem não enviada.')
        return

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

        # Verifica a resposta do Mailgun
        if response.status_code == 200:
            logger.info("✅ Mensagem enviada com sucesso!")
        else:
            logger.error(f"⚠️ Falha ao enviar mensagem. Código: {response.status_code}, Erro: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.exception("Erro ao tentar enviar mensagem devido a uma falha de solicitação HTTP.", exc_info=e)
    except Exception as e:
        logger.exception("Erro inesperado ao enviar mensagem.", exc_info=e)
