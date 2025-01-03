<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useFairStore } from "@/stores/fairStore";
import Button from "@/components/ui/button/Button.vue";
import { useCalendarStore } from "@/stores/calendarStore";
import { ChevronRight, ChevronLeft } from "lucide-vue-next";

// Initialize Fair Store and fetch fairs on mount
const fairStore = useFairStore();
onMounted(() => {
  fairStore.fetchFairs();
});

// Initialize Calendar Store
const calendarStore = useCalendarStore();

// State for View Menu and Tooltip
const isViewMenuOpen = ref(false);
const hoveredFair = ref(null); // For single fair tooltip
const hoveredFairs = ref([]);  // For multiple fairs tooltip
const tooltipPosition = ref({ x: 0, y: 0 });

// Days of the Week Labels
const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

// Computed Properties for Displaying Month and View Mode
const formattedMonthYear = computed(() => {
  const options = { month: "long", year: "numeric" };
  return calendarStore.currentDate.toLocaleDateString(undefined, options);
});

const viewModeLabel = computed(() => {
  return (
    calendarStore.viewMode.charAt(0).toUpperCase() +
    calendarStore.viewMode.slice(1) +
    " View"
  );
});

// Methods to Toggle View Menu and Navigate Dates
const toggleViewMenu = () => {
  isViewMenuOpen.value = !isViewMenuOpen.value;
};

const nextDay = () => {
  calendarStore.nextDay();
};

const previousDay = () => {
  calendarStore.previousDay();
};

// Computed Properties for Month and Week Dates
const monthDates = computed(() => {
  const dates = [];
  const date = new Date(
    calendarStore.currentDate.getFullYear(),
    calendarStore.currentDate.getMonth(),
    1
  );
  while (date.getMonth() === calendarStore.currentDate.getMonth()) {
    dates.push(new Date(date));
    date.setDate(date.getDate() + 1);
  }
  return dates;
});

const weekDates = computed(() => {
  const dates = [];
  const currentDate = new Date(calendarStore.currentDate);
  const dayOfWeek = currentDate.getDay(); // 0 (Sun) - 6 (Sat)
  const firstDayOfWeek = new Date(currentDate);
  firstDayOfWeek.setDate(currentDate.getDate() - dayOfWeek);

  for (let i = 0; i < 7; i++) {
    const date = new Date(firstDayOfWeek);
    date.setDate(firstDayOfWeek.getDate() + i);
    dates.push(date);
  }
  return dates;
});

// Function to Retrieve Approved Fairs for a Specific Date
const getFairsForDate = (date) => {
  return fairStore.fairs.filter((fair) => {
    return (
      fair.status === "approved" &&
      new Date(fair.date).toDateString() === date.toDateString()
    );
  });
};

// Utility Functions to Check Date States
const isToday = (date) => {
  const today = new Date();
  return (
    date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
  );
};

const isCurrentDay = (date) => {
  return date.toDateString() === calendarStore.currentDate.toDateString();
};

// Methods to Show and Hide Fair Details in Tooltip
const showFairDetails = (fair) => {
  hoveredFair.value = fair;
};

const hideFairDetails = () => {
  hoveredFair.value = null;
};

const showAdditionalFairs = (fairs) => {
  hoveredFairs.value = fairs;
};

const hideAdditionalFairs = () => {
  hoveredFairs.value = [];
};

// Update Tooltip Position on Mouse Move
const updateTooltipPosition = (event) => {
  // Use clientX and clientY for viewport-relative positioning
  const offsetX = 15; // Adjusted offset for better placement
  const offsetY = 15;
  
  // Ensure the tooltip doesn't go off the right or bottom edge of the viewport
  const tooltipWidth = 300; // Approximate width of the tooltip
  const tooltipHeight = hoveredFair.value || hoveredFairs.value.length > 0 ? 150 : 0; // Approximate height

  let x = event.clientX + offsetX;
  let y = event.clientY + offsetY;

  if (x + tooltipWidth > window.innerWidth) {
    x = event.clientX - tooltipWidth - offsetX;
  }

  if (y + tooltipHeight > window.innerHeight) {
    y = event.clientY - tooltipHeight - offsetY;
  }

  tooltipPosition.value = { x, y };
};

onMounted(() => {
  document.addEventListener("mousemove", updateTooltipPosition);
});

onBeforeUnmount(() => {
  document.removeEventListener("mousemove", updateTooltipPosition);
});
</script>

