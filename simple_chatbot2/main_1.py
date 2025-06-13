import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from langchain import hub

from dotenv import load_dotenv

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

    selected_prompt = st.selectbox(
    "프롬프트를 선택해 주세요.",
    ("기본모드", "SNS 게시글", "요약"), index=0
)
    

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        st.chat_message(chat_message.role).write(chat_message.content)

# 새로운 메시지를 추가
def add_messages(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

# 체인 생성
def create_chain(prompt_type):
    # prompt | llm | parser
    # 프롬프트 (기본 모드)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", '당신은 친절한 AI 어시스턴트입니다. 다음의 질문에 간결하게 답변해 주세요.'),
            ("user", "#Question:\n{question}"),
        ]
    )
    if prompt_type == 'SNS 게시글':
        prompt = load_prompt("prompts/sns.yaml", encoding="utf-8")
    elif prompt_type == '요약':
        prompt = hub.pull('jiwon/chain-of-density-map-korean')

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
    chain = create_chain(selected_prompt)

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
