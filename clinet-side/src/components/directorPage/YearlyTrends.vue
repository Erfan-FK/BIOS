<template>
    <div class="p-6 bg-gray-50 h-full">
      <h1 class="text-2xl font-bold mb-6">Yearly Trends</h1>
  
      <!-- Scrollable Container -->
      <div class="bg-white shadow-md rounded-lg overflow-y-auto p-4 h-[600px]">
        <!-- Students Sent Line Chart -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4 mb-6">
          <h3 class="text-lg font-bold text-center mb-4">Number of Students at Bilkent</h3>
          <div class="flex justify-center items-center">
            <canvas ref="studentsChart"></canvas>
          </div>
        </div>
  
        <!-- Average YKS Scores Line Chart -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4 mb-6">
          <h3 class="text-lg font-bold text-center mb-4">Average YKS Scores of Bilkent Students</h3>
          <div class="flex justify-center items-center">
            <canvas ref="yksChart"></canvas>
          </div>
        </div>
  
        <!-- Scholarship Distribution Stacked Bar Chart -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4">
          <h3 class="text-lg font-bold text-center mb-4">Scholarship Distribution</h3>
          <div class="flex justify-center items-center">
            <canvas ref="scholarshipChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </template>


<script setup>
import { ref, onMounted } from "vue";
import { Chart, registerables } from "chart.js";

// Register Chart.js components
Chart.register(...registerables);

// Mock Yearly Data for Bilkent
const yearlyBilkentData = [
  { year: 2019, totalStudents: 4000, fullScholarship: 1200, halfScholarship: 1800, noScholarship: 1000, yksAverage: 445 },
  { year: 2020, totalStudents: 4200, fullScholarship: 1300, halfScholarship: 1900, noScholarship: 1000, yksAverage: 450 },
  { year: 2021, totalStudents: 4400, fullScholarship: 1400, halfScholarship: 2000, noScholarship: 1000, yksAverage: 455 },
  { year: 2022, totalStudents: 4600, fullScholarship: 1500, halfScholarship: 2100, noScholarship: 1000, yksAverage: 460 },
  { year: 2023, totalStudents: 4800, fullScholarship: 1600, halfScholarship: 2200, noScholarship: 1000, yksAverage: 465 },
];

// Chart References
const studentsChart = ref(null);
const yksChart = ref(null);
const scholarshipChart = ref(null);

// Render Students Chart
const renderStudentsChart = () => {
  new Chart(studentsChart.value, {
    type: "line",
    data: {
      labels: yearlyBilkentData.map((data) => data.year),
      datasets: [
        {
          label: "Total Students at Bilkent",
          data: yearlyBilkentData.map((data) => data.totalStudents),
          borderColor: "#4caf50",
          backgroundColor: "rgba(76, 175, 80, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          enabled: true,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Year",
          },
        },
        y: {
          title: {
            display: true,
            text: "Number of Students",
          },
          beginAtZero: true,
        },
      },
    },
  });
};

// Render YKS Chart
const renderYksChart = () => {
  new Chart(yksChart.value, {
    type: "line",
    data: {
      labels: yearlyBilkentData.map((data) => data.year),
      datasets: [
        {
          label: "Average YKS Score",
          data: yearlyBilkentData.map((data) => data.yksAverage),
          borderColor: "#2196f3",
          backgroundColor: "rgba(33, 150, 243, 0.2)",
          fill: true,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          enabled: true,
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Year",
          },
        },
        y: {
          title: {
            display: true,
            text: "YKS Average",
          },
          beginAtZero: true,
        },
      },
    },
  });
};

// Render Scholarship Distribution Chart
const renderScholarshipChart = () => {
  new Chart(scholarshipChart.value, {
    type: "bar",
    data: {
      labels: yearlyBilkentData.map((data) => data.year),
      datasets: [
        {
          label: "Full Scholarships",
          data: yearlyBilkentData.map((data) => data.fullScholarship),
          backgroundColor: "#90EE90",
        },
        {
          label: "Half Scholarships",
          data: yearlyBilkentData.map((data) => data.halfScholarship),
          backgroundColor: "#0000FF",
        },
        {
          label: "No Scholarships",
          data: yearlyBilkentData.map((data) => data.noScholarship),
          backgroundColor: "#f44336",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          enabled: true,
        },
      },
      scales: {
        x: {
          stacked: true,
          title: {
            display: true,
            text: "Year",
          },
        },
        y: {
          stacked: true,
          title: {
            display: true,
            text: "Number of Scholarships",
          },
          beginAtZero: true,
        },
      },
    },
  });
};

// Render Charts on Component Mount
onMounted(() => {
  renderStudentsChart();
  renderYksChart();
  renderScholarshipChart();
});
</script>

<style scoped>
canvas {
  max-width: 100%;
  height: 400px;
}

/* Ensure scrollable container respects parent dimensions */
.bg-white {
  max-height: 100%;
}
</style>
