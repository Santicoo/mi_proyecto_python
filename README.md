# Versión 3 — Editorial / Cuadernillo (renderizado en servidor, sin JavaScript)

Quiz sobre **Stack y Arquitecturas de Software**, construido con Python y Flask.

- **Estética:** cuadernillo impreso. Papel crema, tipografía serif, reglas finas, numeración tipográfica y marcas al margen.
- **Estructura:** núcleo aislado en domain/ (banco de preguntas + reglas de evaluación, **sin importar Flask**) y app.py como adaptador web.
- **Flujo del quiz:** **una página por pregunta**. Cada respuesta es un formulario HTML que se envía al servidor; el avance se guarda en la sesión de Flask. **No hay JavaScript**: la aplicación funciona igual con JS desactivado.
- **Preguntas:** 8, agrupadas en tres secciones temáticas, con índice navegable.

## Evidencias
- **Repositorio de Git:** [Santicoo/mi_proyecto_python](https://github.com/Santicoo/mi_proyecto_python)
- **Pull Request:** [Santicoo/mi_proyecto_pythonl](https://github.com/Santicoo/mi_proyecto_python/) 
- **Despliegue público en Render:** [https://mi-proyecto-python-2.onrender.com](https://mi-proyecto-python-2.onrender.com)

## Estructura

```text
version-3-editorial/
├── app.py                  # Rutas Flask (adaptador web) + sesión
├── requirements.txt
├── domain/                 # Núcleo, sin dependencias de framework
│   ├── banco.py            # Preguntas
│   └── evaluador.py        # calificar() y resumen() — funciones puras
├── templates/
│   ├── base.html
│   ├── portada.html
│   ├── pregunta.html
│   ├── resultado.html
│   └── error.html
└── static/css/editorial.css
