
# Email 요약기 (Streamlit + LangChain + Pydantic + SerpAPI)

이 프로젝트는 이메일 본문을 입력하면 **PydanticOutputParser**로 핵심 정보를 구조화하여 추출하고, **SerpAPI**로 발신자 관련 \*\*추가 정보(웹 검색 결과)\*\*를 자동 수집한 뒤, **리포트 형태**로 보여주는 **대화형 Streamlit 앱**입니다.

> 키워드: Streamlit, LangChain, Pydantic, OpenAI, SerpAPI, OutputParser

---

## 주요 기능

* 📩 **이메일 엔티티 추출**: 발신자/수신자/제목/요약/일정 등
* 🧱 **구조화 파싱**: LangChain의 **PydanticOutputParser**로 안전한 데이터 모델링
* 🌐 **발신자 정보 보강**: **SerpAPI** 구글 검색 결과를 자동 수집
* 🧾 **요약 리포트 생성**: 마크다운 형식으로 정갈하게 출력
* 💬 **대화형 UI**: Streamlit `st.chat_message` 기반 채팅 인터페이스

---

## 아키텍처 한눈에 보기

```
사용자 입력(이메일 본문)
        │
        ▼
[PromptTemplate] ──▶ [OpenAI Chat Model] ──▶ [PydanticOutputParser(EmailSummary)]
        │                                                │
        │                                                └─ 추출된 엔티티
        │
        ├─▶ [SerpAPIWrapper] ──(발신자 이름/이메일로 검색)──▶ 추가 정보(JSON/문자열)
        │
        ▼
[리포트 Prompt] ─▶ [OpenAI Chat Model] ─▶ 스트리밍 출력(마크다운)
```

---

## 디렉터리 구조 (예시)

```
.
├── app.py                    # Streamlit 앱(공유하신 코드)
├── prompts/
│   └── email.yaml            # 리포트 생성 Prompt (langchain_teddynote.prompts.load_prompt)
├── .env                      # 환경변수(로컬 개발용)
├── requirements.txt
└── README.md
```

---

## 요구 사항

* **Python** 3.10+
* OpenAI API Key
* SerpAPI API Key ([https://serpapi.com](https://serpapi.com))
* 인터넷 연결

### requirements.txt (예시)

```txt
streamlit>=1.33.0
python-dotenv>=1.0.0
pydantic>=2.5.0
langchain>=0.2.0
langchain-core>=0.2.0
langchain-openai>=0.1.0
langchain-community>=0.2.0
```

> 버전은 사용 환경에 맞게 조정하세요. 서로 의존성 맞추려면 동일한 메이저/마이너를 유지하는 것을 권장합니다.

---

## 환경 변수 설정

프로젝트 루트에 **.env** 파일을 만들고 아래 내용을 채워주세요.

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
SERPAPI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

> 코드 상단에서 `dotenv.load_dotenv()`를 호출하므로 `.env`가 자동 로드됩니다.
> 또한 예제 코드에 `os.environ["SERPAPI_API_KEY"] = "YOUR_API_KEY_HERE"`가 있으니 **.env 값을 우선**으로 쓰려면 해당 하드코딩 라인을 삭제하거나 주석 처리하는 것을 권장합니다.

---

## 실행 방법

1. 의존성 설치

```bash
pip install -r requirements.txt
```

2. 환경 변수 설정

```bash
cp .env.example .env   # 없다면 직접 .env 생성
# OPENAI_API_KEY, SERPAPI_API_KEY 입력
```

3. 앱 실행

```bash
streamlit run app.py
```

4. 브라우저에서 안내된 로컬 주소로 접속
   (예: [http://localhost:8501](http://localhost:8501))

---

## 핵심 코드 포인트

### 1) PydanticOutputParser로 안전한 스키마 보장

```python
class EmailSummary(BaseModel):
    sender_name: str
    sender_email: str
    recipient_name: str
    recipient_email: str
    subject: str
    meeting_date: str
    meeting_time: str
    meeting_location: str
    summary: str
```

* LLM 출력이 **정의된 스키마**로 들어오게 만들어, 다운스트림 로직을 **안정**적으로 작성할 수 있습니다.

### 2) 체인 구성 (추출용)

```python
output_parser = PydanticOutputParser(pydantic_object=EmailSummary)
prompt = PromptTemplate.from_template("""
You are a helpful assistant...
#EMAIL CONVERSATION:
{email_conversation}
#FORMAT:
{format}
""").partial(format=output_parser.get_format_instructions())

chain = prompt | ChatOpenAI(model="gpt-4-turbo") | output_parser
```

### 3) SerpAPI로 발신자 정보 검색

```python
params = {"engine": "google", "gl": "kr", "hl": "ko", "num": "3"}
search = SerpAPIWrapper(params=params)
search_query = f"{answer.sender_name} {answer.sender_email}"
raw = search.run(search_query)
```

### 4) 리포트 생성 체인

`prompts/email.yaml`에 정의된 포맷을 불러와 **스트리밍**으로 출력:

```python
report_chain = load_prompt(... ) | ChatOpenAI(model="gpt-4-turbo") | StrOutputParser()
for token in report_chain.stream(inputs):
    ...
```

---

## 설정/모델 관련 팁

* **모델 선택**: `gpt-4-turbo`(생성), `gpt-4o`(멀티모달/한국어 강함) 등 사용 목적에 맞게 교체
* **온도(temperature)**: 요약 일관성을 높이려면 `0 ~ 0.3` 권장
* **비용**: OpenAI/SerpAPI 모두 **유료 요금**이 발생할 수 있으니 호출량 주의
* **레이트리밋**: 검색/생성 호출 빈도를 조절하고, 에러 시 재시도(backoff) 로직 고려

---

## 참고

* LangChain Docs: [https://python.langchain.com/](https://python.langchain.com/)
* Pydantic Docs: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
* SerpAPI Docs: [https://serpapi.com/](https://serpapi.com/)
* Streamlit Docs: [https://docs.streamlit.io/](https://docs.streamlit.io/)
* TeddyNote: [https://wikidocs.net/book/14314]

