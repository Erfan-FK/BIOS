<script setup>
import { ref, computed, onMounted } from "vue";
import { useGuideStore } from "@/stores/guideStore";
import { useAdvisorStore } from "@/stores/advisorStore";
import { useAuthStore } from "@/stores/authStore";
import {ChevronLeft, ChevronRight, CheckCircle, Star, XCircle} from "lucide-vue-next";
import Button from "../ui/button/Button.vue";
import { storeToRefs } from "pinia";

const guideStore = useGuideStore();
const advisorStore = useAdvisorStore();
const authStore = useAuthStore();

const day = ref(0);
const { advisor } = storeToRefs(advisorStore);
const { guides } = storeToRefs(guideStore);

onMounted( async () => {
  await guideStore.getGuides();
  await advisorStore.fetchAdvisor(authStore.user.profile_id);
  day.value = advisor.value.authorizedDay[0];
});

const filteredGuideIndices = computed(() => {
  return guides.value.map((guide, index) => {
    return guide.availability[day.value * 4] || guide.availability[day.value * 4 + 1] || guide.availability[day.value * 4 + 2] || guide.availability[day.value * 4 + 3] ? index : -1;
  }).filter((index) => index !== -1);
});

const guideAvailabilities = computed(() => {
  return guides.value.map((guide) => {
    return guide.availability.slice(day.value * 4, day.value * 4 + 4);
  });
});

const previousDay = async() => {
  const authorizedDays = advisor.value.authorizedDay;
  const currentIndex = authorizedDays.indexOf(day.value);
  const previousIndex = (currentIndex - 1 + authorizedDays.length) % authorizedDays.length;
  day.value = authorizedDays[previousIndex];
  await guideStore.getGuides();
}

const nextDay = async () => {
  const authorizedDays = advisor.value.authorizedDay;
  const currentIndex = authorizedDays.indexOf(day.value);
  const nextIndex = (currentIndex + 1) % authorizedDays.length;
  day.value = authorizedDays[nextIndex];
  await guideStore.getGuides();
}

const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <!-- Header -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Guides  Availability Overview</h2>
        <p class="text-md text-gray-600 mt-2">
          View and manage guide availability by day and time slot.
        </p>
      </div>
      <div class="flex items-center">
        <div class="flex justify-between items-center w-64 bg-white rounded-lg border-solid border border-gray-300">
          <Button @click="previousDay" class="px-2 py-1 text-gray-600" variant="ghost">
            <ChevronLeft/>
          </Button>
          <span class="px-4 py-1 text-black font-bold">
            {{ daysOfWeek[day] }}
          </span>
          <Button @click="nextDay" class="px-2 py-1 text-gray-600" variant="ghost">
            <ChevronRight/>
          </Button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <table class="min-w-full border border-gray-200">
        <thead>
          <tr class="bg-gray-100 border-b">
            <th class="text-left font-bold text-red-700 p-4">#</th>
            <th class="text-left font-bold text-red-700 p-4">Name</th>
            <th class="text-center font-bold text-red-700 p-4">9:00 - 11:00</th>
            <th class="text-center font-bold text-red-700 p-4">11:00 - 13:00</th>
            <th class="text-center font-bold text-red-700 p-4">13:30 - 16:00</th>
            <th class="text-center font-bold text-red-700 p-4">16:00 - 17:30</th>
            <th class="text-center font-bold text-red-700 p-4">Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(guideIndex,index) in filteredGuideIndices"
            :key="guideIndex"
            class="border-b hover:bg-gray-50"
          >
            <td class="p-4">{{ index + 1 }}</td>
            <td class="p-4 flex items-center space-x-4">
              <img
                :src="guides[guideIndex].user.profile_picture"
                alt="Guide Profile"
                class="w-10 h-10 rounded-full border border-gray-300"
              />
              <span>{{ guides[guideIndex].name }}</span>
            </td>
            <td class="p-4 text-center" v-for="i in 4">
              <span class="relative group">
                <CheckCircle
                  v-if="guideAvailabilities[guideIndex][i-1]"
                  class="w-6 h-6 text-green-500 mx-auto"
                />
                <XCircle
                  v-else
                  class="w-6 h-6 text-red-500 mx-auto"
                />
                <div
                  class="absolute left-1/2 transform -translate-x-1/2 mt-2 hidden group-hover:block bg-black text-white text-sm rounded-md px-2 py-1 shadow-md"
                >
                  {{ guideAvailabilities[guideIndex][i] ? "Available" : "Unavailable" }}
                </div>
              </span>
            </td>
            <td class="p-4">
              <div class="flex w-full h-full justify-center">
                <span class="flex items-center space-x-1 ">
                  <span class="font-semibold text-gray-900">{{ guides[guideIndex].rating.toFixed(1) }}</span>
                  <Star class="w-5 h-5 text-yellow-400 fill-current" />
                </span>
                <span class="text-gray-500">({{ guides[guideIndex].reviewCount }} reviews)</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Tooltip Visibility */
.group-hover div {
  display: block !important;
}
</style>
