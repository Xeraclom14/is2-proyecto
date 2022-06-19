from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask import send_from_directory
from flask_mysqldb import MySQL
from flask_mail import Mail
import os
import mail_config
from flask_login import LoginManager

app = Flask(__name__)

###encuestador id
###INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`) VALUES ('V','C','J','A','1')


###BD
app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''

###Nombre de la BD
app.config['MYSQL_DB'] = 'is2_proyecto'
mysql = MySQL(app)

###datos de sesión
#La clave secreta, esto es importante.
app.secret_key = 'ffc5c7a327818c3193a6b640'

###Mail de la aplicacion
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_DEFAULT_SENDER'] = mail_config.MAIL_USER
app.config['MAIL_USERNAME'] = mail_config.MAIL_USER
app.config['MAIL_PASSWORD'] = mail_config.MAIL_PASSWORD
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#funcionalidad de sesión
#login_manager = LoginManager()
#login_manager.init_app(app)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)

#@app.before_request
#def make_session_permanent():
#    session.permanent = False


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


###crea un usuario en ala base de datos
import src.delete
import src.edit
import src.form
import src.forms
import src.index
import src.login
import src.stats
import src.logout
import src.register
import src.loginadmin
import src.profile

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port = 5000, debug = True)

