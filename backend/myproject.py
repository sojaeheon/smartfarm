from flask import Flask, jsonify, g, request, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from flask_cors import CORS
import base64
from datetime import datetime, timezone
import os
import requests

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
    print(uid+" "+password)
    
    connection = get_db_connection()
    with connection.cursor() as cursor:
        query = "SELECT * FROM users WHERE id = %s AND password = %s"
        cursor.execute(query, (uid, password))
        user = cursor.fetchone()
    print(user)
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
        return jsonify({"loggedIn": True, "username": session['uid'],"device_name":session['device_name']})
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
def sensor_graph():
    device_name = request.args.get('device_name')  # 쿼리 파라미터로 데이터 가져오기

    print(device_name)
    connection = get_db_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT * FROM sensor WHERE device_name = %s ORDER BY date DESC LIMIT 2880"
        cursor.execute(check_query, (device_name,))
        sensor_list = cursor.fetchall()
    

    return jsonify({"success": True, "data": sensor_list })  # JSON 형식으로 반환

@app.route('/api/disease_load', methods=['GET'])
def disease_load():
    username = request.args.get('username')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT * FROM disease WHERE id = %s ORDER BY date DESC"
        cursor.execute(check_query, (username,))
        disease_list = cursor.fetchall()

        # 데이터가 없으면 오류 메시지 반환
        if not disease_list:
            return jsonify({"success": False, "message": "No data found"})

        # Base64 데이터를 포함한 JSON 응답 준비
        disease_data = []
        for disease in disease_list:
            disease_data.append({
                "disease_id": disease["disease_id"],
                "disease_name": disease["disease_name"],
                "original_image": disease["original_image"].decode('utf-8'),  # Base64 문자열로 변환
                "bounding_image": disease["bounding_image"].decode('utf-8'),  # Base64 문자열로 변환
                "answer": disease["answer"],
                "date": disease["date"].isoformat()
            })

    return jsonify({"success": True, "disease_list": disease_data})


@app.route('/api/disease_delete', methods=['POST'])
def delete_disease():
    data = request.get_json()
    disease_id = data.get('disease_id')

    if not disease_id:
        return jsonify({"error": "disease_id가 제공되지 않았습니다."}), 400

    connection = get_db_connection()
    with connection.cursor() as cursor:
        delete_query = "DELETE FROM disease WHERE disease_id = %s"
        cursor.execute(delete_query, (disease_id,))
        connection.commit()

    return jsonify({"success": True, "message": "이미지가 성공적으로 삭제되었습니다."})

# 세션 추가 엔드포인트
@app.route('/api/session/new', methods=['POST'])
def create_session():
    data = request.get_json()
    username = data.get('username')
    question = data.get('question')  # 질문 내용 가져오기
    
    if not username or not question:
        return jsonify({'error': 'username and question are required'}), 400

    # 데이터베이스 연결 및 새로운 세션 추가
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 새 세션을 추가하는 SQL 쿼리 작성
            insert_query = """
                INSERT INTO chat_sessions (id, started_at, ended_at, question)
                VALUES (%s, %s, %s, %s)
            """
            started_at = datetime.now()
            cursor.execute(insert_query, (username, started_at, None, question))
            connection.commit()

            # 방금 추가한 세션의 ID를 가져오기
            session_id = cursor.lastrowid

        # 성공적으로 추가된 세션 정보를 반환
        return jsonify({
            "session_id": session_id,
            "username": username,
            "question": question,  # 질문 내용 반환
            "started_at": started_at.isoformat(),
            "ended_at": None
        }), 201

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Failed to create session'}), 500

@app.route('/api/chat_history', methods=['GET'])
def chat_history():
    username = request.args.get('username')

    connection = get_db_connection()
    with connection.cursor() as cursor:
        check_query = "SELECT * FROM chat_sessions WHERE id = %s ORDER BY started_at DESC"
        cursor.execute(check_query, (username,))
        history = cursor.fetchall()

        # 데이터가 없으면 오류 메시지 반환
        if not history:
            return jsonify({"success": False, "message": "No data found"})


    return jsonify({"success": True, "history": history})

