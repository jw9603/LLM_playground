from dotenv import load_dotenv
from langchain_teddynote import logging

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# 1. Load Documents
def load_document():
    loader = PyMuPDFLoader('./data/1.pdf')
    docs = loader.load()

    return docs

# 2. Split Document
def split_text(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    return split_documents

# 3. Embedding
def embed_document():
    embeddings = OpenAIEmbeddings()

    return embeddings

# 4. Vector Space 생성
def create_db(split_documents, embeddings):
    vector_store = FAISS.from_documents(documents=split_documents, embedding=embeddings)

    return vector_store

# 5. Retriever 생성
def create_retriever(vector_store):
    retriever = vector_store.as_retriever()

    return retriever

# 6. Prompt 생성
def create_prompt():
    prompt = PromptTemplate.from_template(
        """You are an assistant for question-answering tasks.
    You are given some context documents. Use them to help answer the question if relevant.
    If the context is not helpful, feel free to answer based on your own knowledge.
    Always include "page" number if the information is from context.
    Please Answer in Korean.
    
    #Context:
    {context}
    
    #Question:
    {question}
    
    #Answer: """
    )

    return prompt

# 7. LLM 생성
def define_llm():   
    llm = ChatOpenAI(model_name='gpt-4o', temperature=0)

    return llm

# 8. 체인 생성
def make_chain(retriever, prompt, llm):
    chain = (
        {'context': retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        |StrOutputParser()
    )

    return chain

def ask_user_question():
    print("\n주어진 PDF에 대해 궁금한 점을 입력하세요.")
    question = input().strip()
    return question

def ask_answer(retriever, question, llm, chain):
    # 문서 기반 체인 실행
    response = chain.stream(question)
    for tok in response:
        print(tok, end='', flush=True)


def main():
    # API 키 정보 로드
    load_dotenv()

    # LangSmith 추적 시작 및 프로젝트명 기입
    logging.langsmith('Basic-RAG')

    # 사전 단계
    docs = load_document()
    split_documents = split_text(docs)
    embeddings = embed_document()
    vector_store = create_db(split_documents, embeddings)

    # RumTime 단계
    retriever = create_retriever(vector_store)
    prompt = create_prompt()
    llm = define_llm()
    chain = make_chain(retriever, prompt, llm)

    # 체인 실행
    question = ask_user_question()

    ask_answer(retriever, question, llm, chain)

if __name__ == '__main__':
    main()    