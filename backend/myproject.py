from flask import Flask, jsonify, g, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = '818188'
CORS(app)
    
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

# 로그인 처리
@app.route('/api/logincheck', methods=['POST'])
def login_check():
    data = request.get_json()
    print(data)
    uid = data.get('username')
    password = data.get('password')
    print(uid+" "+password)
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, uid)
        user = cursor.fetchone()

    if user:
        session['logged_in'] = True
        session['uid'] = user['id']
        session['rapa_ip'] = user['ip']
        session['port'] = user['port']
        return jsonify({"success": True, "session": dict(session)})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

# 회원가입 처리
@app.route('/api/register', methods=['POST'])
def signup():
    data = request.get_json()
    uid = data.get('username')
    upw = data.get('password')
    rapa_ip = data.get('rapa_ip')
    port = data.get('port')
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(check_query, (uid,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "이미 존재하는 사용자 ID입니다."})

        insert_query = "INSERT INTO users (id, password, ip, port) VALUES (%s, %s, %s, %s)"
        hashed_password = upw
        cursor.execute(insert_query, (uid, hashed_password, rapa_ip, port))
        connection.commit()

    return jsonify({"success": True, "message": "회원가입이 완료되었습니다."})

# 아이디 중복확인
@app.route('/api/check-uid', methods=['POST'])
def check_uid():
    data = request.get_json()
    uid = data.get('uid')
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(check_query, (uid,))
        if cursor.fetchone():
            return jsonify({"available": False})
        else:
            return jsonify({"available": True})

# 세션 확인
@app.route('/api/session-check', methods=['GET'])
def session_check():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({"loggedIn": True, "username": session['uid']})
    else:
        return jsonify({"loggedIn": False})

# 로그아웃
@app.route('/api/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})

# 센서데이터
@app.route('/api/sensor_data', methods=['POST'])
def sensor_data():
    print(request.get_json())


@app.route('/api/get_answer', methods=['GET', 'POST'])
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
    init()
    app.run(host='0.0.0.0', port=7000, debug=True)


    
