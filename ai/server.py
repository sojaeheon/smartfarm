from flask import Flask, jsonify, request,g 
import pymysql
from flask_cors import CORS
from robo import *
import os
import tempfile
from llm import *
import base64
from io import BytesIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = '818188'
CORS(app)

# 전역 변수 설정
embeddings_model = None
retriever = None
chain = None

# 데이터베이스 설정 정보
db_config = {
    'host': '192.168.0.7',
    'user': 'farmi_db',
    'password': '818188',
    'db': 'farmi_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """데이터베이스 연결을 생성합니다."""
    if 'db' not in g:
        g.db = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            db=db_config['db'],
            charset=db_config['charset'],
            cursorclass=db_config['cursorclass']
        )
    return g.db

@app.teardown_appcontext
def close_db_connection(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


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
        username = data.get('username')
        print(question)
        print(chain)
        if not question:
            return jsonify({"error": "질문이 제공되지 않았습니다."}), 400

        try:
            answer = get_answer_from_chain(chain, question,llm)
            print(answer,flush=True)

            connection = get_db_connection()
            with connection.cursor() as cursor: 
                  insert_query = "INSERT INTO chatbot (id,question,answer,date) VALUES (%s, %s, %s, %s)"
                  cursor.execute(insert_query, (username, question, answer, datetime.now()))
                  connection.commit()
                  
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

        image_file = request.files['photo']
        username = request.form['username']
        tmp_file_path = None  # finally 블록에서 삭제할 파일 경로를 저장
        
        try:
            # 이미지를 메모리에 로드하여 여러 작업에 사용
            image_data = image_file.read()  # 파일 데이터를 메모리에 저장
            original_image_base64 = base64.b64encode(image_data).decode("utf-8")

            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(image_data)
                tmp_file_path = tmp_file.name

            # 모델 예측 수행
            disease_name, disease_data = sb_decision(tmp_file_path)
            question = f'딸기 {disease_name} 치료방법을 알려주세요.'
            solution = get_answer_from_chain(chain, question, llm)

            # 바운딩 박스 그리기 위해 이미지 로드
            bounding_image = draw_bounding_box(tmp_file_path, disease_data, disease_name)

            # 바운딩 박스 이미지 저장 및 인코딩
            buffered = BytesIO()
            bounding_image.save(buffered, format="PNG")  # PNG 형식으로 저장
            bounding_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # MySQL 데이터베이스에 진단 결과 저장
            connection = get_db_connection()
            with connection.cursor() as cursor:
                insert_query = """
                    INSERT INTO disease (id, disease_name, original_image, bounding_image, answer, date)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                # 현재 날짜와 시간
                current_date = datetime.now()
                cursor.execute(insert_query, (username, disease_name, original_image_base64, bounding_image_base64, solution, current_date))
                connection.commit()

            print(question)
            print(solution)
            data = {
                "disease": disease_name,
                "solution": solution,
                "originalImage": original_image_base64,
                "boundingImage": bounding_image_base64
            }
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": f"질병 진단 처리 중 오류 발생: {str(e)}"}), 500
        finally:
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
            
if __name__ == "__main__":
    init()
    app.run(host='0.0.0.0', port=7777, debug=True)