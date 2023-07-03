from bibtexparser import parse_file
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.milvus import Milvus
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, connections, utility
from typing import Dict, List, Tuple
import json
import textwrap

connections.connect()

def create_collection():
    if utility.has_collection("iCitation"):
        print("Dropping iCitation collection")
        collection = Collection("iCitation")
        collection.drop()

    print("Creating iCitation collection")
    # 1. define fields
    fields = [
        FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65_535),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=768)
    ]
    # 2. enable dynamic schema in schema definition
    schema = CollectionSchema(
            fields, 
            "The schema for the sources", 
            enable_dynamic_field=True
    )

    # 3. reference the schema in a collection
    collection = Collection("iCitation", schema)

    # 4. index the vector field and load the collection
    index_params = {
        "metric_type": "L2",
        "index_type": "HNSW",
        "params": {"M": 8, "efConstruction": 64},
    }

    collection.create_index(
        field_name="vector", 
        index_params=index_params
    )

    # 5. load the collection
    collection.load()
    print("iCitation collection loaded")

def search(sentence: str) -> Dict[str, List[Tuple[float, str]]]:
    print("searching with query: ", sentence)
    vector_store: Milvus
    output = vector_store.similarity_search_with_score(sentence, 5)
    sources = {}

    for doc, score in output:
        text = doc.page_content
        source = json.loads(doc.metadata['metadata'].decode('utf-8'))['source']
        wrapped_text = '\n'.join(textwrap.wrap(text, width=60))

        if source in sources:
            sources[source].append((score, wrapped_text))
        else:
            sources[source] = [(score, wrapped_text)]

    print("searching done")
    return sources

create_collection()

print("retrieving HuggingFace embeddings")
embeddings = HuggingFaceEmbeddings()

print("retrieving iCitation collection")
vector_store = Milvus(embeddings, "iCitation")