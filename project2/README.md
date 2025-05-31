# 🧾 PDF 논문 요약 및 번역기 (LangChain + YAML Prompt Engineering)

이 프로젝트는 논문 PDF 파일을 입력하면 다음 작업을 자동으로 수행하는 LangChain 기반의 코드입니다. 

PromptTemplate를 공부하면서 간단하게 만들어 보았습니다:

- 논문 주요 섹션(요약문, 방법론, 결과) 추출  
- 해당 내용을 기반으로 핵심 요약 생성  
- 저자의 주요 기여(contributions) 추출  
- 요약 결과를 자연스러운 한국어로 번역  

## 흐름

```

📄 PDF 파일
↓
🧠 Section 추출 (정규식 기반)
↓
🧾 PromptTemplate (YAML 정의)
↓
🤖 LLM 호출 (ChatGPT-4o)
↓
📝 요약, 기여도 추출, 한국어 번역 결과 출력

````

---

## 🛠 설치 방법

```bash
# 1. 프로젝트 클론
git clone https://github.com/your-username/pdf-paper-summarizer.git
cd project2
````

---

## 📂 폴더 구조

```
.
├── prompts/
│   └── paper_tasks.yaml        # 각 작업별 PromptTemplate 정의 (요약, 기여도 추출, 번역)
├── summarize_paper.py          # 메인 실행 스크립트
└── README.md
```

---

## 사용 방법

```
python summarize_paper.py ./example_paper.pdf
```

지금 디렉토리에 있는 논문은 제 논문입니다.. ㅎㅎ


실행하면 네 가지 결과가 출력됩니다:

* 🔎🔎🔎 [Paper Summary] 🔎🔎🔎
* 🔎 [Summary]
* 🧠 [Contributions]
* 🇰🇷 [Korean Translation]

---

## 주요 기술 스택

* **LangChain Core & LCEL** – 프롬프트 체인 구성
* **OpenAI GPT-4o** – 자연어 처리
* **YAML Prompt 구성** – 모듈형 프롬프트 설계
* **PyPDF2** – PDF 텍스트 추출
* **정규 표현식 (regex)** – 논문 구조 분석

---

## 📌 참고 사항

* `prompts/paper_tasks.yaml`에서 프롬프트 내용을 자유롭게 수정하여 다양한 형태의 Prompt Engineering을 실험할 수 있습니다.
* 논문 PDF 구조가 불완전하거나 스캔본일 경우 텍스트 추출이 어려울 수 있습니다.
