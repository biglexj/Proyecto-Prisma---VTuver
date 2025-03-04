import signal
import sys
import time
import threading
import asyncio

from modules.chat_downloader import chat_loop
from context.ely_personality import ely_personality_text
from context.ely_rules import rule_resultado

async def main():
    print("Ely VTuber: Hola, empezando la matriz de interacción.")

    # Register signal handler so that all threads can be exited.
    def signal_handler(sig, frame):
        print("Received CTRL + C, attempting to gracefully exit. Close all dashboard windows to speed up shutdown.")
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Cargar la personalidad y las reglas
    ely_personality_text = ely_personality_text()
    ely_rules = rule_resultado()

    # Crear y ejecutar el hilo para el chat
    chat_thread = threading.Thread(target=chat_loop, daemon=True)
    chat_thread.start()

    while True:
        time.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
    