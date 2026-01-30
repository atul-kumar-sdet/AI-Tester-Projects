import ollama

try:
    models = ollama.list()
    print(models)
except Exception as e:
    print(e)
