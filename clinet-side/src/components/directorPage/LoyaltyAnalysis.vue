<template>
    <div class="p-6 bg-gray-50 h-full">
      <h1 class="text-2xl font-bold mb-6 text-center">Bilkent Loyalty Analysis</h1>
  
      <!-- Scrollable Container -->
      <div class="bg-white shadow-md rounded-lg overflow-y-auto p-4 h-[600px]">
        
        <!-- Schools by Loyalty Level Table -->
        <div class="bg-gray-100 shadow-md rounded-lg p-4">
          <h3 class="text-lg font-bold mb-4">Schools by Loyalty Level</h3>
          <table class="w-full border-collapse border border-gray-300">
            <thead class="bg-gray-200">
              <tr>
                <th class="border border-gray-300 p-2">High School</th>
                <th class="border border-gray-300 p-2">Visits</th>
                <th class="border border-gray-300 p-2">Loyalty Level</th>
                <th class="border border-gray-300 p-2">Students Sent to Bilkent</th>
                <th class="border border-gray-300 p-2">YKS Average</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="school in sortedHighSchools"
                :key="school.highSchool"
                :class="{
                  'bg-green-50': school.studentsToBilkent > 30,
                  'bg-yellow-50': school.studentsToBilkent  > 14 && school.studentsToBilkent <= 30,
                  'bg-red-50': school.studentsToBilkent <= 14,
                }"
              >
                <td class="border border-gray-300 p-2">{{ school.highSchool }}</td>
                <td class="border border-gray-300 p-2">{{ school.visitsToBilkent }}</td>
                <td class="border border-gray-300 p-2">
                  {{
                    school.studentsToBilkent > 30
                      ? "High Loyalty"
                      : school.studentsToBilkent > 14
                      ? "Medium Loyalty"
                      : "Low Loyalty"
                  }}
                </td>
                <td class="border border-gray-300 p-2">{{ school.studentsToBilkent }}</td>
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
  
  const highSchoolStore = useHighSchoolStore();
  const { highSchools } = highSchoolStore;
  
  // Sort high schools by YKS average in descending order
  const sortedHighSchools = computed(() =>
    [...highSchools].sort((a, b) => b.yksAverage - a.yksAverage)
  );
  </script>
  
  <style scoped>
  /* Ensure scrollable container respects its parent dimensions */
  .bg-white {
    max-height: 100%;
  }
  </style>
  