from fastapi import FastAPI, HTTPException, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import index_llm as index_llm
import os
# Configuración de FastAPI
app = FastAPI()

# Configuración de Jinja2 para plantillas
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Usando el sistema de plantillas Jinja2
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/check-files")
async def check_files():
    # Verificar si hay archivos CSV en la carpeta 'data'
    files_exist = os.path.exists("data") and any(file.endswith('.csv') for file in os.listdir("data"))

    return {"filesExist": files_exist}

@app.get("/delete-files")
async def delete_files():
    # Eliminar los archivos CSV de la carpeta 'data'
    for file in os.listdir("data"):
        if file.endswith('.csv'):
            os.remove(os.path.join("data", file))

# @app.get("/query", response_class=HTMLResponse)
# async def query(request: Request):
#     try:
#         query = request.query_params["query"]
#         if not query:
#             raise HTTPException(status_code=400, detail="No query provided")
#         response = index_llm.construct_index("./dataclients", query)
#         return templates.TemplateResponse("index.html", {"request": request, "response": response})

#     except Exception as e:
#         raise HTTPException(status_code=400, detail="No query provided")

# Entrada de la respuesta
@app.post("/query")  
async def query(request: Request):
    try:
        data = await request.json()
        query = data.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="No query provided")
        response = index_llm.construct_index("./data", query)
        return {"reply": response}  # Asegúrate de devolver la respuesta en el formato esperado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enviar un archivo CSV
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")

    # Ruta de la carpeta donde se guardarán los archivos
    folder_path = "data"
    os.makedirs(folder_path, exist_ok=True)  # Crea la carpeta si no existe

    file_location = f"{folder_path}/{file.filename}"

    # Guardar el archivo en la carpeta
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8081)
