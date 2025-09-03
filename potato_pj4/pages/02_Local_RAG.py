import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote.prompts import load_prompt
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
import os
from retriever import create_retriever
from langchain_teddynote import logging
from dotenv import load_dotenv


load_dotenv()

logging.langsmith('[Project] PDF RAG')

# Cache Directory 생성
if not os.path.exists('.cache'):
    os.mkdir('.cache')

if not os.path.exists('.cache/files'):
    os.mkdir('.cache/files')

if not os.path.exists(".cache/embeddings"):
    os.mkdir('.cache/embeddings')

st.title('Talking Potatio의 Local Model 기반 RAG🍟')

# 처음 1번만을 실행하기 위한 코드
if 'messages' not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state['messages'] = []

if 'chain' not in st.session_state:
    st.session_state['chain'] = None

# sidebar 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_button = st.button('대화 초기화')
    # 파일 업로드
    uploaded_file = st.file_uploader("파일 업로드", type='pdf')

    # 모델 선택 메뉴
    selected_model = st.selectbox("LLM 선택", ['gpt-4o', 'gpt-4-turbo', 'gpt-4o-mini', 'ollama'], index=0)

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

# 파일을 캐시에 저장(시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner="업로드한 파일을 처리 중...!")
def embed_file(file):
    # 업로드한 파일을 캐시 디렉토리에 저장
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    # RAG
    return create_retriever(file_path)

def format_doc(document_list):
    return '\n\n'.join([doc.page_content for doc in document_list])

def create_chain(retriever, model_name='gpt-4o'):

    
    if model_name == 'ollama':
        # 6단계
        prompt = load_prompt("./prompts/pdf-rag-ollama.yaml")
        # 7단계: LLM
        llm = ChatOllama(model='EEVE-KOREAN-10.8B:latest', temperature=0)
    else:
        # 6단계
        prompt = load_prompt("./prompts/pdf-rag.yaml")
        # 7단계: LLM
        llm = ChatOpenAI(model=model_name, temperature=0)

    #8단계
    chain = (
        {"context": retriever | format_doc, "question": RunnablePassthrough()}
        | prompt
        | llm
        |StrOutputParser()
    )

    return chain

# 파일이 업로드 되었을 때 처리
if uploaded_file:
    retriever = embed_file(uploaded_file)
    chain = create_chain(retriever, model_name=selected_model)
    st.session_state['chain'] = chain

# 초기화 버튼이 눌리면...
if clear_button:
    st.session_state['messages'] = []

print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보시오.")

# 경고 메시지를 띄우기 위한 빈 영역
warning_messae = st.empty()

# 만약 사용자 입력이 들어오면..
if user_input:
    
    # chain 을 생성
    chain = st.session_state['chain']

    if chain is not None:
        # 웹에 대화를 출력(사용자의 입력)
        st.chat_message("user").write(user_input)
        # Streaming 할 경우
        response = chain.stream(user_input)
        with st.chat_message('assistant'):
            # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
            container = st.empty()
            ai_answer = ''
            for token in response:
                ai_answer += token
                container.markdown(ai_answer)

        # 대화 기록을 저장한다.
        add_message("user", user_input)
        add_message('assistant', ai_answer)
    
    else:
        # 파일을 업로드 하라는 경고 메시지 출력
        warning_messae.warning('파일을 업로드 해주세요.')
