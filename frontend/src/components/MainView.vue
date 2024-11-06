<template>
    <div>
        <AppHeader />
    </div>
    <div class="main">
        <div class="grid-container">
            <!-- Camera -->
            <div class="grid-item" id="camera">
                <img :src="videoSrc" alt="Camera Stream" />
                <!-- <video ref="video" width="100%" autoplay></video> -->
            </div>

            <!-- Actuator Buttons -->
            <div class="grid-item" id="actuator-container">
                <div v-for="(actuator, index) in actuators" :key="index" class="actuator">
                    <button type="button" :class="{ on: actuator.isOn }" @click="toggleActuator(index)">
                        <img :src="actuator.imgSrc" alt="Actuator Image" /> <br> {{ actuator.isOn ? 'ON' : 'OFF' }}
                    </button>
                    <div id="actuator-label">
                        {{ actuator.label }}
                    </div>
                </div>
            </div>

            <!-- Current Data -->
            <div class="grid-item" id="current-data">
                <div id="Chart">
                    <Chart :ChartData="currentSensorData" />
                </div>
                <div id="button-container">
                    <button type="button" v-for="(sensor, index) in sensors" :key="index" class="sensors-button"
                        :class="{ 'on': sensor.isOn }" @click="toggleSwitch(sensor)">{{ sensor.label }}</button>
                </div>
            </div>

            <!-- Weather -->
            <div class="grid-item" id="weather">
                <div class="weather-content">
                    <img :src="weatherIconUrl" alt="Icon" />
                    <div class="weather_text">
                        <p v-if="weather.temp !== null">온도: {{ weather.temp }}℃</p>
                        <p v-if="weather.humidity !== null">습도: {{ weather.humidity }}%</p>
                        <p v-if="weather.description">날씨: {{ weather.description }}</p>
                        <p v-else> 날씨 정보를 불러오는 중...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import Chart from './Chart.vue';
import axios from 'axios'; // axios를 사용해 API 호출을 합니다.

export default {
    data() {
        return {
            videoSrc: 'http://192.168.0.38:7777/video_feed',
            actuators: [
                { label: 'DC팬', isOn: false, imgSrc: require('../assets/dcfan.svg') },
                { label: '워터펌프(급수)', isOn: false, imgSrc: require('../assets/water-pump.svg') },
                { label: '워터펌프(배수)', isOn: false, imgSrc: require('../assets/water-pump.svg') },
                { label: 'LED', isOn: false, imgSrc: require('../assets/brightness.svg') },
            ],
            sensors: [
                { label: '조도', isOn: true},
                { label: 'CO2', isOn: false},
                { label: '온도', isOn: false},
                { label: '습도', isOn: false},
                { label: '수위', isOn: false}
            ],
            currentSensorData: {},
            api_key: 'b220e5b857e610bc88ca3db69f5be7be',
            url_base: 'https://api.openweathermap.org/data/2.5/',
            lat: '35.9646',   //군산 위도
            lon: '126.7369',  //군산 경도
            weather: {
                temp: null,
                humidity: null,
                description: '',
                icon: '',
            },
        };
    },
    options: {
        responsive: false
    },
    computed: {
        // weather.icon 값이 있을 때 아이콘 URL 생성
        weatherIconUrl() {
            const iconUrl = this.weather.icon ? `https://openweathermap.org/img/wn/${this.weather.icon}@2x.png` : '';
            console.log("Weather icon URL:", iconUrl); // 아이콘 URL 로그 출력
            return iconUrl;
        }
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

        // 초기 센서 설정
        this.currentSensorData = this.getSensorData(this.sensors.find(sensor => sensor.isOn));
        // 센서 데이터 가져오기(차트)
        this.fetchSensorData();  
        // 날씨 데이터 가져오기
        this.fetchWeatherData();
    },
    methods: {
        toggleActuator(index) {
            if (this.actuators[index].label === '워터펌프(급수)') {
                // '워터펌프(급수)' 버튼을 눌렀을 때 '워터펌프(배수)'를 비활성화
                this.actuators.forEach((actuator, idx) => {
                    if (actuator.label === '워터펌프(배수)') {
                        this.actuators[idx].isOn = false;
                    }
                });
            } else if (this.actuators[index].label === '워터펌프(배수)') {
                // '워터펌프(배수)' 버튼을 눌렀을 때 '워터펌프(급수)'를 비활성화
                this.actuators.forEach((actuator, idx) => {
                    if (actuator.label === '워터펌프(급수)') {
                        this.actuators[idx].isOn = false;
                    }
                });
            }
            // 직접 상태를 변경
            this.actuators[index].isOn = !this.actuators[index].isOn;
            console.log(`Actuator ${this.actuators[index].label} is now ${this.actuators[index].isOn ? 'ON' : 'OFF'}`);
            // 액추에이터가 이미 켜져 있는 경우-시간설정
            // if (this.actuators[index].isOn) {
            //     this.actuators[index].isOn = false; // 바로 끄기
            // } else {
            //     // 액추에이터 켜기
            //     this.actuators[index].isOn = true;
            //     console.log(`Actuator ${this.actuators[index].label} is now ON`);

            //     // 설정된 시간 후에 자동으로 끄기 (n분=n*60*1000, n시간=n*60*60*1000)
            //     const offTime = 60000; // 1시간(밀리초 단위)
            //     setTimeout(() => {
            //         this.actuators[index].isOn = false;
            //         console.log(`Actuator ${this.actuators[index].label} is now OFF after ${offTime / 1000 / 60} minutes`);
            //     }, offTime);
            // }
        },
        toggleSwitch(sensor) {
            // 만약 클릭된 센서가 이미 켜져 있으면 끄기
            if (sensor.isOn) {
                sensor.isOn = false;
            } else {
                // 클릭된 센서가 꺼져 있으면 다른 모든 센서를 끄고 이 센서만 켜기
                this.sensors.forEach(s => { s.isOn = false });
                sensor.isOn = true;
            }
            this.currentSensorData = this.getSensorData(sensor);
        },
        async fetchSensorData() {
            try {
                const response = await axios.get('/api/sensor_graph');  // 데이터베이스에서 센서 데이터 가져오기
                const data = response.data.slice(-10);  // 최근 10개 데이터만 가져옵니다.

                this.sensors = data.map(item => ({
                    date: item.date,
                    temperature: item.temperature,
                    humidity: item.humidity,
                    light: item.light,
                    waterlevel: item.waterlevel,
                    co2: item.co2,
                }));

                this.updateChartData();  // 차트 데이터 업데이트
            } catch (error) {
                console.error("센서 데이터를 불러오지 못했습니다:", error);
            }
        },
        updateChartData() {
            this.currentSensorData = {
                labels: this.sensors.map(item => item.date),  // x축에 날짜 설정
                datasets: [
                    { label: '온도', data: this.sensors.map(item => item.temperature)},
                    { label: '습도', data: this.sensors.map(item => item.humidity)},
                    { label: '조도', data: this.sensors.map(item => item.light)},
                    { label: '수위', data: this.sensors.map(item => item.waterlevel)},
                    { label: 'CO2', data: this.sensors.map(item => item.co2)},
                ]
            };
        },
        fetchWeatherData() {
            const url = `${this.url_base}weather?lat=${this.lat}&lon=${this.lon}&appid=${this.api_key}&lang=kr&units=metric`;
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Network response was not ok. Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => { // 데이터 구조에 맞게 경로 설정
                    console.log(data); // 응답 전체 확인
                    this.setResult(data);
                })
                .catch(error => {
                    console.error("날씨 정보 불러오기 실패:", error);
                });
        },
        setResult(data) {
            if (data && data.main && data.weather && data.weather.length > 0) {
                this.weather = {
                    temp: data.main.temp, // 온도
                    humidity: data.main.humidity, // 습도
                    description: data.weather[0].description, // 날씨 설명
                    icon: data.weather[0].icon // 아이콘 값 저장
                };
                console.log("Weather icon:", this.weather.icon); // 아이콘 값 확인
            }
        },
        dateBuilder: function () {
            let d = new Date();
            let months = [
                "1월", "2월", "3월", "4월", "5월", "6월",
                "7월", "8월", "9월", "10월", "11월", "12월"
            ];
            let days = ["월요일", "화요일", "수요일", "목요일", "금요일"];
            let day = days[d.getDay()];
            let date = d.getDate();
            let month = months[d.getMonth()];
            let year = d.getFullYear();
            return `${day} ${date} ${month} ${year}`;
        },

    },
    components: {
        AppHeader,
        Chart
    }
};
</script>

