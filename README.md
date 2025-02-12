Proyecto de Chat de YouTube con Síntesis de Voz
Este proyecto permite descargar y procesar chats en vivo de YouTube, generando respuestas automáticas y sintetizando audio para reproducir las respuestas.

Características
Descarga de Chats en Vivo: Utiliza ChatDownloader para conectarse y descargar mensajes de chat en vivo desde YouTube.
Procesamiento de Mensajes: Extrae y procesa mensajes de chat, incluyendo el nombre del autor y el contenido del mensaje.
Generación de Respuestas: Utiliza ollama_engine para generar respuestas basadas en el texto del chat y una personalidad definida.
Síntesis de Voz: Convierte las respuestas generadas en audio utilizando un modelo de voz predefinido.
Gestión de Contexto: Mantiene un historial de contexto limitado para mejorar la coherencia de las respuestas.
Requisitos
Python 3.11.9 usado
Paquetes de Python: ChatDownloader, re, os, torch, sounddevice, entre otros.
Uso
Clona el repositorio.
Instala los paquetes necesarios utilizando pip:
Ejecuta el script main.py para iniciar la descarga y procesamiento del chat.
Ejemplo de Ejecución
Estructura del Proyecto
main.py: Script principal que maneja la descarga y procesamiento del chat.
model_voz/: Directorio que contiene el modelo de voz utilizado para la síntesis de audio.
Notas
Asegúrate de que el archivo de modelo de voz (Ely_model.wav) esté presente en el directorio model_voz/cloning/.
El script maneja excepciones y errores comunes, proporcionando mensajes de error claros.