import test.ollama as ollama

prompt = input

response = ollama.chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

ouput_ollama = response["message"]["content"]
print("Ely:", ouput_ollama)