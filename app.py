import os

from flask import Flask, abort, redirect, render_template, request, session, url_for

from domain import banco, evaluador

# Nombre del estudiante que aparece en la portada y en el quiz.
ESTUDIANTE = "Santiago Cordoba Muriel"
ASIGNATURA = "Ingeniería de Software II"

CLAVE_RESPUESTAS = "respuestas"

app = Flask(__name__)
# En Render se define la variable de entorno SECRET_KEY; el valor por defecto es solo para desarrollo.
app.secret_key = os.environ.get("SECRET_KEY", "clave-de-desarrollo")


@app.context_processor
def inyectar_identidad():
    return {"estudiante": ESTUDIANTE, "asignatura": ASIGNATURA, "total": banco.TOTAL}


def _respuestas():
    return session.get(CLAVE_RESPUESTAS, {})


@app.route('/')
def home():
    respondidas = len(_respuestas())
    return render_template('index.html', respondidas=respondidas, en_curso=respondidas > 0)


@app.post('/iniciar')
def iniciar():
    """Reinicia el quiz y envía a la primera pregunta."""
    session[CLAVE_RESPUESTAS] = {}
    return redirect(url_for('pregunta', numero=1))


@app.route('/pregunta/<int:numero>')
def pregunta(numero):
    """Muestra una pregunta y, si ya fue respondida, su retroalimentación."""
    actual = banco.obtener(numero)
    if actual is None:
        abort(404)

    elegida = _respuestas().get(str(numero))
    veredicto = evaluador.calificar(numero, elegida) if elegida else None

    return render_template(
        'pregunta.html',
        pregunta=actual,
        veredicto=veredicto,
        elegida=elegida,
        anterior=numero - 1 if numero > 1 else None,
        siguiente=numero + 1 if numero < banco.TOTAL else None,
        respondidas=len(_respuestas()),
    )


@app.post('/pregunta/<int:numero>')
def responder(numero):
    """Guarda la respuesta en la sesión y vuelve a la pregunta (POST/Redirect/GET)."""
    if not banco.existe(numero):
        abort(404)

    opcion = request.form.get('opcion', '')
    if not evaluador.es_opcion_valida(opcion):
        return redirect(url_for('pregunta', numero=numero))

    respuestas = dict(_respuestas())
    respuestas[str(numero)] = opcion
    session[CLAVE_RESPUESTAS] = respuestas

    return redirect(url_for('pregunta', numero=numero))


@app.route('/resultado')
def resultado():
    return render_template('resultado.html', resumen=evaluador.resumen(_respuestas()))


@app.post('/reiniciar')
def reiniciar():
    session.pop(CLAVE_RESPUESTAS, None)
    return redirect(url_for('home'))


@app.errorhandler(404)
def no_encontrado(_error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
