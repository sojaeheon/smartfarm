<template>
  <header>
    <div>
      <AppHeader />
    </div>
  </header>
  <div id="Chart">
    <Chart :ChartData="currentSensorData" />
  </div>
  <div id="button-container">
    <button type="button" v-for="(sensor, index) in sensors" :key="index" class="sensors-button"
      :class="{ 'on': sensor.isOn }" @click="toggleSwitch(sensor)">{{ sensor.label }}</button>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue';
import Chart from './Chart.vue';

export default {
  name: 'GraphView',
  data() {
    return {
      sensors: [
        { label: '조도', isOn: true, data: [10, 20, 30, 40, 50, 60] },
        { label: 'CO2', isOn: false, data: [12, 22, 32, 42, 52, 62] },
        { label: '온도', isOn: false, data: [15, 25, 35, 45, 55, 65] },
        { label: '습도', isOn: false, data: [8, 18, 28, 38, 48, 58] },
        { label: '수위', isOn: false, data: [9, 19, 29, 39, 49, 59] }
      ],
      currentSensorData: {}
    };
  },
  mounted() {
    // 초기 센서 설정
    this.currentSensorData = this.getSensorData(this.sensors.find(sensor => sensor.isOn));
  },
  methods: {
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
    getSensorData(sensor) {
      return {
        labels: ["1", "2", "3", "4", "5", "6"],  // x축 라벨 (예시)
        datasets: [
          {
            label: sensor.label,
            data: sensor.data,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1
          }
        ]
      };
    }
  },
  components: {
    AppHeader,
    Chart
  }
};
</script>

<style>
#button-container {
  margin-top: 5vh;
  margin-left: 15vw;
}

.sensors-button {
  width: 7vw;
  height: 7vh;
  margin: 1vh 2vw;
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
  margin: 2vh 10vw;
  display: flex;
  width: 70vw;
}
</style>
