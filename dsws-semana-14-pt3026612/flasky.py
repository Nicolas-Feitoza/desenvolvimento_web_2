import os
import click
from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate
from flask_login import login_required

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

@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """
    Executa testes unitários.
    Uso:
        flask test                  -> Executa todos os testes
        flask test nome_do_teste    -> Executa um teste específico
    """
    import unittest
    try:
        if test_names:
            tests = unittest.TestLoader().loadTestsFromNames(test_names)
        else:
            tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
    except ModuleNotFoundError as e:
        click.echo(f"Erro: O módulo especificado não foi encontrado: {e}")
    except Exception as e:
        click.echo(f"Erro ao executar os testes: {e}")

@app.route('/secret')
@login_required
def secret():
    return 'Apenas usuários cadastrados são permitidos!'