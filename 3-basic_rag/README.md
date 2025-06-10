# 📄 PDF 기반 RAG Q&A 시스템

이 프로젝트는 업로드된 PDF 문서를 기반으로 사용자의 질문에 답변하는 **RAG(Retrieval-Augmented Generation)** 시스템입니다. OpenAI의 GPT-4o 모델과 LangChain, FAISS 벡터 데이터베이스를 사용해 **문서 기반 질의응답**과 **일반 지식 기반 답변**을 모두 지원합니다.

이 프로젝트는 RAG를 처음 경험해보는 프로젝트로써, RAG의 뼈대 코드라고 생각하면 좋을것 같습니다!

---

## 주요 기능

- PDF 문서 내에서 관련 정보를 찾아 질문에 답변
- 문서에 없는 일반 상식 질문에 대해서도 AI가 직접 답변
- CLI 및 Streamlit 기반 UI 제공
- LangChain 기반 문서 임베딩 및 벡터 검색 기능 포함

---

## 📁 프로젝트 구조
```
├── main.py # CLI 버전 실행 스크립트
├── main1.py # Streamlit UI 앱
├── data/
│ └── 1.pdf # 예시 PDF 파일 (사용자가 업로드, )
├── .env # OpenAI API 키 환경 변수 -> 미공개
└── README.md # 프로젝트 설명 파일
```
---

## CLI 사용법
```bash
python main.py
```

- 콘솔에 나오는 안내에 따라 질문을 입력하면 PDF 기반 또는 일반 지식 기반으로 답변을 제공합니다.




---

## Streamlit 앱실행
```bash
streamlit run main1.py
```
- 웹 브라우저에 열리는 UI에서 PDF 업로드 후 질문을 입력하면 실시간으로 답변이 표시됩니다.




