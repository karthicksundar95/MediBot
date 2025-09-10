from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=".*LangChain uses pydantic v2 internally.*"
)

load_dotenv()


class PineConeRAG:
    def __init__(self, mode:str, path:str=None, index_name=None):
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2") 
        self.pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        self.path = path
        self.mode = mode
        if self.mode.lower() == "indexing":
            self.read_data()
            self.chunk_documents()
            self.connect_to_pinecone()
            self.create_index()
        elif self.mode.lower() == 'retrieval':
            self.connect_to_pinecone()
            self.create_retriever(index_name)

    def read_data(self):
        dir_loader = DirectoryLoader(self.path,
                                        glob="*pdf",
                                        loader_cls=PyPDFLoader)
        self.documents = dir_loader.load()
        logging.info(f"Documents are read from the path {self.path} successfully!")        

    def chunk_documents(self):
        chunker = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        self.text_chunks = chunker.split_documents(self.documents)

    def connect_to_pinecone(self):
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        logging.info("Successfully established connection to Pinecone!")

    def create_index(self):
        self.index_name = "medicalbot"
        # 2️⃣ Delete the old index if it exists
        if self.index_name in [i["name"] for i in self.pc.list_indexes()]:
            self.pc.delete_index(self.index_name)
            logging.info(f"Deleted existing Pinecone index: {self.index_name}")

        # 3️⃣ Create a new index with correct dimension
        self.pc.create_index(
            name=self.index_name,
            dimension=384,  # match your embeddings
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        logging.info(f"Created new Pinecone index: {self.index_name} with dimension 384")

        # 4️⃣ Get the Pinecone Index object
        self.index = self.pc.Index(self.index_name)

        # 5️⃣ Create the LangChain vector store using the Index object
        self.vectorstore = PineconeVectorStore.from_documents(
            documents=self.text_chunks[:10],
            index_name=self.index_name,
            embedding=self.embeddings
        )
        logging.info(f"Documents embedded and stored in PineconeVectorStore: {self.index_name}")

    def create_retriever(self, index_name:str):
        docsearch = PineconeVectorStore.from_existing_index(
                                                            index_name=index_name,
                                                            embedding=self.embeddings
                                                        )
        # define retreiver using pinecone object
        self.retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

if __name__ == "__main__":
    # Check indexing
    # PineConeRAG(path="./data", mode='indexing')

    # Check retrieval
    retrieval_obj = PineConeRAG(mode='retrieval', index_name='medicalbot')

    query_result = retrieval_obj.retriever.get_relevant_documents("Mary Beth Trimper")

    print("Number of results:", len(query_result))
    for i, doc in enumerate(query_result, 1):
        print(f"Result {i}:", doc.page_content)