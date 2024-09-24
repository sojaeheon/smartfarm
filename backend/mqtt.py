import paho.mqtt.client as mqtt
import threading   # 스레드 사용하기 위해 필요


MQTT_BROKER = "192.168.0.34"  # mqtt 브로커 주소
MQTT_PORT = 1883  # mqtt 브로커가 사용하는 포트 번호, 1883이 기본값

# 토픽들
MQTT_TEMP = "sensor/temp" 
temp = "None"

MQTT_HUMI = "sensor/humi"
humi = "None"


#락 설정
data_lock = threading.Lock()  # 데이터 보호를 위한 락
# 데이터 접근을 보호하기 위한 락, 여러 스레드가 동시에 
# 데이터에 접근할 때 문제가 생기지 않도록 함


# MQTT 메시지 처리 콜백 함수
def on_message(client, userdata, message):
    global temp, humi                         # 여기에 센서 변수 추가
    with data_lock:  # sensor_data에 대한 동시 접근을 방지하기 위해 락을 사용
        if message.topic=="sensor/temp" :
            temp = message.payload.decode()  
            print(f"Received temp data message: {temp}")
            
        if message.topic=="sensor/humi" :
            humi = message.payload.decode() 
            print(f"Received humi data message: {humi}")


# MQTT 클라이언트 설정 함수
def setup_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)  # 브로커 주소, 포트, 타임아웃 설정
    
    client.subscribe("sensor/#")  # sensor/ 로 시작하는 모든 토픽을 구독
    return client 


# MQTT 클라이언트를 백그라운드에서 실행하는 함수
def start_mqtt():
    mqtt_client = setup_mqtt()  # mqtt 클라이언트 설정
    mqtt_client.loop_start()   # 비동기적으로 mqtt 네트워크 루프를 시작