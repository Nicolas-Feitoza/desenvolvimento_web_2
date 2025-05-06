from flask import Flask redirect, url_for, abort, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<nome>')
def user(nome):
    return '<h1>Hello, {}!</h1>'.format(nome)

@app.route('/contextorequisicao')
def contexto_requisicao():
    user_agent = request.headers.get('User-Agent');
    return <p>Your browser is {}</p>'.format(user_agent);

@app.route('/codigostatusdiferente')
def status_diferente():
    return "Bad request"

@app.route('/objetoresposta')
def objeto_resposta():
    resposta = make_response('<h1>This document carries a cookie!</h1>')
    return resposta

@app.route('/redirecionamento')
def redirecionar():
    return redirect('https://ptb.ifsp.edu.br')

@app.route('/abortar')
def abortar():
    abort(404)

if __name__ == '__main__':
    app.run(debug=True)
