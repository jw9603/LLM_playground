import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
import os
from retriever import create_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_teddynote import logging
from dotenv import load_dotenv



load_dotenv()

logging.langsmith('[Project] Multi Turn 챗봇🍟')

# Cache Directory 생성
if not os.path.exists('.cache'):
    os.mkdir('.cache')

if not os.path.exists('.cache/files'):
    os.mkdir('.cache/files')

if not os.path.exists(".cache/embeddings"):
    os.mkdir('.cache/embeddings')

st.title('대화 내용을 기억하는 챗봇🍟')

# 처음 1번만을 실행하기 위한 코드
if 'messages' not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state['messages'] = []

if "store" not in st.session_state:
    st.session_state['store'] = {}
     


# sidebar 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_button = st.button('대화 초기화')

    # 모델 선택 메뉴
    selected_model = st.selectbox("LLM 선택", ['gpt-4o', 'gpt-4o-mini'], index=0)
    
    # 세션 ID를 지정하는 메뉴
    session_id = st.text_input("세션 ID를 입력하세요.", "abc123")
    

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))




# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_ids):
    if session_ids not in st.session_state['store']:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        st.session_state['store'][session_ids] = ChatMessageHistory()
    return st.session_state['store'][session_ids]  # 해당 세션 ID에 대한 세션 기록 반환

# 체인 생성
def create_chain(model_name='gpt-4o'):
    # 프롬프트 정의
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "당신은 Question-Answering 챗봇입니다. 주어진 질문에 대한 답변을 제공해주세요.",
            ),
            # 대화기록용 key 인 chat_history 는 가급적 변경 없이 사용하세요!
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "#Question:\n{question}"),  # 사용자 입력을 변수로 사용
        ]
    )

    # llm 생성
    llm = ChatOpenAI(model_name="gpt-4o")

    # 일반 Chain 생성
    chain = prompt | llm | StrOutputParser()
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,  # 세션 기록을 가져오는 함수
        input_messages_key="question",  # 사용자의 질문이 템플릿 변수에 들어갈 key
        history_messages_key="chat_history",  # 기록 메시지의 키
    )
    
    return chain_with_history


# 초기화 버튼이 눌리면...
if clear_button:
    st.session_state['messages'] = []

print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보시오.")

# 경고 메시지를 띄우기 위한 빈 영역
warning_messae = st.empty()

if "chain" not in st.session_state:
    st.session_state['chain'] = create_chain(model_name=selected_model)


# 만약 사용자 입력이 들어오면..
if user_input:
    chain = st.session_state['chain']
    
    if chain is not None:
    
        response = chain.stream(
            # 질문 입력
            {"question": user_input},
            # 세션 ID 기준으로 대화를 기록합니다.
            config={"configurable": {"session_id": session_id}},
        )
        # 사용자의 입력
        st.chat_message("user").write(user_input)

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
    
