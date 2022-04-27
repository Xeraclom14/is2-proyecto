from __main__ import app

@app.route('/edit/<id>')
def edit(id):
    return "Editando encuesta " + id + "."