<template>
    <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { defineComponent, ref, onMounted, watch } from "vue";
  import { Chart, registerables } from "chart.js";
  
  // Register Chart.js components
  Chart.register(...registerables);
  
  export default defineComponent({
    name: "LineChart",
    props: {
      data: {
        type: Object,
        required: true,
      },
      options: {
        type: Object,
        default: () => ({
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: "X Axis",
              },
            },
            y: {
              title: {
                display: true,
                text: "Y Axis",
              },
            },
          },
        }),
      },
    },
    setup(props) {
      const chartCanvas = ref(null);
      let chartInstance = null;
  
      const renderChart = () => {
        if (chartInstance) {
          chartInstance.destroy(); // Destroy previous instance to avoid overlapping
        }
        chartInstance = new Chart(chartCanvas.value, {
          type: "line",
          data: props.data,
          options: props.options,
        });
      };
  
      onMounted(renderChart);
      watch(
        () => props.data,
        () => {
          renderChart();
        }
      );
  
      return {
        chartCanvas,
      };
    },
  });
  </script>
  
  <style scoped>
  .chart-container {
    width: 85%; /* Slightly smaller than the full width */
    max-width: 1000px; /* Adjust the maximum width */
    margin: 0 auto; /* Center the chart horizontally */
  }
  
  canvas {
    max-width: 100%;
    height: 500px; /* Slightly reduce the height */
  }
  </style>
  