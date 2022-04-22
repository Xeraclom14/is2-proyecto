from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from numpy import insert

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'encuestas'
mysql = MySQL(app)

@app.route('/')
def Index():
    return "Hola."

@app.route('/edit/<id>')
def edit(id):
    return "Editando encuesta " + id + "."

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO encuesta (id_encuestador, titulo) VALUES (1 , %s);', request.form['titulo'])
        mysql.connection.commit()
        print(request.form['titulo'])
        return render_template('creation.html')
    else:
        return render_template('creation.html')

@app.route('/stats/<id>')
def stats(id):
    return "Estadísticas de la encuesta con ID " + id + "."

@app.route('/form/<id>')
def form(id):
    return "Respndiendo encuesta con ID " + id + "."

if __name__ == '__main__':
    app.run(port = 5000, debug = True)