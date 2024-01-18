import chromadb

#Instancia
chroma_client = chromadb.Client()

#Crea la colección
collection = chroma_client.get_or_create_collection(name="my_collection")

