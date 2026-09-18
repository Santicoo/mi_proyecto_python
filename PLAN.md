# Plan de desarrollo — Versión 3 (Núcleo aislado / estética editorial)

Evaluación de Ingeniería de Software II

---

## 1. Objetivo

Modificar una aplicación web existente en **Python y Flask** incorporando una sección creativa con el nombre del estudiante y un **quiz interactivo sobre Stack y Arquitecturas de Software**, para luego aplicar el flujo Git/GitHub, abrir un Pull Request y desplegar en Render.

### Historia de usuario

> Como estudiante de Ingeniería de Software II, quiero modificar una aplicación web desarrollada con Python y Flask, incorporando una sección creativa con mi nombre y una funcionalidad de quiz sobre Stack y Arquitecturas de Software.

---

## 2. Stack tecnológico

| Elemento | Selección |
|---|---|
| Lenguaje | Python 3 |
| Framework backend | Flask |
| Frontend | HTML + CSS (**sin JavaScript**) |
| Estado del cuestionario | Sesión de Flask (cookie firmada) |
| Datos | Módulo Python en el paquete `domain` |
| Servidor de producción | Gunicorn |
| Versionado | Git + GitHub |
| Despliegue | Render |

### Justificación

La decisión distintiva de esta versión es **prescindir de JavaScript**. El requisito de la evaluación es que el cuestionario identifique la opción seleccionada, dé retroalimentación e indique si la respuesta es correcta; nada de eso exige lógica en el cliente. Un formulario HTML y la sesión del servidor lo resuelven por completo.

El beneficio no es estético sino arquitectónico: al no haber estado en el navegador, existe **una sola fuente de verdad**. Además la aplicación es accesible por defecto (funciona con JavaScript desactivado, con lector de pantalla y con navegación por teclado nativa) y cada pregunta tiene su propia URL, por lo que se puede enlazar, recargar o marcar como favorita.

El costo de esta decisión es una recarga de página por respuesta. Para un cuestionario de ocho preguntas es un costo aceptable.

---

## 3. Arquitectura propuesta

Monolito modular con **núcleo aislado**: el dominio no conoce Flask.

```text
              NAVEGADOR
                  |
      formularios HTML (POST) + enlaces (GET)
                  |
                  v
        +---------------------+
        |       app.py        |   Adaptador web
        |  rutas + sesión     |   (lo único que importa Flask)
        +----------+----------+
                   |  llama a funciones puras
                   v
        +---------------------+
        |   domain/evaluador  |   calificar() · resumen()
        +----------+----------+
                   |
                   v
        +---------------------+
        |    domain/banco     |   Preguntas y respuestas
        +---------------------+

        templates/ + static/  ->  presentación
```

### Responsabilidades

- **`domain/banco.py`:** banco de preguntas con sección, tema, enunciado, cuatro opciones, respuesta correcta y explicación. Sin dependencias externas.
- **`domain/evaluador.py`:** `calificar(numero, opcion)` y `resumen(respuestas)`. Funciones puras: entran datos, salen datos.
- **`app.py`:** traduce HTTP a llamadas del dominio y guarda el avance en la sesión. Es el único módulo que importa Flask.
- **`templates/`, `static/`:** presentación editorial.

### Justificación arquitectónica

La dirección de las dependencias es la que propone **Clean Architecture**: `app.py` importa `domain`, y `domain` no importa nada del framework. En términos de **arquitectura hexagonal**, las funciones del evaluador son el puerto y las rutas de Flask son el adaptador HTTP.

Se aplica el patrón **POST/Redirect/GET**: al responder se hace `POST`, se guarda en la sesión y se redirige a la misma pregunta con `GET`. Así, recargar la página no reenvía el formulario ni duplica respuestas.

No se usan microservicios ni EDA: son conceptos evaluados en el cuestionario, pero aplicarlos aquí solo añadiría infraestructura sin resolver ningún problema del proyecto.

---

## 4. Funcionalidad del quiz

- 8 preguntas, cuatro opciones cada una, agrupadas en tres secciones temáticas.
- **Índice navegable** en la portada: se puede ir a cualquier pregunta.
- Una **URL por pregunta** (`/pregunta/3`), recargable y enlazable.
- Al responder: se marca la correcta, se señala la elegida si fue errónea y se muestra la explicación.
- Barra de progreso con el número de preguntas respondidas.
- El avance persiste en la sesión: se puede cerrar la pestaña y continuar.
- Resultado final con puntuación, porcentaje, mensaje y **revisión completa** con enlace para volver a cada pregunta.
- Las preguntas no respondidas se contabilizan como incorrectas y se señalan como "sin responder".

