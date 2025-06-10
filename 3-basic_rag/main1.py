import streamlit as st
from dotenv import load_dotenv

from langchain_teddynote import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

import os
import tempfile

# 환경 변수 로드
load_dotenv()
logging.langsmith('Basic-RAG-Streamlit')

st.set_page_config(page_title="PDF 기반 Q&A", page_icon="📄")
st.title("📄 PDF 기반 Q&A 서비스")

# 1. PDF 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드 해주세요", type=["pdf"])

if uploaded_file:
    # 1-1. 임시 파일로 저장
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_pdf_path = tmp_file.name

    # 2. 문서 로드
    loader = PyMuPDFLoader(tmp_pdf_path)
    docs = loader.load()

    # 3. 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    # 4. 임베딩 생성
    embeddings = OpenAIEmbeddings()

    # 5. 벡터 DB 생성
    vector_store = FAISS.from_documents(documents=split_documents, embedding=embeddings)

    # 6. Retriever 생성
    retriever = vector_store.as_retriever()

    # 7. 프롬프트 생성
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

    # 8. LLM + 체인 생성
    llm = ChatOpenAI(model_name='gpt-4o', temperature=0)
    chain = (
        {'context': retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 9. 사용자 질문 입력 받기
    question = st.text_input("❓ 궁금한 내용을 입력하세요")

    # 10. 질문 입력 시 응답 출력
    if question:
        st.markdown("### 🤖 답변")
        response_stream = chain.stream(question)

        # 실시간 응답 출력
        output_container = st.empty()
        full_response = ""
        for chunk in response_stream:
            full_response += chunk
            output_container.markdown(full_response)

else:
    st.info("먼저 PDF 파일을 업로드해주세요.")