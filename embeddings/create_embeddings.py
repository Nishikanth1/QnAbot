
import logging
import sys
import faiss

from langchain.docstore.document import Document 
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from config import MODEL_NAME
from text_splitter import TextSplitter


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logging.basicConfig(encoding='utf-8', format='%(asctime)s %(levelname)s  %(message)s', level=logging.INFO)



class Embeddings:
    def __init__(self, model=MODEL_NAME) -> None:
        self.embedding_model = OllamaEmbeddings(model=model)
        #set index by running a sample query to get embedding dimension
        self.index = faiss.IndexFlatL2(len(self.embedding_model.embed_query("sample query")))
        self.vector_store = FAISS(
                                embedding_function=self.embedding_model,
                                index=self.index,
                                docstore=InMemoryDocstore(),
                                index_to_docstore_id={},
                            )
    
    def create_embeddings(self, file_path):
        text_splitter = TextSplitter(file_path)
        logger.info(f"creating embeddings and adding to vector store for {file_path}")
        for split in text_splitter.split():
            docs_content = [doc.page_content if isinstance(doc, Document) and doc.page_content else doc for doc in split]
            docs_embeddings = self.embedding_model.embed_documents(docs_content)
            content_and_embeddings = list(zip(docs_content, docs_embeddings))
            self.vector_store.add_embeddings(content_and_embeddings)
        logger.info(f"created embeddings and added to vector store for {file_path}")

    def get_similar_context(self, query):
        logger.info(f"getting similar context for <<{query}>>")
        return self.vector_store.similarity_search(query)

if __name__ == "__main__":
    embedder = Embeddings(MODEL_NAME)
    embedder.create_embeddings("./data/documents/Deloitte-SOC2.pdf")
    query = "What is soc2 report"
    print(embedder.vector_store.similarity_search(query))
    
    # embedder.create_embeddings("./data/documents/logs.json")
    # embedder.create_embeddings("./data/documents/open_api.json")
    