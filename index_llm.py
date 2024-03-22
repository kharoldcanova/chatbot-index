import os
import dotenv
from llama_index import SimpleDirectoryReader, PromptHelper, ServiceContext, VectorStoreIndex
from llama_index.llms import OpenAI
import pandas as pd
from llama_index import Document

dotenv.load_dotenv()

def load_api_key():
    return os.environ.get('OPENAI_API_KEY')

def create_prompt_helper():
    max_input_size = 4096
    num_outputs = 2000
    chunk_overlap_ratio = 0.1 
    chunk_size_limit = 600
    return PromptHelper(max_input_size, num_outputs, chunk_overlap_ratio, chunk_size_limit=chunk_size_limit)

def create_llm(api_key):
    return OpenAI(
        model="gpt-3.5-turbo-1106", 
        temperature=0, 
        max_tokens=2000, 
        openai_api_key=api_key,
        system_prompt= "Eres un asistente inteligente que responde preguntas sobre los clientes de Mil Mujeres. Tu nombre es Mil Mujeres Bot",
        )

# def create_index(directory_path, llm, prompt_helper):
#     documents = SimpleDirectoryReader(directory_path).load_data()
#     service_context = ServiceContext.from_defaults(llm=llm, prompt_helper=prompt_helper)
#     return VectorStoreIndex.from_documents(documents, service_context=service_context)

def create_index(directory_path, llm, prompt_helper):
    service_context = ServiceContext.from_defaults(llm=llm, prompt_helper=prompt_helper)

    # Lista para almacenar los documentos
    documentos = []

    # Leer cada archivo CSV en el directorio
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(file_path)

            # Transformar cada fila en un documento de texto
            for _, row in df.iterrows():
                texto = ', '.join(f"{key}: {value}" for key, value in row.items())
                documentos.append(Document(text=texto))

    # Crear el índice con los documentos
    return VectorStoreIndex.from_documents(documentos, service_context=service_context)


def query_index(index, query):
    query_engine = index.as_query_engine()
    return query_engine.query(query)

# def construct_index(directory_path):
#     api_key = load_api_key()
#     prompt_helper = create_prompt_helper()
#     llm = create_llm(api_key)
#     index = create_index(directory_path, llm, prompt_helper)
#     question = input("Ask a question: ")
#     response = query_index(index, question)
#     print(response)
#     return response

# construct_index("./dataclients")


def construct_index(directory_path, question):
    api_key = load_api_key()
    prompt_helper = create_prompt_helper()
    llm = create_llm(api_key)
    index = create_index(directory_path, llm, prompt_helper)
    #question = input("Ask a question: ")
    response = query_index(index, question)
    print(response)
    return response


