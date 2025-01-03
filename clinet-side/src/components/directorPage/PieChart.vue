<template>
  <div class="w-full h-[300px]">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Chart, PieController, ArcElement, Tooltip, Legend } from "chart.js";

// Register the necessary components for Chart.js
Chart.register(PieController, ArcElement, Tooltip, Legend);

const props = defineProps({
  chartData: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    default: () => ({
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
      },
    }),
  },
});

const chartCanvas = ref(null);
let chartInstance = null;

onMounted(() => {
  if (chartCanvas.value) {
    chartInstance = new Chart(chartCanvas.value, {
      type: "pie",
      data: props.chartData,
      options: props.options,
    });
  }
});

// Cleanup to avoid memory leaks
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
</script>

<style scoped>
canvas {
  max-width: 100%;
  max-height: 100%;
}
</style>
