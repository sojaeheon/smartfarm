from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

# 언어 모델 설정
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-pro-001',
    google_api_key='',
    temperature=0,
)

# 문서 로드 및 분할
def load_and_split_pdf(pdf_path):
    """PDF 파일을 로드하고 텍스트를 분할하는 함수"""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    # 청크 설정으로 연속적인 문맥 유지 (문서를 500자 단위로 나누고, 중복이 일부 겹치도록 설정)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(pages)

    return texts

# 임베딩 모델 생성
def create_embeddings_model():
    """임베딩 모델을 생성하는 함수"""
    model_name = "BAAI/bge-m3" # jhgan/ko-sroberta-multitask
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}

    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf


# 문서 검색 설정
def setup_document_search(texts, embeddings_model):
    """Chroma 벡터 스토어를 설정하고 문서 검색을 위한 retriever 생성"""
    persist_dir = "chroma_db"  # 인덱스가 저장된 폴더

    # 기존 인덱스가 있으면 로드하고, 없으면 새로 생성
    if os.path.exists(persist_dir):
        # 기존 인덱스 로드
        docsearch = Chroma(
            embedding_function=embeddings_model,
            persist_directory=persist_dir
        )
    else:
        # 새로운 인덱스 생성
        docsearch = Chroma.from_documents(
            documents=texts, 
            embedding=embeddings_model,
            persist_directory=persist_dir
        )
    
    # MMR 검색을 사용하여 관련된 3개의 문서를 반환하도록 검색 설정, 10개의 후보 중 선택
    # MRR 방식은 검색 결과가 중복되지 않도록 다양성을 확보하면서 관련성이 높은 문서를 반환
    retriever = docsearch.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'fetch_k': 30}
    )
    return retriever


# 프롬프트 템플릿 설정
def create_prompt_template():
    """프롬프트 템플릿을 생성하는 함수"""
    RAG_PROMPT_TEMPLATE = """문서, 본문, pdf에서 찾았다라는 말은 하지 않고 자세하고 정확하게 한국어만 사용해서 알려주세요:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
    return prompt

# 체인 생성
def create_rag_chain(retriever, prompt):
    """문서 검색과 질문 답변 체인을 설정하는 함수"""
    rag_chain = (
        {
            "context": retriever | RunnablePassthrough(),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# 사용자 입력 및 답변 출력
def get_answer_from_chain(chain, user_input, llm):
    """질문에 대한 답변을 얻는 함수"""
    answer = chain.stream(user_input)
    previous_chunk = ""
    final_answer = ""

    for chunk in answer:
        new_text = chunk.replace(previous_chunk, "")
        final_answer += new_text
        previous_chunk += new_text

    # 키워드 리스트 정의
    keywords = ["죄송","제공된 정보","찾을 수 없","제공해주신","추천해 드릴 수 없","내용과 맞지 않","주어진 정보","관련이 없","제시된 내용","대한 정보만"]

    # 키워드가 포함된 경우 LLM 기반으로 새로운 답변 생성
    if any(keyword in final_answer for keyword in keywords):
        messages = [
            {"role": "user", "content": user_input}
        ]
        
        # LLM에 올바른 형식으로 요청
        response = llm.invoke(messages)
        return response.content  # LLM 응답에서 내용 추출
    else:
        return final_answer  # 키워드가 없는 경우 기존 답변 반환