<style>
.main {
    display: flex;

    margin-top: 10px;
    margin-left: 10px;
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    gap: 2vh;
    width: 83vw;
    height: 80vh;
    margin: 1vh 0 0 1vw;
}

.grid-item {
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px solid rgba(0, 0, 0, 0.5);
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
    height: 10vh;
    border: 2px solid #F99E17;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    cursor: pointer;
    font-size: large;
}

.on {
    background-color: #F99E17;
}

#actuator-label {
    text-align: center;
    margin: 0.5vw 0;
}

#current-data {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* 중앙 정렬 */
}

#button-container {
    /* margin-top: 5vh;
    margin-left: 15vw; */
    display: flex;
    justify-content: center;
    /* 버튼들을 중앙에 배치 */
    margin-top: 10px;
    gap: 10px;
    /* 버튼 간 간격 */
}

.sensors-button {
    width: 5vw;
    height: 6vh;
    border: 2px solid #F99E17;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
    display: inline-block;
    cursor: pointer;
}

.sensors-button.on {
    background-color: #F99E17;
}

#Chart {
    margin: 0 10px;
    position: relative;
    width: 30vw;
}

#data-button {
    width: 7vw;
    height: 10vh;
    border: 2px solid #63C758;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    margin: 0 0.25vw;
    font-size: medium;
}

#weather {
    display: flex;
    flex-direction: column;
    /* 세로 정렬 */
    align-items: center;
    /* 가로 중앙 정렬 */
    justify-content: center;
    /* 세로 중앙 정렬 */
    text-align: center;
    /* 텍스트 중앙 정렬 */
}

.weather-content {
    display: flex;
    /* 아이콘과 텍스트를 가로로 정렬 */
    align-items: center;
    /* 세로 중앙 정렬 */
}

.weather_text p {
    margin: 3px 0;
    /* p 태그 간 간격 조정 */
}

.weather img {
    width: 30px;
    height: 30px;
}

@media (max-aspect-ratio: 1/1) {
    .grid-container {
        grid-template-columns: 1fr;
        grid-template-rows: auto;
        /* margin: 2vw 0; */
    }

    .actuator button {
        width: 15vw;
        color: black;
    }

    #data-button {
        width: 15vw;
        color: black;
        margin: 0 1vw;
    }
}

#camera {
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    /* 내용이 넘치는 경우 숨김 처리 */
}

#camera img,
#camera video {
    width: 100%;
    /* 부모의 너비에 맞춰 100% 사용 */
    height: auto;
    /* 높이는 자동 조절 */
    max-height: 100%;
    /* 최대 높이를 100%로 설정 */
}
</style>
