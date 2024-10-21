from flask import Flask, jsonify, g, request, session, redirect
import pymysql
from flask_cors import CORS
from robo import sb_decision
import os
import tempfile
from llm import *

app = Flask(__name__)
app.secret_key = '818188'
CORS(app)

# 모델 로드
def load_models():
    global embeddings_model, retriever, chain
    texts = load_and_split_pdf("농업기술길잡이40_딸기.pdf")
    embeddings_model = create_embeddings_model()
    retriever = setup_document_search(texts, embeddings_model)
    prompt = create_prompt_template()
    chain = create_rag_chain(retriever, prompt)

def init():
    load_models()
    
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

# 로그인 처리
@app.route('/api/logincheck', methods=['POST'])
def login_check():
    data = request.get_json()
    uid = data.get('uid')
    password = data.get('password')
    # 데이터베이스 연결 및 쿼리 실행
    connection = get_db_connection()

    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s AND password = %s"
        cursor.execute(query, (uid, password))
        user = cursor.fetchone()

    connection.close()
    print(user)
    if user:
        # 세션에 로그인 정보 저장
        session['logged_in'] = True
        session['uid'] = user['id']
        session['rapa_ip'] = user['ip']
        session['port']=user['port']

        session_data = dict(session)
        print(session_data)

        return jsonify({"success": True, "session" : session_data})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

# 회원가입
@app.route('/api/register', methods=['POST'])
def signup():
    data = request.get_json()
    uid = data.get('uid')
    upw = data.get('password')
    rapa_ip = data.get('rapa_ip')
    port = data.get('port')

    # 데이터베이스 연결 및 쿼리 실행
    connection = get_db_connection()
    with connection.cursor() as cursor:
         # 사용자 중복 체크
        check_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(check_query, (uid))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "이미 존재하는 사용자 ID입니다."})

        # 사용자 등록
        insert_query = "INSERT INTO users (id, password, ip, port) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (uid, upw, rapa_ip, port))
        connection.commit()

    connection.close()
    
    return jsonify({"success": True, "message": "회원가입이 완료되었습니다."})

#아이디 중복확인
@app.route('/api/check-uid', methods=['POST'])
def check_uid():
    data = request.get_json()
    uid = data.get('uid')

    connection = get_db_connection()

    with connection.cursor() as cursor:
         # 사용자 중복 체크
        check_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(check_query, (uid))
        if cursor.fetchone():
            return jsonify({"available": False})
        else:
            return jsonify({"available": True})

# 세션 상태 확인 API
@app.route('/api/session-check', methods=['GET'])
def session_check():
    """로그인 세션 상태를 확인합니다."""
    if 'logged_in' in session and session['logged_in']:
        return jsonify({"loggedIn": True, "username": session['username']})
    else:
        return jsonify({"loggedIn": False})

# 로그아웃 처리
@app.route('/api/logout', methods=['GET'])
def logout():
    """세션에서 사용자 이름을 제거하여 로그아웃합니다."""
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route('/api/get_answer', methods=['GET', 'POST'])
def get_answer():
    if request.method == 'GET':
        return jsonify({"message": "이 엔드포인트는 POST 메소드를 사용하여 질문을 보내야 합니다."}), 200

    if request.method == 'POST':
        data = request.get_json()
        question = data.get('question')
        print(question)
        if not question:
            return jsonify({"error": "질문이 제공되지 않았습니다."}), 400

        try:
            answer = get_answer_from_chain(chain, question)
            print(answer,flush=True)
                        
            return jsonify({"answer": answer}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        
@app.route('/api/disease', methods=['GET', 'POST'])
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
            disease_name,__ = sb_decision(tmp_file_path)
            question = f'딸기 {disease_name} 치료방법을 알려주세요.'
            solution = get_answer_from_chain(chain, question)

            print(question)
            print(solution)
            data = {
                "disease": disease_name,
                "solution": solution
            }
            print(data)
            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": f"질병 진단 처리 중 오류 발생: {str(e)}"}), 500
        finally:
            os.remove(tmp_file_path)
            
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)


    