@app.route('/api/session/<int:session_id>/end', methods=['POST'])
def end_session(session_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            update_query = """
                UPDATE chat_sessions SET ended_at = %s WHERE session_id = %s
            """
            ended_at = datetime.now()
            cursor.execute(update_query, (ended_at, session_id))
            connection.commit()

        return jsonify({'success': True, 'message': 'Session ended successfully.'}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Failed to end session'}), 500
    
@app.route('/api/delete_history/<int:session_id>', methods=['DELETE'])
def delete_history(session_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 메시지 삭제 쿼리
            delete_messages_query = """
                DELETE FROM messages WHERE session_id = %s
            """
            cursor.execute(delete_messages_query, (session_id,))

            # 세션 삭제 쿼리
            delete_session_query = """
                DELETE FROM chat_sessions WHERE session_id = %s
            """
            cursor.execute(delete_session_query, (session_id,))

            # 모든 변경사항을 커밋
            connection.commit()

        return jsonify({'success': True, 'message': 'Session and related messages deleted successfully.'}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': 'Failed to delete session and messages'}), 500
    
@app.route('/api/session/<int:session_id>', methods=['GET'])
def message_load(session_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 메시지를 불러오는 쿼리
            check_query = "SELECT * FROM messages WHERE session_id = %s ORDER BY timestamp ASC"
            cursor.execute(check_query, (session_id,))
            history = cursor.fetchall()

            # 데이터가 없으면 오류 메시지 반환
            if not history:
                return jsonify({"success": False, "message": "No data found"}), 404

            # 데이터가 있으면 메시지와 함께 성공 메시지 반환
            return jsonify({"success": True, "history": history}), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Failed to load messages", "details": str(e)}), 500


# 액추에이터 서버의 엔드포인트들
ACTUATOR_URLS = {
    "led": "http://202.31.150.31:9999/led",
    "dc_fan": "http://202.31.150.31:9999/dc_fan",
    "water_supply": "http://202.31.150.31:9999/water_supply",
    "water_drainage": "http://202.31.150.31:9999/water_drainage"
}

@app.route('/api/actuators', methods=['POST'])
def control_actuators():
    # 요청에서 상태와 device_name을 받음
    data = request.get_json()  # POST 데이터 받기
    status_data = data.get('status')  # 상태 정보
    device_name = data.get('device_name')  # 장치 이름

    if not status_data or not device_name:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

    # DB 연결
    connection = get_db_connection()
    cursor = connection.cursor()

    # 상태 값을 저장할 변수
    led_status = None
    dc_fan_status = None
    water_supply_status = None
    water_drainage_status = None

    # 각 장치의 상태를 업데이트
    for actuator in status_data:
        label = actuator['label']
        status = actuator['isOn']

        # 상태 값 할당
        if label == 'LED':
            led_status = status
        elif label == 'DC팬':
            dc_fan_status = status
        elif label == '워터펌프(급수)':
            water_supply_status = status
        elif label == '워터펌프(배수)':
            water_drainage_status = status

    # `device_name`에 대한 상태 업데이트 (기존 값이 있으면 UPDATE, 없으면 INSERT)
    cursor.execute("""
        INSERT INTO actuator (device_name, led, dc_fan, water_supply, water_drainage)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            led = VALUES(led),
            dc_fan = VALUES(dc_fan),
            water_supply = VALUES(water_supply),
            water_drainage = VALUES(water_drainage)
    """, (device_name, led_status, dc_fan_status, water_supply_status, water_drainage_status))

    # 각 액추에이터 서버로 상태 전달
    actuator_labels = {
        'led': led_status,
        'dc_fan': dc_fan_status,
        'water_supply': water_supply_status,
        'water_drainage': water_drainage_status
    }

    for column, status in actuator_labels.items():
        if status is not None and column.lower() in ACTUATOR_URLS:
            actuator_url = ACTUATOR_URLS[column.lower()]
            try:
                response = requests.post(actuator_url, json={'status': status})
                if response.status_code != 204:
                    print(f"Failed to update {column} on actuator server.")
            except requests.exceptions.RequestException as e:
                print(f"Error sending to actuator server for {column}: {e}")

    connection.commit()

    
@app.route('/api/actuators/status', methods=['GET'])
def get_actuator_status():
    # DB 연결
    connection = get_db_connection()
    cursor = connection.cursor()

    # 각 장치의 최신 상태 가져오기
    cursor.execute("SELECT device_name, dc_fan, led, water_supply, water_drainage FROM actuator ORDER BY act_id DESC LIMIT 1")
    actuator = cursor.fetchone()

    if not actuator:
        return jsonify({'success' : False})

    # 상태를 반환
    return jsonify({
        'success' : True,
        'device_name': actuator['device_name'],
        'led': actuator['led'],
        'dcfan': actuator['dc_fan'],
        'waterpump_fill': actuator['water_supply'],
        'waterpump_drain': actuator['water_drainage']
    })
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)


    
