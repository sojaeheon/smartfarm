from flask import Flask, jsonify, g, request, session
from flask_cors import CORS
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

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

@app.route('/api/logincheck', methods=['POST'])
def login_check():
    data = request.get_json()
    uid = data.get('username')
    password = data.get('password')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (uid,))
        user = cursor.fetchone()

    if user:
        session['logged_in'] = True
        session['username'] = user['id']
        session['rapa_ip'] = user['ip']
        session['port'] = user['port']

        return jsonify({"success": True, "session": dict(session)})
    else:
        print(user)
        return jsonify({"success": False, "message": "Invalid username or password."})

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
        hashed_password = generate_password_hash(upw)
        cursor.execute(insert_query, (uid, hashed_password, rapa_ip, port))
        connection.commit()

    return jsonify({"success": True, "message": "회원가입이 완료되었습니다."})

@app.route('/api/session-check', methods=['GET'])
def session_check():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({"loggedIn": True, "username": session['username']})
    else:
        return jsonify({"loggedIn": False})

@app.route('/api/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return jsonify({"success": True, "message": "Logged out successfully."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)
