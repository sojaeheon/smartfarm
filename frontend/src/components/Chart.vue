<template>
  <canvas v-if="ChartData" ref="BarChart"></canvas>
  <p v-else>차트를 표시하려면 센서를 선택하세요.</p>
</template>

<script>
import Chart from "chart.js/auto";
import zoomPlugin from "chartjs-plugin-zoom";

Chart.register(zoomPlugin);

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
    this.renderChart();
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
      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const canvas = this.$refs.BarChart;
      if (canvas) {
        const ctx = canvas.getContext("2d");

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
                ticks: {
                  autoSkip: false, // 레이블 자동 생략 비활성화
                  maxRotation: 0, // 레이블 회전 각도를 조정하여 겹침 방지
                  minRotation: 0,
                }
              }
            },
            plugins: {
              zoom: {
                pan: {
                  enabled: true,
                  mode: "x",
                  threshold: 500,
                },
                zoom: {
                  wheel: {
                    enabled: true,
                  },
                  pinch: {
                    enabled: true,
                  },
                  mode: "x",
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
