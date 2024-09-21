<template>
    <div>
        <AppHeader />
    </div>
    <div class="grid-container">
        <!-- Camera -->
        <div class="grid-item" id="camera">
            camera
            <!-- <video ref="video" width="100%" autoplay></video> -->
        </div>

        <!-- Actuator Buttons -->
        <div class="grid-item" id="actuator-container">
            <div v-for="(actuator, index) in actuators" :key="index" class="actuator">
                <button type="button" :class="{ on: actuator.isOn }" @click="toggleActuator(index)">
                    {{ actuator.label }} <br> {{ actuator.isOn ? 'ON' : 'OFF' }}
                </button>
            </div>
        </div>

        <!-- Current Data -->
        <div class="grid-item" id="current-data">
            <ul>
                <li v-for="(value, key) in data" :key="key">{{ key }} <br> {{ value }}</li>
            </ul>
        </div>

        <!-- Weather -->
        <div class="grid-item" id="weather">
            <h3>현재 날씨</h3>
            <p>온도: {{ weather.temp }}°C</p>
            <p>습도: {{ weather.humidity }}%</p>
            <p>날씨: {{ weather.description }}</p>
        </div>
    </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';

export default {
    data() {
        return {
            actuators: [
                { label: '조도', isOn: false },
                { label: 'CO2', isOn: false },
                { label: '온도', isOn: false },
                { label: '습도', isOn: false },
                { label: '수위', isOn: false }
            ],
            data: {
                온도: '22°C',
                습도: '45%',
                CO2: '400ppm',
                조도: '350lux',
                수위: '50%',
            },
            weather: {
                temp: '',
                humidity: '',
                description: ''
            }
        };
    },
    mounted() {
        // 웹캠 접근
        /*navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                this.$refs.video.srcObject = stream;
            })
            .catch(error => {
                console.error("카메라 접근 실패:", error);
            });*/
        // 날씨 데이터 가져오기
        this.fetchWeatherData();
    },
    methods: {
        toggleActuator(index) {
            // 직접 상태를 변경
            this.actuators[index].isOn = !this.actuators[index].isOn;
            console.log(`Actuator ${this.actuators[index].label} is now ${this.actuators[index].isOn ? 'ON' : 'OFF'}`);
        },
        fetchWeatherData() {
            // 기상청 API 요청 예시
            fetch('https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid=YOUR_API_KEY&units=metric')
                .then(response => response.json())
                .then(data => {
                    this.weather.temp = data.main.temp;
                    this.weather.humidity = data.main.humidity;
                    this.weather.description = data.weather[0].description;
                })
                .catch(error => {
                    console.error("날씨 정보 불러오기 실패:", error);
                });
        }
    },
    components: {
        AppHeader,
    }
};
</script>

<style>
.grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 2vh;
    width: 83vw;
    height: 80vh;
    margin: 2vh 0 0 8.5vw;
}

.grid-item {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px solid #000;
    border-radius: 8px;
    padding: 10px;
}

#actuator-container {
    display: flex;
    flex-direction: row;
    align-items: center;
}

.actuator {
    margin: 0 5px;
    /* 각 actuator 사이에 간격 추가 */
}

.actuator button {
    width: 7vw;
    height: 7vh;
    border: 2px solid #F99E17;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    cursor: pointer;
}

.on {
    background-color: #F99E17;
}

.grid-item ul {
    display: flex;
    list-style: none;
    padding: 0;
}

.grid-item li {
    width: 7vw;
    height: 10vh;
    border: 2px solid #63C758;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    padding: 2vh 0;
    margin: 0 0.25vw;
}

@media (max-width: 768px) {
    .grid-container {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        margin: 2vw 0;
    }

    .actuator button {
        width: 15vw;
        height: 7vh;
        color: black;
        border: 2px solid #F99E17;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        display: inline-block;
        cursor: pointer;
    }
}
</style>
