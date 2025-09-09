import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_teddynote.prompts import load_prompt
from langchain_openai import ChatOpenAI
from langchain_teddynote.models import MultiModal
from langchain_teddynote.messages import stream_response
import os
from retriever import create_retriever
from langchain_teddynote import logging
from dotenv import load_dotenv


load_dotenv()

logging.langsmith('[Project] 이미지 인식')

# Cache Directory 생성
if not os.path.exists('.cache'):
    os.mkdir('.cache')

if not os.path.exists('.cache/files'):
    os.mkdir('.cache/files')

if not os.path.exists(".cache/embeddings"):
    os.mkdir('.cache/embeddings')

st.title('Talking Potatio의 이미지 인식 기반 기반 챗봇🍟')

# 처음 1번만을 실행하기 위한 코드
if 'messages' not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state['messages'] = []
    
# 탭을 생성
main_tab1, main_tab2 = st.tabs(['이미지', '대화 내용'])


# sidebar 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_button = st.button('대화 초기화')
    # 이미지 업로드
    uploaded_file = st.file_uploader("이미지 업로드", type=['jpg', 'jpeg', 'png'])

    # 모델 선택 메뉴
    selected_model = st.selectbox("LLM 선택", ['gpt-4o', 'gpt-4o-mini'], index=0)
    
    # 시스템 프롬프트 추가
    system_prompt = st.text_area("시스템 프롬프트", 
                                 "당신은 표(재무제표) 를 해석하는 금융 AI 어시스턴트 입니다. 당신의 임무는 주어진 테이블 형식의 재무제표를 바탕으로 흥미로운 사실을 정리하여 친절하게 답변하는 것입니다.",
                                 height=200)
    

# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state['messages']:
        main_tab2.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state['messages'].append(ChatMessage(role=role, content=message))

# 이미지를 캐시에 저장(시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner="업로드한 이미지를 처리 중...!")
def process_file(file):
    # 업로드한 파일을 캐시 디렉토리에 저장
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    return file_path

def generate_answer(img_file_path, system_prompt, user_prompt, model_name='gpt-4o'):
    llm = ChatOpenAI(
        temperature=0,
        model=model_name
    )
    
    # 멀티모달 객체 생성
    multimodal_llm_with_prompt = MultiModal(
    llm, system_prompt=system_prompt, user_prompt=user_prompt
    )
    
    # 이미지 파일로 부터 질의(스트림 방식)
    answer = multimodal_llm_with_prompt.stream(img_file_path)
    
    return answer


# 초기화 버튼이 눌리면...
if clear_button:
    st.session_state['messages'] = []

print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보시오.")

# 경고 메시지를 띄우기 위한 빈 영역
warning_messae = main_tab2.empty()

# 이미지가 업로드가 된다면...
if uploaded_file:
    image_file_path = process_file(uploaded_file)
    main_tab1.image(image_file_path)

# 만약 사용자 입력이 들어오면..
if user_input:
    # 파일이 업로드 되었는지 확인
    if uploaded_file:
        # 이미지 파일을 처리
        image_file_path = process_file(uploaded_file)
        # 이미지 파일을 업로드 했다는 메시지 출력
        warning_messae.success("이미지 파일을 업로드 했습니다.")
        
        # 답변 요청
        response = generate_answer(image_file_path, system_prompt, user_input, selected_model)
        
        # 사용자의 입력
        main_tab2.chat_message("user").write(user_input)

    
        with main_tab2.chat_message('assistant'):
            # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
            container = st.empty()
            ai_answer = ''
            for token in response:
                ai_answer += token.content
                container.markdown(ai_answer)

        # 대화 기록을 저장한다.
        add_message("user", user_input)
        add_message('assistant', ai_answer)
    
    else:
        # 이미질,ㄹ 업로드 하라는 경고 메시지 출력
        warning_messae.warning('이미지를 업로드 해주세요.')
