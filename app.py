from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def Index():
    return "Hola."

@app.route('/edit/<id>')
def edit_form(id):
    return "Editando encuesta " + id + "."

@app.route('/create')
def create():
    return render_template('creation.html')

@app.route('/stats/<id>')
def stats(id):
    return "Estadísticas de la encuesta con ID " + id + "."

@app.route('/form/<id>')
def form(id):
    return "Respndiendo encuesta con ID " + id + "."

if __name__ == '__main__':
    app.run(port = 5000, debug = True)