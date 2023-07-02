from bibtexparser import parse_file
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.milvus import Milvus
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from typing import Dict, List, Tuple
import json
import textwrap

print("retrieving huggingface embeddings")
embeddings = HuggingFaceEmbeddings()

print("retrieving milvus collection")
vector_store = Milvus(embeddings, "iCitation")

def search(sentence: str) -> Dict[str, List[Tuple[float, str]]]:
    print("searching with query: ", sentence)
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