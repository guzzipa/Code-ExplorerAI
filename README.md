# LangChain Git Integration

Este proyecto utiliza LangChain para analizar repositorios Git y realizar consultas sobre los archivos Python.

## Características
- Clona un repositorio Git.
- Divide los archivos en trozos procesables.
- Crea embeddings utilizando OpenAI.
- Permite consultas conversacionales sobre el código.

## Configuración
1. Crea un archivo `.env` con las siguientes claves:

OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


2. Instala las dependencias:
```bash pip install -r requirements.txt```

3. corre el Script 
python main.py
