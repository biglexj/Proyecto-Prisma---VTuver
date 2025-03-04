import json

def load_personality():
    with open("json/ely_personality.json", "r", encoding="utf-8") as archivo:
        ely_personality = json.load(archivo)

    ely_personality_text = (
        "Nombre: " + ely_personality["nombre"] + "\n" +
        "Personalidad: " + ely_personality["personalidad"] + "\n" +
        "Estilo Visual: " + ely_personality["estilo_visual"] + "\n" +
        "Interacciones: " + ely_personality["interacciones"] + "\n" +
        "Habilidades: " + ely_personality["habilidades"] + "\n" +
        "Tono de voz: " + ely_personality["tono_de_voz"] + "\n" +
        "Misión: " + ely_personality["mision"] + "\n" +
        "Bienvenida: " + ely_personality["bienvenida"] + "\n" +
        "Despedida: " + ely_personality["despedida"] + "\n" +
        "Humor: " + ely_personality["humor"]
    )

    return ely_personality_text 