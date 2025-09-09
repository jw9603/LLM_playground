# 🍟 Multi-turn Chatbot with LangChain & Streamlit

이 레포지토리는 LangChain Expression Language (LCEL) 과 메모리 기능을 활용해 만든 멀티턴 대화 챗봇 예제입니다. [기존 프로젝트](https://github.com/jw9603/LangChain_playground/tree/main/potato_pj4)에 멀티턴만 추가한 프로젝트입니다!

Streamlit을 이용해 UI를 구성했고, OpenAI LLM(gpt-4o, gpt-4o-mini)을 기반으로
대화 내용을 기억하며 응답하는 챗봇을 구현했습니다.

## 주요 기능

멀티턴 대화 지원
- RunnableWithMessageHistory + ChatMessageHistory 로 대화 맥락을 유지

세션별 대화 분리
- session_id를 지정해 여러 독립 대화를 동시에 관리 가능

실시간 스트리밍 응답
- OpenAI API 스트리밍을 Streamlit UI에 반영

간단한 초기화 기능
- 버튼 클릭으로 현재 대화 UI 기록 초기화 가능

확장 용이
- 추후 RAG, 벡터 스토어, 요약 메모리 등으로 쉽게 확장 가능
