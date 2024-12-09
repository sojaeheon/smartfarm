<template>
    <div>
        <AppHeader />
    </div>
    <div class="main">
        <div class="grid-container">
            <!-- Camera -->
            <div class="grid-item" id="camera">
                <img :src="videoSrc" alt="Camera Stream" />
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
                    <Chart v-if="isDataLoaded" :ChartData="currentSensorData" />
                </div>
                <div id="button-container">
                    <button type="button" v-for="(sensor, index) in sensors" :key="index" class="sensors-button"
                        :class="{ 'on': sensor.isOn }" @click="toggleSwitch(sensor)">{{ sensor.label }}</button>
                    <button @click="refreshChart" class="refresh-button">
                        <img src="@/assets/reload.png" alt="새로고침" class="refresh-icon" />
                    </button>
                </div>
                <!-- 새로고침 버튼 추가 -->
                
            </div>

            <!-- Weather -->
            <div class="grid-item" id="weather">
                <h4>&lt; {{ weather.year }}년 {{ weather.month }} {{ weather.date }} {{ weather.days }} &gt;</h4>
                <div class="weather-content">
                    <img :src="weatherIconUrl" alt="Icon" />
                    <div class="weather_text">
                        <p v-if="weather.temp !== null">온도: {{ weather.temp }}℃</p>
                        <p v-if="weather.humidity !== null">습도: {{ weather.humidity }}%</p>
                        <p v-if="weather.description">날씨: {{ weather.description }}</p>
                        <p v-else> 날씨 정보를 불러오는 중...</p>
                    </div>
                </div>
                <div class="forecast">
                    <div class="forecast-list">
                        <div v-for="(hour, index) in hourlyForecast" :key="index" class="forecast-item">
                            <p>{{ hour.time }}</p>
                            <img :src="getWeatherIconUrl(hour.icon)" alt="예보 아이콘" />
                            <p>{{ hour.temp }}℃</p>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import Chart from './Chart.vue';
import axios from 'axios';

