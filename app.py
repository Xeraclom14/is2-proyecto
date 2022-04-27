from multiprocessing.sharedctypes import Value
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from select import select

app = Flask(__name__)

#encuestador id
#INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`) VALUES ('V','C','J','A','1')
e_id = 1


#BD
app.config['MYSQL_HOST'] = 'localhost'

#como uso password para el root, creo un usuario aparte con todos los privilegios
#Descomentar esto (y comentar lo de abajo) para usar root
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_USER'] = 'rhoda437'
app.config['MYSQL_PASSWORD'] = 'PassAuxParaProyectoIS2$'

#Nombre de la BD
app.config['MYSQL_DB'] = 'is2_proyecto'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

#crea un usuario en ala base de datos
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `Encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`,`password`) VALUES ('V','C','J','A','j@gmail.com','asd')")
    mysql.connection.commit()
    return "Encuestador j@gmail.com creado"
    #return "INDEX"

@app.route('/edit/<id>')
def edit(id):
    return "Editando encuesta " + id + "."

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT titulo FROM Encuesta WHERE id_encuesta = %s;",(id,))
    datos = cur.fetchall()
    cur.execute("DELETE FROM Encuesta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()
    flash("Encuesta \"" + datos[0][0] +"\" eliminada exitosamente.")
    return redirect(url_for("forms"))

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        if(request.form['titulo'] != ""):
            #categorias =  request.form['categoria'].upper().split(',')
            #for categoria in categorias:
            #    categoria = categoria.rstrip()
            #    categoria = categoria.lstrip()
            #    print(categoria)
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO Encuesta (id_encuesta, id_encuestador, titulo) VALUES (1, %s , %s);", (e_id, request.form['titulo']))
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
    cur.execute("SELECT * FROM Encuesta")
    datos = cur.fetchall()
    #print(datos)
    return render_template('forms.html', forms = datos)

#@app.route('/login')
#def login():
#    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def logeo():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'uname' in request.form and 'psw' in request.form:

        # Create variables for easy access
        username = request.form['uname']
        password = request.form['psw']        

        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Encuestador WHERE email = %s AND password = %s', (username, password,))
        
        # Fetch one record and return result
        account = cursor.fetchone()
        
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            # Redirigir a pag principal
            return 'Logged in successfully!'

        else:
            #Cuenta incorrecta
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg='')

@app.route('/funciona')
def funciona():
    return render_template('funciona.html')

if __name__ == '__main__':
    app.run(port = 5000, debug = True)      