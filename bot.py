from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

from config import MODEL_NAME
from embeddings.create_embeddings import Embeddings


template = """Answer the question based only on the following context: Reply with 'I dont know' if context is not relevant.

context: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

class Bot:
    def __init__(self) -> None:
        self.chain = None
        self.model = ChatOllama(model=MODEL_NAME)
        self.embedder = Embeddings(MODEL_NAME)
    
    def add_files_to_store(self, file_path_list):
        for file_path in file_path_list:
            self.embedder.create_embeddings(file_path) 

    def ask_question(self, query):
        if not self.chain:
            self.chain = (
                    {"context": self.embedder.vector_store.as_retriever() | format_docs, "question": RunnablePassthrough()}
                    | prompt
                    | self.model
                    | StrOutputParser()
                )
        return self.chain.invoke(query)

if __name__ == "__main__":
    query = "who needs soc2 report"
    file_path_list = ["data/documents/deloitte-soc2-short.pdf"]
    bot = Bot()
    resp = bot.add_files_to_store(file_path_list)
    resp = bot.ask_question(query)
    
    print(f"response for query: <<{query}>> is response: <<{resp}>>")