<template>
  <div class="w-full h-full rounded-lg bg-white relative">
    <!-- Heading and Description -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Schedule</h2>
        <p class="text-md text-gray-600 mt-2">
          View upcoming fairs you are scheduled to attend.
        </p>
      </div>
    </div>

    <!-- Header -->
    <div class="p-6">
      <div
        class="flex justify-between items-center bg-gray-100 p-4 rounded-t-lg"
      >
        <div>
          <h2 class="text-2xl font-bold">{{ formattedMonthYear }}</h2>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Navigation Buttons -->
          <div
            class="flex items-center bg-white rounded-lg border-solid border border-gray-300"
          >
            <Button
              @click="previousDay"
              class="px-2 py-1 text-gray-600"
              variant="ghost"
            >
              <ChevronLeft />
            </Button>
            <span class="px-4 py-1 text-black font-bold">
              {{
                calendarStore.currentDate.toLocaleDateString(undefined, {
                  weekday: "short",
                  day: "numeric",
                })
              }}
            </span>
            <Button
              @click="nextDay"
              class="px-2 py-1 text-gray-600"
              variant="ghost"
            >
              <ChevronRight />
            </Button>
          </div>
        </div>
      </div>

      <!-- Calendar Views -->
      <div class="bg-gray-100">
        <!-- Month View -->
        <div class="grid grid-cols-7">
          <!-- Days of the Week -->
          <div
            v-for="day in daysOfWeek"
            :key="day"
            class="text-center text-sm font-bold text-gray-800 border p-2 bg-white"
          >
            {{ day }}
          </div>
          <!-- Dates -->
          <div
            v-for="date in monthDates"
            :key="date.toDateString()"
            class="border h-24 p-2 relative bg-white"
          >
            <!-- Date Number with Highlight -->
            <div class="w-full h-8">
              <div
                :class="[
                  'absolute top-2 font-semibold left-2 text-xs h-6 w-6 flex items-center justify-center',
                  isToday(date)
                    ? 'bg-red-600 text-white rounded-full'
                    : 'bg-gray-200 rounded-full',
                  isCurrentDay(date) && !isToday(date)
                    ? 'bg-purple-600 text-white rounded-full'
                    : 'bg-gray-200 rounded-full',
                ]"
              >
                {{ date.getDate() }}
              </div>
            </div>

            <!-- Fairs for the Date -->
            <div
              v-for="(fair) in getFairsForDate(date).slice(0, 1)"
              :key="fair.id"
              class="mt-1 text-xs text-white p-1 rounded bg-blue-500 cursor-pointer"
              @mouseover="showFairDetails(fair)"
              @mouseleave="hideFairDetails"
            >
              {{ fair.visitor.highSchoolName || "Individual Visitor" }} -
              {{ fair.explanation }}
            </div>

            <!-- Overflow Indicator if More than 1 Fair -->
            <div
              v-if="getFairsForDate(date).length > 1"
              class="text-xs text-gray-500 mt-2 cursor-pointer"
              @mouseover="showAdditionalFairs(getFairsForDate(date).slice(1))"
              @mouseleave="hideAdditionalFairs"
            >
              +{{ getFairsForDate(date).length - 1 }} more
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tooltip for Single Fair Details -->
    <div
      v-if="hoveredFair"
      class="fixed bg-white border p-4 rounded shadow-lg z-50 pointer-events-none"
      :style="{ top: tooltipPosition.y + 'px', left: tooltipPosition.x + 'px', maxWidth: '300px' }"
    >
      <h3 class="text-lg font-bold">
        {{ hoveredFair.visitor.highSchoolName || "Individual Visitor" }}
      </h3>
      <p><strong>Contact:</strong> {{ hoveredFair.visitor.contactNumber }}</p>
      <p><strong>Date:</strong> {{ new Date(hoveredFair.date).toLocaleDateString() }}</p>
      <p><strong>Status:</strong> {{ hoveredFair.status }}</p>
      <p><strong>Explanation:</strong> {{ hoveredFair.explanation }}</p>
    </div>

    <!-- Tooltip for Multiple Fairs Details -->
    <div
      v-if="hoveredFairs.length > 0"
      class="fixed bg-white border p-4 rounded shadow-lg z-50 pointer-events-none"
      :style="{ top: tooltipPosition.y + 'px', left: tooltipPosition.x + 'px', maxWidth: '300px' }"
    >
      <h3 class="text-lg font-bold">Additional Fairs</h3>
      <div v-for="fair in hoveredFairs" :key="fair.id" class="mt-2">
        <h4 class="text-md font-semibold">
          {{ fair.visitor.highSchoolName || "Individual Visitor" }}
        </h4>
        <p><strong>Contact:</strong> {{ fair.visitor.contactNumber }}</p>
        <p><strong>Date:</strong> {{ new Date(fair.date).toLocaleDateString() }}</p>
        <p><strong>Status:</strong> {{ fair.status }}</p>
        <p><strong>Explanation:</strong> {{ fair.explanation }}</p>
        <hr class="my-2" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Optional: Add any component-specific styles here */

/* Optional: Prevent text selection inside tooltips */
.tooltip-content {
  user-select: none;
}
</style>
