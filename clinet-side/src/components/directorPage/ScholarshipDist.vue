<template>
    <div class="p-6 bg-gray-50 h-full">
      <h1 class="text-2xl font-bold mb-6 text-center">Scholarship Distribution</h1>
  
      <!-- Scrollable Container -->
      <div class="bg-white shadow-md rounded-lg overflow-y-auto p-4 h-[600px]">
        <!-- Stacked Bar Chart -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4">
          <h3 class="text-lg font-bold text-center mb-4">Scholarship Breakdown</h3>
          <div class="flex justify-center items-center">
            <canvas ref="scholarshipBarChart"></canvas>
          </div>
        </div>
  
        <!-- Summary Table -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4 mt-6">
          <h3 class="text-lg font-bold mb-4 text-center">Scholarship Details by High School</h3>
          <table class="w-full border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 p-2">High School</th>
                <th class="border border-gray-300 p-2">Full Scholarships</th>
                <th class="border border-gray-300 p-2">Half Scholarships</th>
                <th class="border border-gray-300 p-2">No Scholarships</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="school in highSchools" :key="school.highSchool">
                <td class="border border-gray-300 p-2">{{ school.highSchool }}</td>
                <td class="border border-gray-300 p-2">{{ school.fullScholarship }}</td>
                <td class="border border-gray-300 p-2">{{ school.halfScholarship }}</td>
                <td class="border border-gray-300 p-2">{{ school.noScholarship }}</td>
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
  import { useHighSchoolStore } from "@/stores/highschoolStore";
  
  // Register Chart.js components
  Chart.register(...registerables);
  
  const highSchoolStore = useHighSchoolStore();
  const { highSchools } = highSchoolStore;
  
  // Chart reference
  const scholarshipBarChart = ref(null);
  
  // Scholarship Bar Chart Data
  const scholarshipBarData = computed(() => ({
    labels: highSchools.map((hs) => hs.highSchool),
    datasets: [
      {
        label: "Full Scholarships",
        data: highSchools.map((hs) => hs.fullScholarship),
        backgroundColor: "#90EE90",
      },
      {
        label: "Half Scholarships",
        data: highSchools.map((hs) => hs.halfScholarship),
        backgroundColor: "#0000FF",
      },
      {
        label: "No Scholarships",
        data: highSchools.map((hs) => hs.noScholarship),
        backgroundColor: "#f44336",
      },
    ],
  }));
  
  // Chart rendering logic
  const renderBarChart = () => {
    new Chart(scholarshipBarChart.value, {
      type: "bar",
      data: scholarshipBarData.value,
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
          },
          y: {
            stacked: true,
            beginAtZero: true,
          },
        },
      },
    });
  };
  
  onMounted(() => {
    renderBarChart();
  });
  </script>
  
  <style scoped>
  /* Ensure the chart is responsive within the container */
  canvas {
    max-width: 100%;
    height: 400px;
  }
  </style>
  