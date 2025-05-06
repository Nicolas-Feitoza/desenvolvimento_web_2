import os
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate

config_name = os.getenv('FLASK_CONFIG', 'testing')  # Define testing como padrão para os testes
app = create_app(config_name)
print(f"Aplicação inicializada com a configuração: {config_name}")

migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """
    Adiciona objetos ao contexto shell.
    Nota: Sempre atualize essa função ao adicionar novos modelos
    """
    return dict(db=db, User=User, Role=Role)