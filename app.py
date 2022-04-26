from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#encuestador id
#INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`) VALUES ('V','C','J','A','1')
e_id = 1


#BD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
#Nombre de la BD
app.config['MYSQL_DB'] = 'encuestas'
mysql = MySQL(app)


#crea un usuario en ala base de datos
@app.route('/')
def Index():
    #cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`) VALUES ('V','C','J','A','j@gmail.com')")
    #mysql.connection.commit()
    return "INDEX"

@app.route('/edit/<id>')
def edit(id):
    return "Editando encuesta " + id + "."

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM encuesta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()
    return redirect(url_for("forms"))

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        if(request.form['titulo'] != ""):
            #TEXTO LIMPIO DE CATEGORIAS
            #categorias =  request.form['categoria'].upper().split(',')
            #for categoria in categorias:
            #    categoria = categoria.rstrip()
            #    categoria = categoria.lstrip()
            #    print(categoria)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO encuesta (id_encuestador, titulo) VALUES (%s , %s);", (e_id, request.form['titulo']))
            mysql.connection.commit()
            #print(request.form['titulo'])
            return redirect(url_for("forms"))
        else:
            print("Ingerese un valor valido")
        #redirigir para borrar el formulario de la memoria (no se envia nuevamente si se recarga la pagina)
        return redirect(url_for("create"))
    else:
        return render_template('creation.html')

@app.route('/stats/<id>')
def stats(id):
    return "Estadísticas de la encuesta con ID " + id + "."

@app.route('/form/<id>')
def form(id):
    return "Respndiendo encuesta con ID " + id + "."

@app.route('/forms')
def forms():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM encuesta")
    datos = cur.fetchall()
    print(datos)
    return render_template('forms.html', forms = datos)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)