export default {
    data() {
        return {
            videoSrc: 'http://202.31.150.31:15915/video_feed',
            actuators: [
                { label: 'DC팬', isOn: false, imgSrc: require('../assets/dcfan.svg') },
                { label: '워터펌프(급수)', isOn: false, imgSrc: require('../assets/water-pump.svg') },
                { label: '워터펌프(배수)', isOn: false, imgSrc: require('../assets/water-pump.svg') },
                { label: 'LED', isOn: false, imgSrc: require('../assets/brightness.svg') },
            ],
            sensors: [
                { label: '조도', isOn: true },
                { label: 'CO2', isOn: false },
                { label: '온도', isOn: false },
                { label: '습도', isOn: false },
                { label: '수위', isOn: false }

            ],
            isDataLoaded: false,
            currentSensorData: {},
            forecastList: [],
            api_key: 'b220e5b857e610bc88ca3db69f5be7be',
            url_base: 'https://api.openweathermap.org/data/2.5/',
            lat: '35.9646',   //군산 위도
            lon: '126.7369',  //군산 경도
            weather: {
                year: null,
                month: null,
                date: null,
                days: null,
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
        // 초기 센서 설정
        this.fetchSensorData();
        // 날씨 데이터 가져오기
        this.fetchWeatherData();
        this.setDateInfo();  // 날짜 설정
    },
    methods: {
        async getActuatorStatus() {
            try {
                const response = await axios.get('/api/actuators/status');
                const status = response.data;
                if(response.data.success){
                    // 각 장치 상태에 맞게 isOn 값을 업데이트
                    this.actuators[0].isOn = status.dcfan === 'on' ? true : false;
                    this.actuators[1].isOn = status.waterpump_fill === 'on' ? true : false;
                    this.actuators[2].isOn = status.waterpump_drain === 'on' ? true : false;
                    this.actuators[3].isOn = status.led === 'on' ? true : false;
                }else{
                    this.actuators[0].isOn = false;
                    this.actuators[1].isOn = false;
                    this.actuators[2].isOn = false;
                    this.actuators[3].isOn = false;
                }
                
                
            } catch (error) {
                console.error('Error fetching actuator status:', error);
            }
        },
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

            // // LED 액추에이터인 경우 서버에 상태 전송
            // if (this.actuators[index].label === 'LED') {
            //     this.controlLed(index);
            // }
            // if (this.actuators[index].label === 'DC팬') {
            //     this.controlDcfan(index);
            // }
            this.controlActuators();
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
            this.isDataLoaded = true; // 차트 데이터가 로드되었음을 표시
        },
        // async controlLed(index) {
        //     // 서버에 POST 요청 보내기
        //     const status = this.actuators[index].isOn ? 'on' : 'off';

        //     await axios.get(`/api/led`, {
        //             params: {
        //                 status: status
        //             }
        //         })
        //         .catch(error => {
        //             console.error('There was a problem with the axios operation:', error);
        //         });
        // },
        // async controlDcfan(index) {
        //     // 서버에 POST 요청 보내기
        //     const status = this.actuators[index].isOn ? 'on' : 'off';

        //     await axios.get(`/api/dcfan`, {
        //         status: status
        //     })
        //         .catch(error => {
        //             console.error('There was a problem with the axios operation:', error);
        //         });
        // },
        async controlActuators() {
            // 장치의 상태 추출
            const statusData = this.actuators.map(actuator => ({
                label: actuator.label,
                isOn: actuator.isOn ? 'on' : 'off'
            }));

            // 서버로 상태 전달
            await axios.post(`/api/actuators`, {
                    status: statusData,  // 모든 장치 상태 전달
                    device_name: this.$store.state.device_name
                })
                .catch(error => {
                    console.error('There was a problem with the axios operation:', error);
                });
        },
        async fetchSensorData() {
            try {
                const response = await axios.get('/api/sensor_graph', {
                    params: {
                        device_name: this.$store.state.device_name  // 쿼리 파라미터로 전달
                    },
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const datas = response.data.data.slice(-1440);

                // 센서 데이터 각각을 별도의 배열에 저장
        // 서버에서 받은 date 값을 그대로 사용
                this.dateArray = datas.map(item => item.date).reverse();
                this.co2Array = datas.map(item => item.co2).reverse();
                this.temperatureArray = datas.map(item => item.temperature).reverse();
                this.humidityArray = datas.map(item => item.humidity).reverse();
                this.lightArray = datas.map(item => item.light).reverse();
                this.waterLevelArray = datas.map(item => item.waterlevel).reverse();

                console.log("Date Array:", this.dateArray);
                console.log("Temperature Array:", this.temperatureArray);

                const sensor = this.sensors.find(sensor => sensor.isOn); // 활성화된 센서 찾기
                if (sensor) {
                    this.currentSensorData = this.getSensorData(sensor); // getSensorData로 데이터를 업데이트
                }
                // 데이터 로드 완료 표시
                this.isDataLoaded = true;
            } catch (error) {
                console.error("센서 데이터를 불러오지 못했습니다:", error);
            }

        },
        getSensorData(sensor) {
            if (!sensor) return {}; // sensor가 undefined일 경우 빈 객체 반환

            let sensorData = [];
            switch (sensor.label) {
                case '온도':
                    sensorData = this.temperatureArray;
                    break;
                case '습도':
                    sensorData = this.humidityArray;
                    break;
                case '조도':
                    sensorData = this.lightArray;
                    break;
                case '수위':
                    sensorData = this.waterLevelArray;
                    break;
                case 'CO2':
                    sensorData = this.co2Array;
                    break;
                default:
                    sensorData = [];
            }
            console.log("Chart Data:", sensorData);  // 콘솔에 데이터 확인
            return {
                dates: this.dateArray,
                datasets: [{
                    label: sensor.label,
                    data: sensorData,
                    backgroundColor: "rgba(54, 162, 235, 0.2)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1,
                    fill: false,  // 선 그래프의 선만 표시하도록 설정
                }]
            };
        },
        getWeatherIconUrl(icon) {
            return icon ? `https://openweathermap.org/img/wn/${icon}@2x.png` : '';
        },
        setDateInfo() {
            const today = new Date();
            const months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"];
            const days = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];

            // this.weather에 날짜 값 설정
            this.weather.year = today.getFullYear();
            this.weather.month = months[today.getMonth()];
            this.weather.date = today.getDate();
            this.weather.days = days[today.getDay()];
        },
        fetchWeatherData() {
            const url = `${this.url_base}weather?lat=${this.lat}&lon=${this.lon}&appid=${this.api_key}&limit=5&lang=kr&units=metric`;
            const forecastUrl = `${this.url_base}forecast?lat=${this.lat}&lon=${this.lon}&appid=${this.api_key}&units=metric&lang=kr`;
            Promise.all([fetch(url), fetch(forecastUrl)])
                .then(async ([currentRes, forecastRes]) => {
                    if (!currentRes.ok || !forecastRes.ok) {
                        throw new Error("Failed to fetch weather data.");
                    }
                    const currentData = await currentRes.json();
                    const forecastData = await forecastRes.json();
                    this.setResult(currentData);
                    this.setHourlyForecast(forecastData.list); // 예보 리스트 설정
                })
                .catch(error => {
                    console.error("날씨 정보 불러오기 실패:", error);
                });
        },
        setResult(data) {
            if (data && data.main && data.weather && data.weather.length > 0) {
                this.weather.temp = data.main.temp; // 온도
                this.weather.humidity = data.main.humidity; // 습도
                this.weather.description = data.weather[0].description; // 날씨 설명
                this.weather.icon = data.weather[0].icon; // 아이콘 값 저장
                console.log("Weather icon:", this.weather.icon); // 아이콘 값 확인
            }
        },
        setHourlyForecast(forecast) {
            // 24시간 예보 데이터를 저장합니다.
            this.hourlyForecast = forecast.slice(0, 8).map(item => ({
                time: item.dt_txt.split(' ')[1].slice(0, 5), // HH:MM 형태로 시간 추출
                temp: item.main.temp,
                icon: item.weather[0].icon,
            }));
        },
        // 새로고침 버튼 클릭 시 호출되는 메서드
        refreshChart() {
            this.fetchSensorData(); // 새 데이터 가져오기
            console.log("Chart data has been refreshed.");
        }
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

/* 기존 스타일 유지 */
.refresh-button {
    margin-top: 1px;
    padding: 8px;
    background-color: transparent;
    border: none;
    cursor: pointer;
}
.refresh-icon {
    width: 40px;
    height: 40px;
}

#camera {
    display: flex;
    justify-content: center;
    align-items: center;
    width: auto;
    height: 40vh;
    /* overflow: hidden; */
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
    margin-top: 0.5vh;
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
    /*margin: 0 10px;*/
    position: relative;
    width: 35vw;
    height: 25vh;
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

.forecast {
    display: flex;
    /* Flexbox로 일렬로 표시 */
    flex-direction: column;
    /* 세로 정렬 */
    align-items: flex-start;
    /* 왼쪽 정렬 */
    margin-top: 10px;
    /* 간격 추가 */
}

.forecast-list {
    display: flex;
    /* Flexbox로 일렬로 표시 */
    overflow-x: auto;
    /* 가로로 넘치는 경우 스크롤 가능 */
}

.forecast-item {
    display: flex;
    /* Flexbox로 내용 정렬 */
    flex-direction: column;
    /* 세로 정렬 */
    align-items: center;
    /* 중앙 정렬 */
    margin-right: 10px;
    /* 간격 추가 */
    text-align: center;
    /* 텍스트 중앙 정렬 */
    font-size: 12px;
    /* 글자 크기 조정 */
}

.forecast-item img {
    width: 40px;
    /* 아이콘 크기 조정 */
    height: 40px;
    /* 아이콘 크기 조정 */
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

    #Chart {
        width: 75vw;
    }

    .sensors-button {
    width: 10vw;
}

}
</style>