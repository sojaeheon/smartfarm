from flask import Flask, jsonify, g, request, session, redirect
import pymysql

app = Flask(__name__)
app.secret_key = '818188'

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
    username = data.get('username')
    password = data.get('password')

    # 데이터베이스 연결 및 쿼리 실행
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s AND passwd = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

    connection.close()

    if user:
        # 세션에 로그인 정보 저장
        session['logged_in'] = True
        session['username'] = username
        return jsonify({"success": True, "message": "Login successful.", "username" : session['username']})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)


    