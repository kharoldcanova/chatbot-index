from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openai import OpenAI as OpenAIAPI
import os
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from dotenv import load_dotenv

# Carga el archivo .env
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Configuración de Jinja2 para plantillas
templates = Jinja2Templates(directory="templates")

# Configura tu clave API de OpenAI aquí
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise Exception("No se encontró la clave API de OpenAI")
client = OpenAIAPI(api_key=api_key)

# Define a root route
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define a route
@app.post("/query")
async def make_query(request: Request):
    try:
        body = await request.json()
        query = body.get("query")

        if not query:
            raise HTTPException(status_code=400, detail="El campo 'query' es necesario")

        # Primero consulta el índice de LlamaIndex
        documents = SimpleDirectoryReader('data').load_data()
        index = VectorStoreIndex.from_documents(documents)

        # Luego utiliza LlamaIndex para generar una respuesta más detallada
        response = index.as_query_engine(query)

        # Luego utiliza OpenAI para generar una respuesta más detallada
        openai_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": response}],
            max_tokens=1000,
        )

        return {"reply": openai_response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
