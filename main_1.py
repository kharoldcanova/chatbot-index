from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openai import OpenAI
import json

# Initialize FastAPI
app = FastAPI()

# Configuración de Jinja2 para plantillas
templates = Jinja2Templates(directory="templates")

# Configura tu clave API de OpenAI aquí
api_key = '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'

client = OpenAI(api_key=api_key)

# Define a root route
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Usando el sistema de plantillas Jinja2
    return templates.TemplateResponse("index.html", {"request": request})

# set maximum input size
max_input_size = 4096
# set number of output tokens
num_outputs = 2000
# set maximum chunk overlap
max_chunk_overlap = 20
# set chunk size limit
chunk_size_limit = 600 

#Directory Path
directory_path = "./data"

# Define a route
@app.post("/query")
async def make_query(request: Request):
    try:
        # Obtiene el cuerpo de la solicitud y lo convierte de JSON a diccionario
        body = await request.json()
        query = body.get("query")

        # Verifica si el campo 'query' está presente
        if not query:
            raise HTTPException(status_code=400, detail="El campo 'query' es necesario")

        # Realiza una petición a la API de ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[{"role": "user", "content": query}],
            max_tokens=1000,
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
