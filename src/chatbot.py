from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message=".*LangChain uses pydantic v2 internally.*"
)

import ollama
from src.vector_db import PineConeRAG


class MediBot:
    def __init__(self, model_name: str = 'llama2:latest'):
        # System prompt template
        self.system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )

        # Initialize Pinecone RAG retriever
        self.pinecone_rag_obj = PineConeRAG(mode='retrieval', index_name='medicalbot')
        self.retriever = self.pinecone_rag_obj.retriever

        # Initialize Ollama LLM
        self.llm = self.OllamaLLM(model_name)

    class OllamaLLM:
        def __init__(self, model_name: str):
            self.model_name = model_name

        def __call__(self, prompt, **kwargs):
            # Render prompt to string (LangChain passes ChatPromptValue)
            if hasattr(prompt, "format"):
                rendered_prompt = prompt.format(**kwargs)
            else:
                rendered_prompt = str(prompt)

            # Send to Ollama chat API
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": rendered_prompt}]
            )
            return response['message']['content']

    def ask(self, question: str) -> str:
        """
        Ask a question to the RAG + LLM pipeline
        """

        # 1️⃣ Create prompt template with placeholder {input} to match LangChain expectations
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "{input}")  # must be {input}, not {question}
            ]
        )

        # 2️⃣ Create document chain
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)

        # 3️⃣ Create retrieval chain
        rag_chain = create_retrieval_chain(self.retriever, question_answer_chain)

        # # print retrived docs
        # retrieved_docs = self.retriever.get_relevant_documents(question)
        # print("&&&&&&$$$$$$$$Retrieved context:")
        # for i, doc in enumerate(retrieved_docs, 1):
        #     print(f"Doc {i}: {doc.page_content}\n")
        
        result = rag_chain.invoke({"input": question})
        if isinstance(result, dict):
            # "answer" key usually contains text
            return result.get("answer", str(result))
        return str(result)


if __name__ == "__main__":
    medibot = MediBot()
    questions = "What is hypertension?"

    answer = medibot.ask(questions)

    print("Question:", questions)
    print("Answer:", answer)
