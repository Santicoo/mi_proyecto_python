# Versión 3 — Editorial / Cuadernillo (renderizado en servidor, sin JavaScript)

Quiz sobre **Stack y Arquitecturas de Software**, construido con Python y Flask.

- **Estética:** cuadernillo impreso. Papel crema, tipografía serif, reglas finas, numeración tipográfica y marcas al margen.
- **Estructura:** núcleo aislado en `domain/` (banco de preguntas + reglas de evaluación, **sin importar Flask**) y `app.py` como adaptador web.
- **Flujo del quiz:** **una página por pregunta**. Cada respuesta es un formulario HTML que se envía al servidor; el avance se guarda en la sesión de Flask. **No hay JavaScript**: la aplicación funciona igual con JS desactivado.
- **Preguntas:** 8, agrupadas en tres secciones temáticas, con índice navegable.

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
```

## Antes de entregar

Abre [app.py](app.py) y cambia la constante:

```python
ESTUDIANTE = "NOMBRE DEL ESTUDIANTE"
```

## Ejecución local

```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```

Abre `http://localhost:5000`.

## Despliegue en Render

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Variable de entorno recomendada:** `SECRET_KEY` con un valor aleatorio (firma la cookie de sesión donde se guarda el avance del cuestionario).

## Rutas

| Ruta | Método | Descripción |
|---|---|---|
| `/` | GET | Portada, ficha del proyecto e índice del cuestionario |
| `/iniciar` | POST | Reinicia la sesión y envía a la pregunta 1 |
| `/pregunta/<n>` | GET | Muestra la pregunta n (con feedback si ya fue respondida) |
| `/pregunta/<n>` | POST | Guarda la respuesta y redirige (POST/Redirect/GET) |
| `/resultado` | GET | Puntuación final y revisión pregunta por pregunta |
| `/reiniciar` | POST | Limpia la sesión |
