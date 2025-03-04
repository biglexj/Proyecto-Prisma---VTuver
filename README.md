# Proyecto-Prisma---VTuver--

## Explicación del Proyecto

### Descripción General
Proyecto-Prisma es una aplicación interactiva que simula una VTuber llamada Ely. Ely está diseñada para interactuar con los usuarios en transmisiones en vivo de YouTube, respondiendo preguntas y generando respuestas de manera dinámica y entretenida. Utiliza modelos avanzados de lenguaje y síntesis de voz para proporcionar una experiencia inmersiva y realista.

### Funcionamiento de `main.py`
El archivo `main.py` es el núcleo del proyecto y realiza las siguientes tareas:

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

### Estructura del Proyecto
- `main.py`: Archivo principal que maneja la interacción en tiempo real con el chat de YouTube, genera respuestas utilizando el modelo de lenguaje Ollama y sintetiza la voz de Ely.
- `context/json/ely_personality.json`: Archivo JSON que contiene la personalidad definida de Ely.
- `context/json/ely_rules.json`: Archivo JSON que contiene las reglas predefinidas para responder a preguntas comunes.
- `experimental/`: Directorio con scripts experimentales y pruebas.

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
    pip install -r requirements.txt

3. Ejecuta el archivo principal:
    python main.py

Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles. 