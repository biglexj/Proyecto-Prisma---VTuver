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
1. **Carga de Datos**:
   - Carga la personalidad de Ely desde un archivo JSON (`data/ely_personality.json`).
   - Carga las reglas predefinidas para responder preguntas desde otro archivo JSON (`data/ely_rules.json`).

2. **Conexión con YouTube**:
   - Utiliza `ChatDownloader` para conectarse al chat en vivo de YouTube y obtener los mensajes en tiempo real.

3. **Procesamiento de Mensajes**:
   - Procesa cada mensaje del chat, buscando coincidencias con las reglas predefinidas utilizando la biblioteca `rapidfuzz`.
   - Genera una respuesta utilizando el modelo de lenguaje Ollama, que se ajusta a la personalidad de Ely.

4. **Filtrado de Texto**:
   - Filtra el texto generado para eliminar análisis internos y asegurar que la respuesta sea coherente y adecuada.

5. **Síntesis de Voz**:
   - Convierte la respuesta generada a voz utilizando el modelo TTS de Coqui.
   - Reproduce el audio generado en tiempo real para que Ely pueda "hablar" en la transmisión en vivo.

### Tecnologías Utilizadas
- **Python**: Lenguaje de programación principal del proyecto.
- **ChatDownloader**: Biblioteca para descargar y procesar chats en vivo de YouTube.
- **Ollama**: Modelo de lenguaje utilizado para generar respuestas complejas y naturales.
- **Coqui TTS**: Modelo de síntesis de voz utilizado para convertir texto a voz.
- **RapidFuzz**: Biblioteca utilizada para encontrar coincidencias entre los mensajes del chat y las reglas predefinidas.
- **SoundDevice**: Biblioteca para reproducir el audio generado en tiempo real.

### Instalación y Ejecución
Para instalar y ejecutar el proyecto, sigue estos pasos:

1. Clona el repositorio:
   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd Proyecto-Prisma---VTuver

2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt

3. Ejecuta el archivo principal:
   ```sh
   python main.py

Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles