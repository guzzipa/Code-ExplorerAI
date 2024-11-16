import os
from git import Repo
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PythonLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory

from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
token = os.getenv("GITHUB_TOKEN")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Falta la clave OPENAI_API_KEY en las variables de entorno.")

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("Falta el token GITHUB_TOKEN en las variables de entorno.")



repo_path = "uala-dataml-cumple_new/"

# Verificar si el repositorio ya está clonado
if not os.path.exists(os.path.join(repo_path, ".git")):
    print("Repositorio no clonado, clonando ahora...")
    Repo.clone_from(f"https://{token}@github.com/Bancar/uala-dataml-cumple.git", repo_path)
else:
    print("El repositorio ya está clonado, usando el existente.")

# Buscar todos los archivos .py en el directorio
file_paths = [
    os.path.join(root, file)
    for root, _, files in os.walk(repo_path)
    for file in files if file.endswith(".py")
]

# Cargar documentos desde archivos Python
documents = []
for file_path in file_paths:
    loader = PythonLoader(file_path)
    documents.extend(loader.load())

print("Documentos cargados:", documents)

# Dividir documentos en trozos para embeddings
documents_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=200,
    chunk_overlap=50
)
texts = documents_splitter.split_documents(documents)

# Crear embeddings
#embeddings = OpenAIEmbeddings(disallowed_special=())
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, disallowed_special=())



# Crear vectorstore persistente
vectordb = Chroma.from_documents(texts, embedding=embeddings, persist_directory='./data')

# Crear LLM y memoria de conversación
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
#llm = ChatOpenAI()
memory = ConversationSummaryMemory(llm=llm, memory_key="chat_history", return_messages=True)

# Crear la cadena de recuperación conversacional
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectordb.as_retriever(search_type="mmr"),
    memory=memory
)

# Realizar una pregunta
question = "que es lo que sabes ? podes sugerir cambios mejoras o nuevos features para este codigo ? "
result = qa(question)
print(result['answer'])

