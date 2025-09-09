from langchain_community.document_loaders import PDFPlumberLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
    
def create_retriever(file_path):
# RAG
    # 1단계: 문서 로드
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()

    # 2단계: 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_documents = text_splitter.split_documents(docs)

    # 3단계: 임베딩 생성
    embeddings = OpenAIEmbeddings()

    # 4단계: DB
    vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
 
    # 5단계: Retriever
    retriever = vectorstore.as_retriever()
    
    return retriever