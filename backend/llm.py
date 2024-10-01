from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

# 언어 모델 설정
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-pro-001',
    google_api_key='AIzaSyCvBysyoy-zvcU7QhGD3k4Wha-rHJ29PvI',
    temperature=0
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
    model_kwargs = {'device': 'cpu'}
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
    docsearch = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings_model,  # 모델 객체 자체를 넘겨줌
        persist_directory="chroma_db" # 폴더 생성
    )
    
    # MMR 검색을 사용하여 관련된 3개의 문서를 반환하도록 검색 설정, 10개의 후보 중 선택
    # MRR 방식은 검색 결과가 중복되지 않도록 다양성을 확보하면서 관련성이 높은 문서를 반환
    retriever = docsearch.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 3, 'fetch_k': 10}
    )
    return retriever


# 프롬프트 템플릿 설정
def create_prompt_template():
    """프롬프트 템플릿을 생성하는 함수"""
    RAG_PROMPT_TEMPLATE = """Answer the question based only on the following context:
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
def get_answer_from_chain(chain, user_input):
    """질문에 대한 답변을 얻는 함수"""
    answer = chain.stream(user_input)
    previous_chunk = ""
    final_answer = ""  # 최종 답변을 저장할 변수

    for chunk in answer:
        new_text = chunk.replace(previous_chunk, "")
        final_answer += new_text  # 매번 새로운 부분을 최종 답변에 추가
        previous_chunk += new_text

    return final_answer  # 최종적으로 하나의 문자열로 응답

# 실행 흐름
# def bot():
#     # PDF 파일 경로
#     pdf_path = "manual/딸기고품질다수확재배매뉴얼 설향.pdf"

#     # 문서 로드 및 분할
#     texts = load_and_split_pdf(pdf_path)

#     # 임베딩 모델 생성
#     embeddings_model = create_embeddings_model()

#     # 문서 검색 설정
#     retriever = setup_document_search(texts, embeddings_model)

#     # 프롬프트 템플릿 설정
#     prompt = create_prompt_template()

#     # 체인 생성
#     rag_chain = create_rag_chain(retriever, prompt)

#     # 사용자로부터 계속 입력받기 위한 루프
#     while True:
#         user_input = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")

#         if user_input.lower() == 'exit':
#             print("프로그램을 종료합니다.")
#             break

#         get_answer_from_chain(rag_chain, user_input)

# if __name__ == "__main__":
#     bot()