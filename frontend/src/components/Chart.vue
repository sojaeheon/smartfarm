<template>
  <canvas v-if="ChartData" ref="BarChart"></canvas>
  <p v-else>차트를 표시하려면 센서를 선택하세요.</p>
</template>

<script>
import Chart from "chart.js/auto";

export default {
  name: "BarChart",
  props: {
    ChartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chartInstance: null
    };
  },
  mounted() {
    // ChartData가 있는 경우에만 차트 렌더링
    //if (this.ChartData && Object.keys(this.ChartData).length > 0) {
    this.renderChart();
    //}
  },
  watch: {
    ChartData(newData) {
      if (newData && Object.keys(newData).length > 0) {
        this.renderChart();
      }
    }
  },
  methods: {
    renderChart() {
      // 기존 차트 인스턴스가 있으면 파괴
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const canvas = this.$refs.BarChart;
      if (canvas) {
        const ctx = canvas.getContext("2d");

        // 새로운 차트 인스턴스 생성
        this.chartInstance = new Chart(ctx, {
          type: "line",
          data: {
            labels: this.ChartData.dates,
            datasets: this.ChartData.datasets,
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
              },
              x: {
                display: true,
                title: {
                  display: true,
                  text: "Date",
                },
              },
            },
          },
        });
      } else {
        console.error("Canvas reference is null.");
      }
    }
  },
};
</script>

<style></style>