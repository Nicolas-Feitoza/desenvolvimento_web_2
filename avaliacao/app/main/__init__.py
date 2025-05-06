from flask import Blueprint

# Define o Blueprint para a seção principal da aplicação
main = Blueprint('main', __name__)

# Importa as views e handlers de erro para registrar os Blueprints corretamente
from . import views, errors