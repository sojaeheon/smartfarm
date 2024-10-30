from flask import Flask, jsonify, g, request, session, redirect
import pymysql
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '818188'

# CORS 설정: 쿠키 전송 활성화
CORS(app, supports_credentials=True)

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

#세션확인
@app.route('/api/check-session', methods=['POST'])
def check_session():
    try:
        if 'uid' in session:
            return jsonify({"logged_in": True})
        else:
            return jsonify({"logged_in": False})
    except Exception as e:
        app.logger.error(f"Error in /api/check-session: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# 로그아웃 처리
@app.route('/api/logout', methods=['GET'])
def logout():
    """세션에서 사용자 이름을 제거하여 로그아웃합니다."""
    session.pop('logged_in', None)
    session.pop('uid', None)
    return jsonify({"success": True, "message": "Logged out successfully."})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)


    
