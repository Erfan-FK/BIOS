<template>
    <div class="p-6 bg-gray-50 h-full">
      <h1 class="text-2xl font-bold mb-6 text-center">General Overview</h1>
  
      <!-- Scrollable Container -->
      <div class="bg-white shadow-md rounded-lg overflow-y-auto p-4 h-[600px]">
        <!-- Summary Stats -->
        <div class="grid grid-cols-3 gap-4 mb-6">
          <div class="bg-gray-100 shadow-md rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold">Total Visits</h3>
            <p class="text-2xl">{{ totalVisits }}</p>
          </div>
          <div class="bg-gray-100 shadow-md rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold">Newcomer Count</h3>
            <p class="text-2xl">{{ totalStudentsSent }}</p>
          </div>
          <div class="bg-gray-100 shadow-md rounded-lg p-4 text-center">
            <h3 class="text-lg font-bold">YKS Improvement</h3>
            <p class="text-2xl">{{ avgYksImprovement }}%</p>
          </div>
        </div>
  
        <!-- Line Chart for YKS Averages -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4 mb-6">
          <h3 class="text-lg font-bold mb-4">Trend of YKS Averages</h3>
          <LineChart :data="lineChartData" />
        </div>
  
        <!-- Top 10 High Schools Table -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4">
          <h3 class="text-lg font-bold mb-4">Top 10 High Schools by YKS Average</h3>
          <table class="w-full border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 p-2">Rank</th>
                <th class="border border-gray-300 p-2">High School</th>
                <th class="border border-gray-300 p-2">YKS Average</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(school, index) in top10Schools" :key="school.highSchool">
                <td class="border border-gray-300 p-2">{{ index + 1 }}</td>
                <td class="border border-gray-300 p-2">{{ school.highSchool }}</td>
                <td class="border border-gray-300 p-2">{{ school.yksAverage }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from "vue";
  import { useHighSchoolStore } from "@/stores/highschoolStore";
  import LineChart from "@/components/LineChart.vue";
  
  const highSchoolStore = useHighSchoolStore();
  const { highSchools } = highSchoolStore;
  
  // Summary Stats
  const totalVisits = computed(() =>
    highSchools.reduce((total, hs) => total + (hs.visitsToBilkent || 0), 0)
  );
  
  const totalStudentsSent = computed(() =>
    highSchools.reduce((total, hs) => total + (hs.studentsToBilkent || 0), 0)
  );
  
  const avgYksImprovement = computed(() => {
    const lastYearAvg = 420; // Mock value for last year's average
    const thisYearAvg =
      highSchools.reduce((total, hs) => total + (hs.yksAverage || 0), 0) /
      (highSchools.length || 1);
    return (((thisYearAvg - lastYearAvg) / lastYearAvg) * 100).toFixed(2);
  });
  
  // Top 10 High Schools
  const top10Schools = computed(() =>
    [...highSchools]
      .sort((a, b) => (b.yksAverage || 0) - (a.yksAverage || 0))
      .slice(0, 10)
  );
  
  // Line Chart Data
  const lineChartData = computed(() => ({
    labels: highSchools.map((hs) => hs.highSchool),
    datasets: [
      {
        label: "YKS Average",
        data: highSchools.map((hs) => hs.yksAverage || 0),
        borderColor: "#4caf50",
        backgroundColor: "rgba(76, 175, 80, 0.2)",
        fill: true,
      },
    ],
  }));
  </script>
  
  <style scoped>
  /* Ensure scrollable container doesn't stretch */
  .bg-white {
    max-height: 100%;
  }
  </style>