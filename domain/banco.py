"""Banco de preguntas del cuestionario.

Módulo de datos puro: no importa Flask ni ninguna otra dependencia externa.
"""

PREGUNTAS = [
    {
        "numero": 1,
        "seccion": "I. Fundamentos",
        "tema": "Stack tecnológico",
        "enunciado": "¿Qué se entiende por Stack tecnológico?",
        "opciones": {
            "A": "La combinación de lenguajes, frameworks, bases de datos, herramientas y servicios",
            "B": "Únicamente el lenguaje de programación utilizado",
            "C": "Únicamente el framework de backend",
            "D": "El diseño visual de la aplicación",
        },
        "correcta": "A",
        "retroalimentacion": (
            "El stack abarca todas las piezas que sostienen el producto: lenguaje, "
            "framework, almacenamiento, control de versiones y servicio de despliegue. "
            "En este proyecto: Python, Flask, HTML/CSS, Git, GitHub y Render."
        ),
    },
    {
        "numero": 2,
        "seccion": "I. Fundamentos",
        "tema": "Monolito modular",
        "enunciado": "¿Cuál es una característica del monolito modular?",
        "opciones": {
            "A": "Cada módulo debe ejecutarse en un servidor independiente",
            "B": "Organiza internamente las responsabilidades en módulos definidos",
            "C": "Obliga a utilizar un bus de eventos",
            "D": "Impide separar la lógica de la presentación",
        },
        "correcta": "B",
        "retroalimentacion": (
            "Un monolito modular se despliega como una sola unidad, pero conserva "
            "fronteras internas claras. Esta aplicación separa el dominio (preguntas "
            "y evaluación) de la capa web."
        ),
    },
    {
        "numero": 3,
        "seccion": "II. Estilos arquitectónicos",
        "tema": "Arquitectura hexagonal",
        "enunciado": "¿Qué representan los puertos en la arquitectura hexagonal?",
        "opciones": {
            "A": "Las bases de datos utilizadas por la aplicación",
            "B": "Los servidores encargados del despliegue",
            "C": "Interfaces mediante las cuales el núcleo se comunica con el exterior",
            "D": "Componentes exclusivos del frontend",
        },
        "correcta": "C",
        "retroalimentacion": (
            "Un puerto es un contrato que define el núcleo. El exterior debe adaptarse "
            "a ese contrato, nunca al contrario."
        ),
    },
    {
        "numero": 4,
        "seccion": "II. Estilos arquitectónicos",
        "tema": "Arquitectura hexagonal",
        "enunciado": "¿Cuál es el propósito de un adaptador en arquitectura hexagonal?",
        "opciones": {
            "A": "Convertir la comunicación externa para ajustarse al contrato de un puerto",
            "B": "Generar automáticamente las bases de datos del sistema",
            "C": "Reemplazar al núcleo de la aplicación",
            "D": "Administrar los permisos del repositorio",
        },
        "correcta": "A",
        "retroalimentacion": (
            "El adaptador traduce entre la tecnología concreta (HTTP, SQL, colas) y el "
            "puerto. En esta aplicación, las rutas de Flask actúan como adaptador sobre "
            "el módulo de evaluación."
        ),
    },
    {
        "numero": 5,
        "seccion": "II. Estilos arquitectónicos",
        "tema": "Clean Architecture",
        "enunciado": "¿Cuál es la regla principal de Clean Architecture?",
        "opciones": {
            "A": "Las dependencias apuntan hacia la infraestructura",
            "B": "Las dependencias del código deben apuntar hacia el núcleo",
            "C": "Toda aplicación debe dividirse en microservicios",
            "D": "La capa de presentación debe controlar la base de datos",
        },
        "correcta": "B",
        "retroalimentacion": (
            "La regla de dependencia: el código fuente siempre apunta hacia adentro. "
            "El dominio no conoce ni el framework web ni el motor de persistencia."
        ),
    },
    {
        "numero": 6,
        "seccion": "II. Estilos arquitectónicos",
        "tema": "Arquitectura orientada a eventos",
        "enunciado": "¿Qué caracteriza a una arquitectura orientada a eventos?",
        "opciones": {
            "A": "Un único servidor central que ejecuta toda la lógica",
            "B": "Una estructura obligatoria de tres capas",
            "C": "El uso exclusivo de bases de datos relacionales",
            "D": "Productores, consumidores e intermediario o bus de eventos",
        },
        "correcta": "D",
        "retroalimentacion": (
            "Los productores publican eventos, el broker los distribuye y los "
            "consumidores reaccionan. El resultado es un sistema asíncrono y desacoplado."
        ),
    },
    {
        "numero": 7,
        "seccion": "III. Proceso y despliegue",
        "tema": "Git y GitHub",
        "enunciado": "¿Cuál es el propósito principal de un Pull Request?",
        "opciones": {
            "A": "Solicitar la revisión e integración de los cambios de una rama",
            "B": "Crear una máquina virtual en la nube",
            "C": "Instalar las dependencias del proyecto",
            "D": "Ejecutar el intérprete de Python",
        },
        "correcta": "A",
        "retroalimentacion": (
            "El Pull Request propone integrar una rama en otra y abre el espacio de "
            "revisión y discusión del código antes de fusionar."
        ),
    },
    {
        "numero": 8,
        "seccion": "III. Proceso y despliegue",
        "tema": "Despliegue",
        "enunciado": "¿Qué evidencia demuestra un despliegue exitoso en Render?",
        "opciones": {
            "A": "Una captura del código fuente en el editor",
            "B": "El repositorio local con todos los commits",
            "C": "El enlace público funcional junto con la evidencia del proceso de despliegue",
            "D": "El archivo de dependencias actualizado",
        },
        "correcta": "C",
        "retroalimentacion": (
            "Un despliegue se demuestra con la URL pública respondiendo y con el log de "
            "build y deploy exitoso en el panel de Render."
        ),
    },
]

TOTAL = len(PREGUNTAS)


def obtener(numero):
    """Devuelve la pregunta con ese número, o None si no existe."""
    for pregunta in PREGUNTAS:
        if pregunta["numero"] == numero:
            return pregunta
    return None


def existe(numero):
    return obtener(numero) is not None
