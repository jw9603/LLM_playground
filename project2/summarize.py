from dotenv import load_dotenv
import yaml
import re
from PyPDF2 import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# === PDF 파싱 ===
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text
    except Exception as e:
        raise RuntimeError(f"PDF 텍스트 추출 실패: {e}")

# === 논문 섹션 분리 ===
def split_sections(text: str) -> dict:
    abstract = re.search(r"(?i)abstract\s*(.*?)\n(?:introduction|1\.|I\.)", text, re.DOTALL)
    methods = re.search(r"(?i)(?:method|methods|approach|preliminary)\s*(.*?)\n(?:results|experiments)", text, re.DOTALL)
    results = re.search(r"(?i)(?:experiments|experiment|result|results)\s*(.*?)\n(?:discussion|conclusion|analysis|summary)", text, re.DOTALL)

    return {
        "abstract": abstract.group(1).strip() if abstract else "",
        "methods": methods.group(1).strip() if methods else "",
        "results": results.group(1).strip() if results else "",
        "content": text.strip(),
    }

# === Prompt Chain 생성기 ===
class PromptChain:
    def __init__(self, config: dict):
        self.prompt = PromptTemplate(
            input_variables=config["input_variables"],
            template=config["template"]
        )
        self.chain = self.prompt | ChatOpenAI(model="gpt-4o", temperature=0) | StrOutputParser()

    def invoke(self, inputs: dict) -> str:
        return self.chain.invoke(inputs)

# === 전체 논문 처리 ===
def process_paper(pdf_path: str, yaml_path: str = './prompts/paper_tasks.yaml') -> dict:
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    text = extract_text_from_pdf(pdf_path)
    sections = split_sections(text)
    
    summarize_paper_chain = PromptChain(yaml_data['summarize_paper'])
    summarize_chain = PromptChain(yaml_data["summarize_sections"])
    contribution_chain = PromptChain(yaml_data["extract_contributions"])
    translate_chain = PromptChain(yaml_data["translate_summary"])

    summary_paper = summarize_paper_chain.invoke({"content": sections["content"]})

    summary = summarize_chain.invoke({
        "abstract": sections["abstract"],
        "methods": sections["methods"],
        "results": sections["results"],
    })

    contributions = contribution_chain.invoke({
        "content": sections["content"]
    })

    translation = translate_chain.invoke({
        "summary": summary
    })

    return {
        'paper_summary': summary_paper,
        "summary": summary,
        "contributions": contributions,
        "korean_translation": translation,
    }

# === 실행 예시 ===
if __name__ == '__main__':

    load_dotenv()
    from langchain_teddynote import logging

    # 프로젝트 이름을 입력합니다.
    logging.langsmith("Paper Summary Project")

    import sys
    if len(sys.argv) < 2:
        print("❗ PDF 파일 경로를 인자로 제공하세요.")
        sys.exit(1)

    pdf_path = sys.argv[1]
    result = process_paper(pdf_path)
    print("\n🔎🔎🔎 [Paper Summary] 🔎🔎🔎\n", result["paper_summary"])
    print("\n🔎 [Summary]\n", result["summary"])
    print("\n🧠 [Contributions]\n", result["contributions"])
    print("\n🇰🇷 [Korean Translation]\n", result["korean_translation"])
