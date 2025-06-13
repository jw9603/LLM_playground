# 🥔 LangChain 기반 PDF Q&A & 프롬프트 챗봇

LLM과 LangChain을 활용하여 다음 두 가지 기능을 제공하는 Streamlit 기반 미니 프로젝트입니다:

1. **PDF 기반 질의응답 (RAG 기반)**
2. **프롬프트 기반 자유 챗봇 (YAML 프롬프트 적용)**

---

## 📁 프로젝트 구조

```
.
├── main.py                # 일반 챗봇 (프롬프트 선택)
├── pages/
│   └── 01_PDF.py          # PDF 기반 Q&A 기능
├── prompts/               # YAML 기반 프롬프트 템플릿
│   ├── pdf-rag.yaml
│   ├── summary.yaml
│   ├── sns.yaml
│   └── ...
├── .cache/                # 업로드한 PDF 및 FAISS 캐시 저장소
├── requirements.txt
└── README.md
```

---

## 🚀 실행 방법


### 1. 환경 변수 설정

`.env` 파일을 루트에 생성하고, 아래와 같이 OpenAI API 키를 입력하세요:

```env
OPENAI_API_KEY=sk-xxxxxxx
```

### 2. 실행

```bash
streamlit run main.py
```

> 📄 PDF 기반 질의응답 기능은 사이드바에서 `01_PDF.py` 페이지로 접근할 수 있습니다.

---

## 🧩 기능 설명

### 📄 PDF 기반 Q&A (pages/01_PDF.py)

업로드한 PDF 문서를 FAISS 벡터스토어로 변환하여, 문서 기반 질의응답 기능을 제공합니다.

- `PyMuPDFLoader`로 PDF 파싱
- `RecursiveCharacterTextSplitter`로 텍스트 분할
- `OpenAIEmbeddings` + `FAISS`로 임베딩 및 검색
- `LangChain`의 Retriever + Prompt + LLM 체인 구성
- 프롬프트: [`prompts/pdf-rag.yaml`](./prompts/pdf-rag.yaml)

질문 예시:
> “이 문서의 핵심 주장은?”  
> “3페이지에서 언급한 기술 개요는?”

### 프롬프트 기반 챗봇 (main.py)

사이드바에서 다양한 YAML 프롬프트를 선택하고, 자유롭게 질문을 던질 수 있는 챗봇입니다.

- 다양한 역할 프롬프트 적용 (예: 요약기, 마케터, 콘텐츠 생성기 등)
- `task` 입력을 통해 프롬프트 세부 조정 가능
- LangChain의 `load_prompt()`로 YAML 프롬프트 자동 로딩

---

## 🛠️ 사용 기술

- **LangChain** (LCEL 기반 체인 구성)
- **OpenAI GPT-4o, GPT-4-turbo**
- **FAISS** (벡터 DB)
- **Streamlit** (UI)
- **dotenv** (환경 변수 관리)
- **PyMuPDF** (PDF 파서)

---

## 확장 아이디어

- ✅ CoT 기반 요약 
- ✅ 복수 PDF 검색 기능 추가
- ✅ Agent + Tool 조합으로 고도화
- ✅ 사용자별 프롬프트 저장 기능
