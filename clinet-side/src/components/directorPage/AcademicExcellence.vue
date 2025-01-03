<template>
  <div class="p-6 bg-gray-50 h-full">
    <h1 class="text-2xl font-bold mb-6 text-center">Academic Excellence</h1>

    <!-- Scrollable Container -->
    <div class="bg-white shadow-md rounded-lg overflow-y-auto p-4 h-[600px]">
      
      <!-- Scatter Plot -->
      <div class="bg-gray-100 shadow-md rounded-lg p-4 mb-6">
        <h3 class="text-lg font-bold text-center mb-4">YKS Average vs. Students Came</h3>
        <div class="flex justify-center items-center">
          <canvas ref="scatterChart"></canvas>
        </div>
      </div>

      <!-- Summary Table -->
      <div class="bg-gray-100 shadow-md rounded-lg p-4">
        <h3 class="text-lg font-bold mb-4">High Performers with Low Student Count</h3>
        <table class="w-full border-collapse border border-gray-300">
          <thead class="bg-gray-200">
            <tr>
              <th class="border border-gray-300 p-2">High School</th>
              <th class="border border-gray-300 p-2">YKS Average</th>
              <th class="border border-gray-300 p-2">Students Sent</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="school in academicOutliers"
              :key="school.highSchool"
            >
              <td class="border border-gray-300 p-2">{{ school.highSchool }}</td>
              <td class="border border-gray-300 p-2">{{ school.yksAverage }}</td>
              <td class="border border-gray-300 p-2">{{ school.studentsToBilkent }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Chart, registerables } from "chart.js";

// Register Chart.js components
Chart.register(...registerables);

import { useHighSchoolStore } from "@/stores/highschoolStore";

const highSchoolStore = useHighSchoolStore();
const { highSchools } = highSchoolStore;

// Scatter Chart Reference
const scatterChart = ref(null);

// Scatter Plot Data
const academicScatterData = computed(() => ({
  datasets: [
    {
      label: "High Schools",
      data: highSchools.map((hs) => ({
        x: hs.yksAverage,
        y: hs.studentsToBilkent,
      })),
      backgroundColor: "#4caf50",
      pointStyle: "circle",
      radius: 6,
    },
  ],
}));

// Scatter Plot Options
const scatterChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: "top",
    },
    tooltip: {
      enabled: true,
    },
    datalabels: {
      formatter: (_, ctx) => highSchools[ctx.dataIndex].highSchool,
      align: "bottom",
      color: "#4caf50",
      font: {
        size: 10,
      },
    },
  },
  scales: {
    x: {
      title: {
        display: true,
        text: "YKS Average",
      },
      beginAtZero: false,
    },
    y: {
      title: {
        display: true,
        text: "Students Sent to Bilkent",
      },
      beginAtZero: true,
    },
  },
};

// Render Scatter Chart
const renderScatterChart = () => {
  if (scatterChart.value) {
    new Chart(scatterChart.value, {
      type: "scatter",
      data: academicScatterData.value,
      options: scatterChartOptions,
    });
  }
};

onMounted(() => {
  renderScatterChart();
});

// High Performers with Low Student Count
const academicOutliers = computed(() =>
  highSchools
    .filter((hs) => hs.yksAverage > 430 && hs.studentsToBilkent < 30) // More inclusive range
    .sort((a, b) => b.yksAverage - a.yksAverage)
);
</script>

<style scoped>
/* Ensure the chart is responsive */
canvas {
  max-width: 100%;
  height: 400px;
}

/* Scrollable container */
.bg-white {
  max-height: 100%;
}
</style>
