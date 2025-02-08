# Proyecto-Prisma---VTuver

## Descripción
Proyecto-Prisma es una aplicación interactiva que simula una VTuber llamada Ely. Ely es una VTuber virtual enérgica y amigable, diseñada para interactuar con los usuarios a través de chats en vivo de YouTube, respondiendo preguntas y generando respuestas de manera dinámica y entretenida.

## Características
- **Interacción en tiempo real**: Ely puede responder a preguntas en tiempo real durante transmisiones en vivo de YouTube.
- **Personalidad definida**: Ely tiene una personalidad bien definida, con características como su nombre, estilo visual, tono de voz, habilidades y más.
- **Respuestas personalizadas**: Ely utiliza reglas predefinidas para responder a preguntas comunes y generar respuestas coherentes con su personalidad.
- **Síntesis de voz**: Ely puede convertir texto a voz utilizando PowerShell para una experiencia más inmersiva.
- **Integración con modelos de lenguaje**: Ely utiliza el modelo de lenguaje Ollama para generar respuestas más complejas y naturales.

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:
- `main.py`: Archivo principal que maneja la interacción en tiempo real con el chat de YouTube, genera respuestas utilizando el modelo de lenguaje Ollama y sintetiza la voz de Ely.
- `data/ely_personality.json`: Archivo JSON que contiene la personalidad definida de Ely.
- `data/ely_rules.json`: Archivo JSON que contiene las reglas predefinidas para responder a preguntas comunes.
- `experimental/`: Directorio con scripts experimentales y pruebas.

## Funcionamiento de `main.py`
El archivo `main.py` realiza las siguientes tareas:
1. Carga la personalidad y las reglas de Ely desde archivos JSON.
2. Conecta con el chat en vivo de YouTube utilizando `ChatDownloader`.
3. Procesa cada mensaje del chat, buscando coincidencias con las reglas predefinidas.
4. Genera una respuesta utilizando el modelo de lenguaje Ollama.
5. Filtra el texto generado para eliminar análisis internos.
6. Convierte la respuesta a voz utilizando `pyttsx3`.
