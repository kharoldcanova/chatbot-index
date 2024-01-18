from llama_index import SimpleDirectoryReader, PromptHelper, ServiceContext, VectorStoreIndex
from llama_index.llms import OpenAI
import os
import dotenv


dotenv.load_dotenv()

def construct_index(directory_path):

    # api key 
    api_key = os.environ.get('OPENAI_API_KEY')
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600 

    # set chunk overlap ratio (valor entre 0 y 1)
    chunk_overlap_ratio = 0.1  # ajusta este valor según tus necesidades

    # define prompt helper
    prompt_helper = PromptHelper(max_input_size, num_outputs, chunk_overlap_ratio, chunk_size_limit=chunk_size_limit)

    # define LLM
    # define HuggingFaceLLM
    llm = OpenAI(model="gpt-3.5-turbo-1106", temperature=0, max_tokens=num_outputs, openai_api_key=api_key)
 
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    service_context = ServiceContext.from_defaults(llm=llm, prompt_helper=prompt_helper)
    
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)

    # index.save_to_disk('index.json')

    query_engine = index.as_query_engine()
    response = query_engine.query("¿Cual es la edad de Sergio?")
    print(response)

construct_index("./data")

