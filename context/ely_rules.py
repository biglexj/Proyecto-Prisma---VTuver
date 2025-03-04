import json
import random
from rapidfuzz import process

def load_rules():
    with open("json/ely_rules.json", "r", encoding="utf-8") as file:
        ely_rules = json.load(file)
    return ely_rules

def rule_resultado(chat_YT, ely_rules):
    for clave, valor in ely_rules.items():
        if "pregunta" in valor:
            match = process.extractOne(chat_YT, valor["pregunta"])
            if match and match[1] > 80:
                if "respuesta_1" in valor:
                    return random.choice([valor["respuesta_1"], valor["respuesta_2"]])
                return valor["respuesta"]
    return "Toma un criterio neutral a las preguntas con un poco de sarcasmo de vez en cuando." 
