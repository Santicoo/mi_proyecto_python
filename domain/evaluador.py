"""Reglas de evaluación del cuestionario.

Funciones puras: reciben datos y devuelven datos. No dependen de Flask,
de la sesión ni de HTTP, de modo que pueden probarse de forma aislada.
"""

from domain import banco

OPCIONES_VALIDAS = ("A", "B", "C", "D")


def es_opcion_valida(opcion):
    return opcion in OPCIONES_VALIDAS


def calificar(numero, opcion):
    """Califica una respuesta. Devuelve None si la pregunta no existe."""
    pregunta = banco.obtener(numero)
    if pregunta is None:
        return None

    acierto = opcion == pregunta["correcta"]
    return {
        "numero": numero,
        "acierto": acierto,
        "elegida": opcion,
        "correcta": pregunta["correcta"],
        "texto_elegida": pregunta["opciones"].get(opcion, ""),
        "texto_correcta": pregunta["opciones"][pregunta["correcta"]],
        "retroalimentacion": pregunta["retroalimentacion"],
    }


def resumen(respuestas):
    """Construye el resultado final a partir de las respuestas guardadas.

    `respuestas` es un diccionario como {"1": "A", "2": "B"} tal y como queda
    almacenado en la sesión, donde las claves se serializan como texto.
    """
    detalle = []
    aciertos = 0

    for pregunta in banco.PREGUNTAS:
        elegida = respuestas.get(str(pregunta["numero"]))
        acierto = elegida == pregunta["correcta"]
        if acierto:
            aciertos += 1
        detalle.append(
            {
                "numero": pregunta["numero"],
                "tema": pregunta["tema"],
                "enunciado": pregunta["enunciado"],
                "elegida": elegida,
                "correcta": pregunta["correcta"],
                "texto_correcta": pregunta["opciones"][pregunta["correcta"]],
                "acierto": acierto,
                "respondida": elegida is not None,
            }
        )

    total = banco.TOTAL
    porcentaje = round((aciertos / total) * 100) if total else 0

    return {
        "aciertos": aciertos,
        "total": total,
        "porcentaje": porcentaje,
        "detalle": detalle,
        "mensaje": _mensaje(porcentaje),
        "completo": all(d["respondida"] for d in detalle),
    }


def _mensaje(porcentaje):
    if porcentaje == 100:
        return "Dominio completo del temario de stack y arquitecturas."
    if porcentaje >= 70:
        return "Buen desempeño. Conviene repasar los puntos señalados más abajo."
    if porcentaje >= 50:
        return "Resultado ajustado: se recomienda revisar la teoría del curso."
    return "Es necesario repasar los conceptos antes de la evaluación."
