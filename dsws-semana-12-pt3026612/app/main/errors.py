from flask import render_template
from . import main

# Tratamento de erro 404 (página não encontrada)
@main.app_errorhandler(404)
def page_not_found(e):
    """Lida com erros 404 (página não encontrada) e retorna a template apropriada."""
    return render_template('404.html'), 404

# Tratamento de erro 500 (erro interno do servidor)
@main.app_errorhandler(500)
def internal_server_error(e):
    """Lida com erros 500 (erro interno do servidor) e retorna a template apropriada."""
    return render_template('500.html'), 500
