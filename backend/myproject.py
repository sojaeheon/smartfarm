from flask import Flask, jsonify, g, request
import pymysql

app = Flask(__name__)

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


@app.route("/api/", methods=['GET'])
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

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
        return jsonify({"success": True, "message": "Login successful."})
    else:
        return jsonify({"success": False, "message": "Invalid username or password."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6000)


    