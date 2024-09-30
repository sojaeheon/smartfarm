from flask import Flask, request, jsonify
from robo import sb_decision
import os
import tempfile
from llm import *

app = Flask(__name__)

# PDF 파일을 로드하고 임베딩 모델 생성
texts = load_and_split_pdf("manual/딸기고품질다수확재배매뉴얼 설향.pdf") 
embeddings_model = create_embeddings_model()
# 문서 검색을 위한 retriever 생성
retriever = setup_document_search(texts, embeddings_model)
# 프롬프트 템플릿 생성
prompt = create_prompt_template()
# RAG 체인 생성
chain = create_rag_chain(retriever, prompt)


# 챗봇
@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('question')
    
    if not user_input:
        return jsonify({"error": "질문이 제공되지 않았습니다."}), 400
    
    try:
        # 유저 질문에 대한 답변 생성
        answer = get_answer_from_chain(chain, user_input)
        return jsonify({"question": user_input, "answer": answer}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 질병 진단
@app.route('/disease', methods=['POST'])
def disease():
    disease_name = None
    solution = None

    if 'image' not in request.files:
        return "이미지가 제공되지 않았습니다.", 400
    
    # 요청에서 이미지를 가져옵니다.
    image = request.files['image']
    
    # 파일 저장 경로 설정
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(image.read())
        tmp_file_path = tmp_file.name
    
    try:
        # 모델 예측 수행
        disease_name = sb_decision(tmp_file_path)
        question = f'딸기 {disease_name} 치료방법을 알려주세요.'
        solution = get_answer_from_chain(chain, question)
    finally:
        # 임시 파일 삭제
        os.remove(tmp_file_path)

    data = {
        "disease": disease_name,
        "solution": solution
    }

    return jsonify(data)

@app.route("/api/", methods=['GET'])
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)


    