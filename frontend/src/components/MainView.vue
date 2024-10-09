<template>
    <div>
        <AppHeader />
    </div>
    <div class="main">
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
                    <img :src="actuator.imgSrc" alt="Actuator Image" /> <br> {{ actuator.isOn ? 'ON' : 'OFF' }}
                </button>
                <div id="actuator-label">
                    {{ actuator.label }}
                </div>
            </div>
        </div>

        <!-- Current Data -->
        <div class="grid-item" id="current-data">
            <button v-for="(value, key) in data" :key="key" id="data-button">{{ key }} <br> {{ value }}</button>
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

export default {
    data() {
        return {
            actuators: [
                { label: 'DC팬', isOn: false, imgSrc: require('../assets/dcfan.svg') },
                { label: '워터펌프', isOn: false, imgSrc: require('../assets/water-pump.svg') },
                { label: 'LED', isOn: false, imgSrc: require('../assets/brightness.svg') },
            ],
            data: {
                온도: '22°C',
                습도: '45%',
                CO2: '400ppm',
                조도: '350lux',
                수위: '50%',
            },
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
        setResult(data){
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
            let days = [ "월요일", "화요일", "수요일", "목요일", "금요일" ];
            let day = days[d.getDay()];
            let date = d.getDate();
            let month = months[d.getMonth()];
            let year = d.getFullYear();
            return `${day} ${date} ${month} ${year}`;
        },        
       
    },
    components: {
        AppHeader,
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
    height: 9vh;
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
#actuator-label
{
    text-align: center;
    margin: 0.5vw 0; 
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
    flex-direction: column; /* 세로 정렬 */
    align-items: center; /* 가로 중앙 정렬 */
    justify-content: center; /* 세로 중앙 정렬 */
    text-align: center; /* 텍스트 중앙 정렬 */
}

.weather-content {
    display: flex; /* 아이콘과 텍스트를 가로로 정렬 */
    align-items: center; /* 세로 중앙 정렬 */
}

.weather_text p {
    margin: 3px 0; /* p 태그 간 간격 조정 */
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
</style>
