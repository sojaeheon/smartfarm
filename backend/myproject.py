from flask import Flask, jsonify, g, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask_cors import CORS
from datetime import datetime, timezone
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

# 센서 데이터
def get_sensor_data():
    connection = get_db_connection()  # g 객체에서 DB 연결 가져오기
    try:
        with connection.cursor() as cursor:
            sql = "SELECT device_name, temperature, humidity, light, waterlevel, co2, date FROM sensor"  # 테이블 이름에 맞게 수정
            cursor.execute(sql)
            result = cursor.fetchall()
            return result  # 데이터 반환
    except Exception as e:
        print(f"Error occurred: {e}")  # 에러 메시지 출력 (디버깅 용도)
        return []  # 오류 발생 시 빈 리스트 반환

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
    device_name= data.get('device_name')
    print(uid+" "+password)
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, uid)
        user = cursor.fetchone()

    if user:
        session['logged_in'] = True
        session['uid'] = user['id']
        session['device_name'] = user['device_name']
        return jsonify({"success": True, "session": dict(session)})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

# 회원가입 처리
@app.route('/api/register', methods=['POST'])
def signup():
    data = request.get_json()
    uid = data.get('username')
    upw = data.get('password')
    device_name = data.get('device_name')
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(check_query, (uid,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "이미 존재하는 사용자 ID입니다."})

        insert_query = "INSERT INTO users (id, password, device_name) VALUES (%s, %s, %s)"
        hashed_password = upw
        cursor.execute(insert_query, (uid, hashed_password, device_name))
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
    data = request.get_json()
    device_name = data.get('device_name')
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    light = data.get('light')
    waterlevel = data.get('waterlevel')
    co2 = data.get('co2')
    date = data.get('date')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        insert_query = """
            INSERT INTO sensor (device_name, temperature, humidity, light, waterlevel, co2, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            device_name, temperature, humidity, light, waterlevel, co2,
            datetime.fromisoformat(date) if date else datetime.now(timezone.utc)
        ))
        connection.commit()

    return jsonify({"message": "Sensor data added successfully"}), 201

# 센서데이터
@app.route('/api/sensor_graph', methods=['GET'])
def sensor_grap():
    data = get_sensor_data()  # 데이터베이스에서 데이터 가져오기
    print(data)
    return jsonify(data)  # JSON 형식으로 반환

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)


    
