import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from langchain import hub

from dotenv import load_dotenv
import glob

load_dotenv()

st.title("Talking 🥔의 Chat GPT")

# 처음 1번만 실행하기 위한 코드
if 'messages' not in st.session_state:
    # 대화 기록을 저장하기 위한 용도로 생성한다.
    st.session_state['messages'] = []

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

    prompt_files = glob.glob('./prompts/*.yaml')
    selected_prompt = st.selectbox(
    "프롬프트를 선택해 주세요.", prompt_files, index=0)
    task_input = st.text_input("Task 입력", "")
    

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        st.chat_message(chat_message.role).write(chat_message.content)

# 새로운 메시지를 추가
def add_messages(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

# 체인 생성
def create_chain(prompt_file_path, task=""):
    # Prompt 적용
    prompt = load_prompt(prompt_file_path, encoding="utf-8")

    if task:
        prompt = prompt.partial(task=task)
    
    # LLM
    llm = ChatOpenAI(model='gpt-4o', temperature=0)

    # 출력 파서
    output_parser= StrOutputParser()

    # 체인 생성
    chain = prompt | llm |output_parser

    return chain

if clear_btn:
    st.session_state['messages'] = []

# 이전 대화를 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어봐")

# 만약에 사용자 입력이 들어오면
if user_input:
    # 사용자의 입력
    st.chat_message("user:").write(user_input)
    # chain을 생성
    chain = create_chain(selected_prompt, task=task_input)

    # 스트리밍 호출
    response = chain.stream({'question':user_input})
    with st.chat_message('assistant'):
        # 빈 공간을 만들어서, 여기에 토큰을 스트리밍 출력한다.
        container = st.empty()

        ai_answer = ''
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # 대화 기록을 저장한다.
    add_messages('user', user_input)
    add_messages('assistant', ai_answer)