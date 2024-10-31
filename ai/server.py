from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS
from robo import *
import os
import tempfile
from llm import *
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = '818188'
CORS(app)

# 전역 변수 설정
embeddings_model = None
retriever = None
chain = None

# 모델 로드
def load_models():
    global embeddings_model, retriever, chain
    texts = load_and_split_pdf("manual/농업기술길잡이40_딸기.PDF")
    embeddings_model = create_embeddings_model()
    retriever = setup_document_search(texts, embeddings_model)
    prompt = create_prompt_template()
    chain = create_rag_chain(retriever, prompt)

def init():
    load_models()
    
@app.route('/api/ai/get_answer', methods=['GET', 'POST'])
def get_answer():
    if request.method == 'GET':
        return jsonify({"message": "이 엔드포인트는 POST 메소드를 사용하여 질문을 보내야 합니다."}), 200

    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question')
        print(question)
        print(chain)
        if not question:
            return jsonify({"error": "질문이 제공되지 않았습니다."}), 400

        try:
            answer = get_answer_from_chain(chain, question)
            print(answer,flush=True)
                        
            return jsonify({"answer": answer}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        
@app.route('/api/ai/disease', methods=['GET', 'POST'])
def disease():
    if request.method == 'GET':
        return jsonify({"message": "이 엔드포인트는 POST 메소드를 사용하여 이미지를 보내야 합니다."}), 200

    if request.method == 'POST':
        if 'photo' not in request.files:
            return jsonify({"error": "이미지가 제공되지 않았습니다."}), 400
        
        image = request.files['photo']
        try:
            # 이미지 파일을 임시로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(image.read())
                tmp_file_path = tmp_file.name

            # 모델 예측 수행
            disease_name,disease_data = sb_decision(tmp_file_path)
            question = f'딸기 {disease_name} 치료방법을 알려주세요.'
            solution = get_answer_from_chain(chain, question)

            # 바운딩 박스
            boundingImage = draw_bounding_box(image,disease_data,disease_name)
            
            # 이미지를 BytesIO 객체에 저장
            buffered = BytesIO()
            boundingImage.save(buffered, format="PNG")  # PNG 형식으로 저장
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Base64 인코딩
            
            print(question)
            print(solution)
            data = {
                "disease": disease_name,
                "solution": solution,
                "boundingImage":img_str
            }
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": f"질병 진단 처리 중 오류 발생: {str(e)}"}), 500
        finally:
            os.remove(tmp_file_path)
            
if __name__ == "__main__":
    init()
    app.run(host='0.0.0.0', port=7777, debug=True)