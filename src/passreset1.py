from sqlite3 import connect
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

from __main__ import app, mysql, mail

@app.route('/passreset1', methods=['GET', 'POST'])
def passreset1():

    if 'loggedin' in session:
        return(render_template("403.html"))

    if request.method == 'POST': 
       #Se ingreso un correo
       if(request.form['email'] != ""):
            
            email = request.form['email']
            
            #conexión          
            cur = mysql.connection.cursor()

            #Esto es para verificar si el correo existe. 
            cur.execute("SELECT * FROM encuestado WHERE email LIKE %s",[email])

            account = cur.fetchone()

            #Si el correo no existe se refresca la pagina.   
            if account is None: 
               flash("warning","El correo no existe")
               return redirect(url_for("passreset1"))

            #Si el correo existe manda un correo con el link para reiniciar tu cuenta.  
            else:

                with mail.connect() as conn:
                    

                    cur.execute("SELECT id_encuestado FROM encuestado WHERE email LIKE %s",[email])

                    auxID = cur.fetchone()
                    
                    #Esta transformaciones se hacen para convertir una tupla string en string
                    auxEmail =''.join(email)
                    #Esta transformacion se hace para convertir una tupla numero en string
                    auxID2 =''.join(map(str,auxID))



                    print (auxEmail)
                    print (auxID2)
            
                    message = 'Estimado usuario usted ha solicitado un cambio de contraseña, siga el siguiente link para cambiar su contraseña: http://127.0.0.1:5008/passwordreset2/'+auxID2
                    subject = "Has solicitado cambio de contraseña en Encuestas Peepo"
                    msg = Message(recipients=[auxEmail],
                        body=message,
                        subject=subject)
                    conn.send(msg)

                
                flash("warning","Se ha enviado un link para cambiar su contraseña a su correo")
                return redirect(url_for("login"))
       else:
            flash("warning","Por favor, ingrese sus datos")
            return redirect(url_for("passreset1")) 
    else: 
        return render_template('passreset1.html')
