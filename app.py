"""Aplicación Flask — Cuadernillo de Stack y Arquitecturas de Software.

Versión 3: cuestionario renderizado íntegramente en el servidor.
No hay JavaScript: cada respuesta es un formulario HTML y el avance del
cuestionario se guarda en la sesión del usuario.

    domain/   -> núcleo: preguntas y reglas de evaluación (sin Flask)
    app.py    -> adaptador web: traduce HTTP a llamadas del núcleo
"""

import os

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from domain import banco, evaluador

# Cambia este valor por tu nombre completo.
ESTUDIANTE = "NOMBRE DEL ESTUDIANTE"
ASIGNATURA = "Ingeniería de Software II"

CLAVE_RESPUESTAS = "respuestas"

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cuadernillo-desarrollo")


@app.context_processor
def inyectar_identidad():
    return {"estudiante": ESTUDIANTE, "asignatura": ASIGNATURA, "total": banco.TOTAL}


def _respuestas():
    return session.get(CLAVE_RESPUESTAS, {})


@app.route("/")
def portada():
    respuestas = _respuestas()
    return render_template(
        "portada.html",
        preguntas=banco.PREGUNTAS,
        respondidas=len(respuestas),
        en_curso=bool(respuestas),
    )


@app.post("/iniciar")
def iniciar():
    """Reinicia el cuadernillo y envía a la primera pregunta."""
    session[CLAVE_RESPUESTAS] = {}
    return redirect(url_for("pregunta", numero=1))


@app.route("/pregunta/<int:numero>")
def pregunta(numero):
    """Muestra una pregunta y, si ya fue respondida, su retroalimentación."""
    actual = banco.obtener(numero)
    if actual is None:
        abort(404)

    elegida = _respuestas().get(str(numero))
    veredicto = evaluador.calificar(numero, elegida) if elegida else None

    return render_template(
        "pregunta.html",
        pregunta=actual,
        veredicto=veredicto,
        elegida=elegida,
        anterior=numero - 1 if numero > 1 else None,
        siguiente=numero + 1 if numero < banco.TOTAL else None,
        respondidas=len(_respuestas()),
    )


@app.post("/pregunta/<int:numero>")
def responder(numero):
    """Guarda la respuesta en la sesión y vuelve a la pregunta (patrón POST/Redirect/GET)."""
    if not banco.existe(numero):
        abort(404)

    opcion = request.form.get("opcion", "")
    if not evaluador.es_opcion_valida(opcion):
        return redirect(url_for("pregunta", numero=numero))

    respuestas = dict(_respuestas())
    respuestas[str(numero)] = opcion
    session[CLAVE_RESPUESTAS] = respuestas

    return redirect(url_for("pregunta", numero=numero))


@app.route("/resultado")
def resultado():
    return render_template("resultado.html", resumen=evaluador.resumen(_respuestas()))


@app.post("/reiniciar")
def reiniciar():
    session.pop(CLAVE_RESPUESTAS, None)
    return redirect(url_for("portada"))


@app.errorhandler(404)
def no_encontrado(_error):
    return render_template("error.html"), 404


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=puerto, debug=True)