### Banco de preguntas

| # | Sección | Tema | Correcta |
|---|---|---|---|
| 1 | I. Fundamentos | Stack tecnológico | A |
| 2 | I. Fundamentos | Monolito modular | B |
| 3 | II. Estilos arquitectónicos | Hexagonal — puertos | C |
| 4 | II. Estilos arquitectónicos | Hexagonal — adaptadores | A |
| 5 | II. Estilos arquitectónicos | Clean Architecture | B |
| 6 | II. Estilos arquitectónicos | Arquitectura orientada a eventos | D |
| 7 | III. Proceso y despliegue | Pull Request | A |
| 8 | III. Proceso y despliegue | Despliegue en Render | C |

Contenido completo en [domain/banco.py](domain/banco.py).

---

## 5. Diseño de la interfaz

Estética de cuadernillo impreso: papel crema, serif, reglas finas y numeración al margen.

```text
              INGENIERÍA DE SOFTWARE II
        Cuadernillo de Stack y Arquitecturas
              NOMBRE DEL ESTUDIANTE
  ------------------------------------------------

  ÍNDICE / II. ESTILOS ARQUITECTÓNICOS / PREGUNTA 3 DE 8
  ________________________________________________
  [======================------------------------]

  ARQUITECTURA HEXAGONAL

  03
  ¿Qué representan los puertos en la
  arquitectura hexagonal?
  ------------------------------------------------
   (A)  Las bases de datos utilizadas
  ------------------------------------------------
   (B)  Los servidores de despliegue
  ------------------------------------------------
   (C)  Interfaces mediante las cuales el núcleo
        se comunica con el exterior
  ------------------------------------------------
   (D)  Componentes exclusivos del frontend
  ------------------------------------------------

   [ Comprobar respuesta ]   [ Anterior ]
```

Tras responder:

```text
   (C)  Interfaces mediante las cuales el núcleo...
        RESPUESTA CORRECTA

   | RESPUESTA CORRECTA
   | Un puerto es un contrato que define el núcleo.
   | El exterior debe adaptarse a ese contrato,
   | nunca al contrario.

   [ Anterior ]   [ Siguiente pregunta ]
```

Al finalizar:

```text
              RESULTADO FINAL

                   7/8
             88% DE ACIERTOS

     Buen desempeño. Conviene repasar los
       puntos señalados más abajo.

              — § —

  REVISIÓN DEL CUESTIONARIO
  | 01  STACK TECNOLÓGICO        CORRECTA
  | 06  EDA                      INCORRECTA
  |     Respondiste A; la correcta era D    revisar
```

---

## 6. Estructura del proyecto

```text
version-3-editorial/
├── app.py
├── requirements.txt
├── domain/
│   ├── banco.py
│   └── evaluador.py
├── templates/{base,portada,pregunta,resultado,error}.html
└── static/css/editorial.css
```

---

## 7. Flujo de Git y GitHub

1. **Fork** del repositorio original.
2. **Clone:** `git clone URL_DEL_FORK`
3. **Entorno virtual:**
   ```bash
   python -m venv .venv
   ```
   ```bash
   .venv\Scripts\activate
   ```
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecución local** antes de modificar nada.
5. **Rama:**
   ```bash
   git checkout -b feature/quiz-arquitecturas
   ```
6. **Desarrollo:** dominio, rutas, plantillas y hoja de estilos.
7. **Commit:**
   ```bash
   git commit -m "feat: cuadernillo de arquitecturas renderizado en servidor"
   ```
8. **Push:**
   ```bash
   git push origin feature/quiz-arquitecturas
   ```
9. **Pull Request** hacia el repositorio original, en un solo párrafo.

### Texto sugerido para el Pull Request

