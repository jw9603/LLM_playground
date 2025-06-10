# 🥔 Simple Chatbot — LangChain x Streamlit Chat App


이 프로젝트는 **Streamlit**과 **LangChain**을 활용해 만든 간단한 **Chat GPT 인터페이스**입니다.  
사용자는 **프롬프트 유형**을 선택하고, **대화형 인터페이스**를 통해 GPT 모델과 실시간으로 소통할 수 있습니다.

> 📌 `chain-of-density` 기반 요약 프롬프트, SNS 스타일 포맷팅, 일반 질의응답 등을 선택할 수 있어  
> 다양한 텍스트 생성 경험을 체험할 수 있습니다!

---

## 🚀 주요 기능

- **대화 기록 저장** 및 출력
- **프롬프트 선택**: 기본 Q&A / SNS 게시글 스타일 / Chain-of-Density 기반 요약
- **스트리밍 응답 출력**
- **LangChain Expression Language (LCEL)** 기반 체인 구성
---

## 🧱 기술 스택

- Python
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI API](https://platform.openai.com/)
- [LangChain Hub](https://smith.langchain.com/hub)
- [LangSmith](https://www.langchain.com/langsmith)

---

## 📂 프로젝트 구조
```plain
simple_chatbot/
  ├── main.py                  # 메인 Streamlit 앱
  ├── prompts/
  │   └── sns.yaml            # SNS 프롬프트 정의 파일
  ├── .env                    # OpenAI API 키 저장  --> 저는 미공개합니다. 개인마다 설정핫히면 됩니다.
  └── README.md
```
---

## 🧪 프롬프트 타입 설명
| 유형      | 설명                                                       |
| ------- | -------------------------------------------------------- |
| 기본모드    | 간단한 Q\&A 시스템 (System 프롬프트 기반)                            |
| SNS 게시글 | `prompts/sns.yaml` 기반 포맷된 SNS 스타일 출력                     |
| 요약      | LangChain Hub의 `chain-of-density` 요약 프롬프트 사용 (점진적 요약 기법) |


---

## References
Chain-of-Density paper: [From Sparse to Dense (2023)](https://arxiv.org/abs/2309.04269)

LangChain Hub 사용법: https://docs.langchain.com/docs/components/hub/

LangChain Expression Language (LCEL): https://docs.langchain.com/docs/expression-language/



