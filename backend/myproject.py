from flask import Flask, jsonify, g, request, session, redirect
import pymysql
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '818188')  # 환경 변수로 관리하는 것을 권장합니다.

# 데이터베이스 설정 정보
db_config = {
    'host': os.getenv('DB_HOST', '192.168.0.7'),
    'user': os.getenv('DB_USER', 'farmi_db'),
    'password': os.getenv('DB_PASSWORD', '818188'),
    'db': os.getenv('DB_NAME', 'farmi_db'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """데이터베이스 연결을 생성합니다."""
    if 'db' not in g:
        g.db = pymysql.connect(**db_config)
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    """요청 종료 시 데이터베이스 연결을 닫습니다."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 로그인 처리
@app.route('/api/logincheck', methods=['POST'])
def login_check():
    data = request.get_json()
    uid = data.get('uid')
    password = data.get('password')
    
    # 데이터베이스 연결 및 쿼리 실행
    connection = get_db_connection()

    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (uid,))
        user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # 세션에 로그인 정보 저장
        session['logged_in'] = True
        session['uid'] = user['id']
        session['rapa_ip'] = user['ip']
        session['port'] = user['port']

        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."}), 401

# 회원가입 처리
@app.route('/api/register', methods=['POST'])
def signup():
    data = request.get_json()
    uid = data.get('uid')
    upw = data.get('password')
    rapa_ip = data.get('rapa_ip')
    port = data.get('port')
    
    # 비밀번호 해싱
    hashed_password = bcrypt.hashpw(upw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 데이터베이스 연결 및 쿼리 실행
    connection = get_db_connection()
    with connection.cursor() as cursor:
        # 사용자 중복 체크
        check_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(check_query, (uid,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "이미 존재하는 사용자 ID입니다."}), 409

        # 사용자 등록
        insert_query = "INSERT INTO users (id, password, ip, port) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (uid, hashed_password, rapa_ip, port))
        connection.commit()

    return jsonify({"success": True, "message": "회원가입이 완료되었습니다."}), 201

# 아이디 중복 확인
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

# 세션 상태 확인 API
@app.route('/api/session-check', methods=['GET'])
def session_check():
    """로그인 세션 상태를 확인합니다."""
    if 'logged_in' in session and session['logged_in']:
        return jsonify({
            "loggedIn": True,
            "uid": session.get('uid'),
            "rapa_ip": session.get('rapa_ip'),
            "port": session.get('port')
        })
    else:
        return jsonify({"loggedIn": False})

# 로그아웃 처리
@app.route('/api/logout', methods=['POST'])
def logout():
    """세션에서 사용자 정보를 제거하여 로그아웃합니다."""
    session.pop('logged_in', None)
    session.pop('uid', None)
    session.pop('rapa_ip', None)
    session.pop('port', None)
    return jsonify({"success": True, "message": "Logged out successfully."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000)
