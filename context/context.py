contexto = []
def agregar_contexto(texto):
    if len(contexto) > 10:  # Limitar la memoria
        contexto.pop(0)
    contexto.append(texto)

def obtener_contexto():
    return " ".join(contexto)