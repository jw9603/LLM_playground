# 📚 Local RAG & Multi-Modal Chatbot with LangChain + Ollama

이 프로젝트는 **LangChain + Streamlit** 기반으로 구현된 **로컬 RAG(Retrieval-Augmented Generation) & 멀티모달 챗봇**입니다.  
OpenAI API와 Ollama 로컬 모델을 선택적으로 활용할 수 있으며, PDF 문서 기반 질의응답뿐 아니라 이미지 인식 기반 질의응답까지 지원합니다. 
[기존 프로젝트](https://github.com/jw9603/LLM_playground/tree/main/simple_chatbot2) 에서 발전되었다 보시면 됩니다.🚀

---

## ✨ Features

- **PDF 기반 RAG**
  - 업로드한 PDF 문서를 임베딩 & 검색
  - 선택한 LLM(OpenAI GPT 시리즈 or Ollama 로컬 모델)으로 답변 생성
  - 실시간 스트리밍 응답

- **로컬 모델 연동 (Ollama)**
  - `ChatOllama`를 활용하여 로컬 환경에서 LLM 실행
  - 기본 모델: `EEVE-KOREAN-10.8B`
  - 동일 UI에서 OpenAI 모델과 로컬 모델을 자유롭게 선택 가능

- **멀티모달 확장**
  - 이미지 업로드 후, 텍스트 + 이미지 기반 질의응답
  - 기본 시스템 프롬프트(재무제표 해석 AI) 제공, 사용자 커스터마이징 가능

---

## Prompt Difference: OpenAI vs Ollama

| 항목    | Ollama (`pdf-rag-ollama.yaml`) | OpenAI (`pdf-rag.yaml`) |
| ----- | ------------------------------ | ----------------------- |
| 출력 형식 | 자유로운 답변                        | Markdown 표, 요약, 출처 포함   |
| 지시 강도 | 최소화                            | 상세 지시 (포맷, 출처, 페이지)     |
| 목적    | 안정적 Q\&A 수행                    | 구조화된 리포트 생성             |
| 언어    | 한국어                            | 한국어                     |