> [NOMBRE DEL ESTUDIANTE] reimaginó la aplicación base como un cuadernillo digital de Stack y Arquitecturas de Software en el que cada una de las ocho preguntas ocupa su propia página y su propia URL, resolviendo toda la interacción con formularios HTML y la sesión de Flask en lugar de JavaScript, de modo que existe una única fuente de verdad en el servidor y la aplicación sigue siendo utilizable sin scripts en el navegador, y separando el banco de preguntas y las reglas de calificación en un paquete de dominio que no importa Flask, con las rutas actuando como adaptador web sobre ese núcleo según la regla de dependencia de Clean Architecture, todo ello acompañado de una interfaz de estética editorial con índice navegable, barra de avance, retroalimentación explicada para cada respuesta y una revisión final que permite volver a cualquier pregunta, con el propósito de convertir la aplicación en un recurso didáctico coherente con los conceptos estudiados durante Ingeniería de Software II.

---

## 8. Despliegue en Render

```text
GitHub -> Render -> Build -> Deploy -> URL pública
```

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Variable de entorno `SECRET_KEY`:** obligatoria en producción. Firma la cookie de sesión donde se guarda el avance; si se deja el valor por defecto, cualquiera podría falsificarla.

---

## 9. Pipeline de la evaluación

```text
FORK -> CLONE -> EJECUCIÓN LOCAL (.venv) -> RAMA feature/*
     -> MODIFICACIÓN HTML/CSS + QUIZ -> COMMIT -> PUSH
     -> PULL REQUEST -> RENDER -> URL PÚBLICA
```

---

## 10. Evidencias obligatorias

1. Fork en GitHub.
2. Repositorio clonado (terminal).
3. `.venv` activo (terminal).
4. Aplicación original en el navegador.
5. `git branch` con la rama de trabajo.
6. Portada con el nombre del estudiante.
7. Una pregunta con sus cuatro opciones.
8. Retroalimentación de respuesta correcta.
9. Retroalimentación de respuesta incorrecta.
10. Resultado final con la revisión.
11. Commit en GitHub.
12. Pull Request.
13. Deploy exitoso en Render.
14. URL pública funcionando.

> Extra recomendado: captura de la barra de direcciones mostrando `/pregunta/3`. Evidencia que cada pregunta tiene su propia URL y que el estado vive en el servidor.

---

## 11. Relación entre los temas y el proyecto

| Tema | Cómo se evidencia |
|---|---|
| Stack tecnológico | Pregunta 1 y justificación del stack |
| Monolito modular | Pregunta 2 y organización del proyecto |
| Arquitectura hexagonal | Preguntas 3 y 4; dominio como núcleo, rutas como adaptador |
| Clean Architecture | Pregunta 5 y regla de dependencia aplicada en el código |
| EDA | Pregunta 6 |
| Cliente-servidor | Todo el estado vive en el servidor; el cliente solo envía formularios |
| Git / Pull Request | Pregunta 7, rama, commit, push y PR |
| Render | Pregunta 8, despliegue y URL pública |

---

## 12. Reflexión arquitectónica

La pregunta que guía esta versión es dónde debe vivir el estado. Una implementación con JavaScript mantiene el avance en el navegador y consulta al servidor solo para validar; aquí ocurre lo contrario: el navegador no guarda nada y el servidor es la única autoridad. Eso simplifica el razonamiento —no hay dos copias del estado que puedan desincronizarse— a cambio de una recarga por respuesta.

La separación entre `domain` y `app.py` no es decorativa. Como el evaluador son funciones puras sin dependencias de Flask, se pueden ejecutar y probar directamente desde el intérprete. Esa es exactamente la propiedad que buscan la arquitectura hexagonal y Clean Architecture: que las reglas de negocio no queden atrapadas dentro del framework.

También se aplicó POST/Redirect/GET, un patrón sencillo pero que evita un problema real: sin él, recargar la página de una pregunta reenviaría el formulario. Es un buen recordatorio de que muchas decisiones arquitectónicas se toman a esta escala, no solo al elegir entre monolito y microservicios.

---

## 13. Checklist

- [ ] Fork realizado
- [ ] Repositorio clonado
- [ ] `.venv` creado y dependencias instaladas
- [ ] Aplicación original ejecutada localmente
- [ ] Rama de trabajo creada
- [ ] Nombre del estudiante configurado en `app.py`
- [ ] Interfaz modificada
- [ ] Quiz implementado con 4 opciones por pregunta
- [ ] Opción seleccionada identificada
- [ ] Feedback correcto/incorrecto
- [ ] Resultado final y revisión
- [ ] Probado localmente
- [ ] `SECRET_KEY` configurada para producción
- [ ] Commit y push
- [ ] Pull Request creado
- [ ] Deploy exitoso en Render
- [ ] URL pública comprobada
- [ ] Evidencias capturadas
