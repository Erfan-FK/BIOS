<script setup>
import { ref } from "vue";
import { toast } from "vue-sonner";
import { useAdvisorStore } from "@/stores/advisorStore.js";

// Mock data for coordinator metrics (all black and white)
const metrics = ref([
  {
    title: "Total Visitors",
    value: 1200,
    color: "bg-white",
    textColor: "text-black",
    borderColor: "border-black",
  },
  {
    title: "Waiting Requests",
    value: 18,
    color: "bg-white",
    textColor: "text-black",
    borderColor: "border-black",
  },
  {
    title: "Rejected Requests",
    value: 5,
    color: "bg-white",
    textColor: "text-black",
    borderColor: "border-black",
  },
  {
    title: "Total Guides",
    value: 45,
    color: "bg-white",
    textColor: "text-black",
    borderColor: "border-black",
  },
  {
    title: "Tours Completed",
    value: 320,
    color: "bg-white",
    textColor: "text-black",
    borderColor: "border-black",
  },
  {
    title: "Total High Schools",
    value: 35,
    color: "bg-white",
    textColor: "text-black",
    borderColor: "border-black",
  },
]);

// Mock guide ratings data (20 guides)
const guides = ref([
  { id: 1, name: "John Doe", rating: 4.8 },
  { id: 2, name: "Jane Smith", rating: 4.5 },
  { id: 3, name: "Robert Johnson", rating: 4.2 },
  { id: 4, name: "Emily Davis", rating: 4.9 },
  { id: 5, name: "Michael Brown", rating: 3.8 },
  { id: 6, name: "Chris Taylor", rating: 3.0 },
  { id: 7, name: "Anna Lee", rating: 2.5 },
  { id: 8, name: "David Wilson", rating: 4.3 },
  { id: 9, name: "Sarah Lewis", rating: 4.6 },
  { id: 10, name: "James Walker", rating: 3.9 },
  { id: 11, name: "Linda Young", rating: 2.8 },
  { id: 12, name: "Paul Harris", rating: 4.7 },
  { id: 13, name: "Laura Hall", rating: 4.4 },
  { id: 14, name: "Brian Scott", rating: 3.6 },
  { id: 15, name: "Karen Nelson", rating: 4.0 },
  { id: 16, name: "Nancy King", rating: 4.8 },
  { id: 17, name: "Mark Allen", rating: 3.2 },
  { id: 18, name: "Lisa Wright", rating: 4.1 },
  { id: 19, name: "Steven Hill", rating: 3.4 },
  { id: 20, name: "Jessica Green", rating: 2.7 },
]);

// Function to get row color based on rating
const getRowColor = (rating) => {
  if (rating > 4.5) return "bg-green-100";
  if (rating >= 3 && rating <= 4.5) return "bg-green-50";
  return "bg-yellow-100";
};

// Access the advisorStore
const advisorStore = useAdvisorStore();

// Function for "Get Working Hours" button
const getWorkingHours = async () => {
  try {
    const data = await advisorStore.sendWorkingHours();
    if (data) {
      toast.success("Working hours sent successfully!");
    } else {
      toast.error("No working hours found.");
    }
  } catch (error) {
    toast.error("Failed to fetch working hours.", {
      description: "Please try again later.",
    });
  }
};
</script>

<template>
  <div class="h-screen overflow-y-auto bg-gray-50 p-6">
    <!-- Page Title -->
    <h1 class="text-3xl font-bold text-center mb-6 text-gray-800">
      Coordinator Data Overview
    </h1>

    <!-- Metrics Cards Section -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div
        v-for="(metric, index) in metrics"
        :key="index"
        class="rounded-lg shadow-lg p-6 text-center transition-transform transform hover:scale-105 border"
        :class="[metric.color, metric.borderColor]"
      >
        <div :class="metric.textColor + ' text-lg font-semibold mb-2'">
          {{ metric.title }}
        </div>
        <div :class="metric.textColor + ' text-4xl font-bold'">
          {{ metric.value }}
        </div>
      </div>
    </div>

    <!-- Button to fetch working hours -->
    <div class="flex justify-center mb-8">
      <button
        @click="getWorkingHours"
        class="bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg shadow-lg transition-transform transform hover:scale-105"
      >
        Get Working Hours
      </button>
    </div>

    <!-- Guide Ratings Table -->
    <div class="bg-white shadow-md rounded-lg p-6 border border-gray-200">
      <h2 class="text-2xl font-semibold mb-4 text-gray-700 text-center">
        Guide Ratings
      </h2>
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-100">
            <th class="p-4 text-left border-b">ID</th>
            <th class="p-4 text-left border-b">Guide Name</th>
            <th class="p-4 text-left border-b">Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="guide in guides"
            :key="guide.id"
            :class="getRowColor(guide.rating)"
          >
            <td class="p-4">{{ guide.id }}</td>
            <td class="p-4">{{ guide.name }}</td>
            <td class="p-4">{{ guide.rating }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Add hover effect for rows */
tr:hover {
  background-color: rgba(0, 0, 0, 0.05); 
}
</style>
