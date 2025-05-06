from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '''<h1>Avaliação contínua: Aula 030</h1>
              <ul>
              <li><a href="/">Home</a></li>
              <li><a href="/user/Nicolas%20Feitoza/PT3026612/IFSP">Identificação</a></li>
              <li><a href="/contextorequisicao">Contexto da requisição</a></li>
              </ul>'''

@app.route('/user/<nome>/<prontuario>/<instituicao>')
def user(nome, prontuario, instituicao):
    return '''<h1>Avaliação contínua: Aula 030</h1>
              <h2>Aluno: {}</h2>
              <h2>Prontuário: {}</h2>
              <h2>Instituição: {}</h2>
              <p><a href="/">Voltar</a></p>'''.format(nome, prontuario, instituicao)

@app.route('/contextorequisicao')
def contexto_requisicao():
    user_agent = request.headers.get('User-Agent')
    ip_remoto = request.remote_addr
    host_app = request.host
    return '''<h1>Avaliação contínua: Aula 030</h1>
              <h2>Seu navegador é: {}</h2>
              <h2>O IP do computador remoto é: {}</h2>
              <h2>O host da aplicação é: {}</h2>
              <p><a href="/">Voltar</a></p>'''.format(user_agent, ip_remoto, host_app)

if __name__ == '__main__':
    app.run(debug=True)
