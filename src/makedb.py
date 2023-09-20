from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

import os
import chromadb

def main():
    documents = []
    # Create a List of Documents from all of our files in the ./docs folder

    input_folder_path = f'input_documents'
    for file in os.listdir(input_folder_path):
        if file.endswith(".pdf"):
            pdf_path = "./" + input_folder_path + "/" + file
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
        elif file.endswith('.docx') or file.endswith('.doc'):
            doc_path = "./" + input_folder_path + "/" + file
            loader = Docx2txtLoader(doc_path)
            documents.extend(loader.load())
        elif file.endswith('.txt'):
            text_path = "./" + input_folder_path + "/" + file
            loader = TextLoader(text_path)
            documents.extend(loader.load())

    # Split the documents into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    documents = text_splitter.split_documents(documents)

    # Convert the document chunks to embedding and save them to the vector store
    from chromadb.config import Settings
    persist_directory = "./data"
    client_settings = Settings(anonymized_telemetry=False,
                               is_persistent=True,
                               persist_directory=persist_directory)
    collection_metadata = {"hnsw:num_threads": -1}

    vectordb = Chroma.from_documents(documents=documents,
                               embedding=OpenAIEmbeddings(),
                               persist_directory=persist_directory,
                               collection_name='UserData',
                               client_settings=client_settings,
                                collection_metadata=collection_metadata)
    vectordb.persist()

if __name__ == '__main__':
    main()