from flask import render_template
from . import main

# Tratamento de erro 404 (página não encontrada)
@main.app_errorhandler(404)
def page_not_found(e):
    """
    Tratador de erro para páginas não encontradas (404).
    """
    return render_template('404.html'), 404

# Tratamento de erro 500 (erro interno do servidor)
@main.app_errorhandler(500)
def internal_server_error(e):
    """
    Tratador de erro para erros internos do servidor (500).
    """
    return render_template('500.html'), 500

# Tratamento de erro 400 (requisição inválida)
@main.app_errorhandler(400)
def bad_request(e):
    """
    Tratador de erro para requisições inválidas (400).
    """
    return render_template('400.html'), 400

# Tratamento de erro 403 (acesso proibido)
@main.app_errorhandler(403)
def forbidden(e):
    """
    Tratador de erro para acesso proibido (403).
    """
    return render_template('403.html'), 403