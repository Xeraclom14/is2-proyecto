from __main__ import app

@app.route('/form/<id>')
def form(id):
    return "Respndiendo encuesta con ID " + id + "."