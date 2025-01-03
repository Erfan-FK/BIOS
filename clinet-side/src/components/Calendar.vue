<script setup>
import Button from "./ui/button/Button.vue";
import { useTourStore } from "../stores/tourStore";
import { useCalendarStore } from "../stores/calendarStore";

import { ChevronRight, ChevronLeft, ChevronDown } from "lucide-vue-next";
import { ref, computed, onMounted } from "vue";

const tourStore = useTourStore();
onMounted(() => {
  tourStore.fetchTours();
});
const calendarStore = useCalendarStore();
const isViewMenuOpen = ref(false);
const hoveredTour = ref(null);
const tooltipPosition = ref({ x: 0, y: 0 });

const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

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

const toggleViewMenu = () => {
  isViewMenuOpen.value = !isViewMenuOpen.value;
};

const selectView = (mode) => {
  calendarStore.setViewMode(mode); // Change the view mode
  isViewMenuOpen.value = false;   // Close the menu
};

const nextDay = () => {
  calendarStore.nextDay();
};

const previousDay = () => {
  calendarStore.previousDay();
};

const isIndividualTour = (tour) => {
  return tour.guestType === "Individual";
};
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

const getToursForDate = (date) => {
  return tourStore.tours.filter((tour) => {
    return new Date(tour.date).toDateString() === date.toDateString();
  });
};

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

const showTourDetails = (tour) => {
  hoveredTour.value = tour;
};

const hideTourDetails = () => {
  hoveredTour.value = null;
};

onMounted(() => {
  document.addEventListener("mousemove", (event) => {
    tooltipPosition.value = { x: event.pageX + 10, y: event.pageY + 10 };
  });
});

const getToursForDateAndSlot = (date, slotId) => {
    return tourStore.tours.filter((tour) => {
        const tourDate = new Date(tour.date).toISOString().split("T")[0]; 
        const compareDate = date.toISOString().split("T")[0]; 
        return (
            tourDate === compareDate && tour.time_slot_id === slotId
        );
    });
};
</script>

<template>
  <div class="w-full h-full rounded-lg bg-white">
    <!-- Heading and Description -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Schedule</h2>
        <p class="text-md text-gray-600 mt-2">
          View and manage your upcoming tours and availability
        </p>
      </div>
    </div>

    <!-- Header -->
    <div class="p-6" >
      <div class="flex justify-between items-center bg-gray-100 p-4 rounded-t-lg">
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
          <!-- View Switcher -->
          <div class="relative">
            <div
              @click="toggleViewMenu"
              class="flex items-center bg-white rounded-lg border-solid border border-gray-300"
            >
              <Button class="px-4 py-1 text-black font-bold" variant="ghost">
                {{ viewModeLabel }}
                <ChevronDown />
              </Button>
            </div>

            <div
              v-if="isViewMenuOpen"
              class="absolute z-50 top-10 right-0 left-0 bg-white border rounded shadow text-gray-600"
            >
              <ul>
                <li>
                  <button
                    @click="selectView('week')"
                    class="w-full text-left px-4 py-2 hover:bg-gray-200"
                  >
                    Week View
                  </button>
                </li>
                <li>
                  <button
                    @click="selectView('month')"
                    class="w-full text-left px-4 py-2 hover:bg-gray-200"
                  >
                    Month View
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Calendar Views -->
      <div class="bg-gray-100">
        <!-- Month View -->
        <div v-if="calendarStore.viewMode === 'month'">
          <div class="grid grid-cols-7">
            <!-- Days of the Week -->
            <div
              v-for="day in daysOfWeek"
              :key="day"
              class="text-center text-s font-bold text-gray-800 border p-2 bg-white"
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

              <!-- Tours with Limited Slots -->
              <div
                v-for="tour in getToursForDate(date).slice(0,1)"
                :key="tour.id"
                :class="[' mt-1 text-xs text-white p-1 rounded', isIndividualTour(tour) ? 'bg-blue-500' : 'bg-green-500']"
                @mouseover="showTourDetails(tour)"
                @mouseleave="hideTourDetails"
              >
              {{ tour.visitor.highSchoolName || "Individual Visitor" }} - {{ tour.slot }}
              </div>

              <!-- Overflow Indicator if More than 2 Tours -->
              <div
                v-if="getToursForDate(date).length > 1"
                class="text-xs text-gray-500 mt-2"
              >
                +{{ getToursForDate(date).length - 1 }} more
              </div>
            </div>
          </div>
        </div>

        <!-- Week View -->
        <div v-if="calendarStore.viewMode === 'week'">
          <!-- Week Days Header -->
          <div class="grid grid-cols-8">
            <!-- Empty cell for Time Slot labels -->
            <div class="p-2"></div>
            <!-- Dates of the Week -->
            <div
              v-for="date in weekDates"
              :key="date.toDateString()"
              :class="[
                'text-center p-2 border font-bold',
                isToday(date) ? 'bg-red-600 text-white border-red-600' : '',
                isCurrentDay(date) && !isToday(date)
                  ? 'bg-purple-600 text-white border-purple-600'
                  : '', !isToday(date) && !isCurrentDay(date) ? 'bg-white' : '',
              ]"
            >
              {{ daysOfWeek[date.getDay()] }} {{ date.getDate() }}
            </div>
          </div>

          <!-- Time Slots and Tours -->
          <div class="grid grid-cols-8">
            <!-- Time Slot Labels -->
            <div class="grid grid-rows-4 bg-white">
              <div class="p-2 border h-28 flex items-center justify-center font-bold">
                9:00 am - 11:00 am
              </div>
              <div class="p-2 border h-28 flex items-center justify-center font-bold">
                11:00 am - 1:00 pm
              </div>
              <div class="p-2 border h-28 flex items-center justify-center font-bold">
                1:30 pm - 4:00 pm
              </div>
              <div class="p-2 border h-28 flex items-center justify-center font-bold">
                4:00 pm - 5:30 pm
              </div>
            </div>

            <!-- Week Days with Time Slots -->
            <div
              v-for="date in weekDates"
              :key="date.toDateString()"
              class="grid grid-rows-4"
            >
              <!-- Time Slots for Each Day -->
              <div
                v-for="slotId in ['0', '1', '2', '3']" 
                :key="slotId"
                class="p-2 border h-28 relative"
                :class="[
                  isToday(date) ? 'bg-red-50 text-white' : '',
                  isCurrentDay(date) && !isToday(date)
                    ? 'bg-purple-50 text-white'
                    : '', !isToday(date) && !isCurrentDay(date) ? 'bg-white' : '',
                ]"
              >
                <!-- Tours -->
                <div
                  v-for="tour in getToursForDateAndSlot(date, slotId)"
                  :key="tour.id"
                  :class="[
                    'text-sm text-white p-1 rounded absolute inset-0 m-1', isIndividualTour(tour) ? 'bg-blue-500' : 'bg-green-500',
                  ]"
                  @mouseover="showTourDetails(tour)"
                  @mouseleave="hideTourDetails"
                >
                {{ tour.visitor.highSchoolName || "Individual Visitor" }} - {{ tour.slot }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Tooltip -->
    <div
      v-if="hoveredTour"
      class="absolute bg-white border p-4 rounded shadow-lg"
      :style="{ top: tooltipPosition.y + 'px', left: tooltipPosition.x + 'px' }"
    >
      <h3 class="text-lg font-bold">
        {{ hoveredTour.visitor.highSchoolName || "Individual Visitor" }}
      </h3>
      <p>Contact: {{ hoveredTour.visitor.contactNumber }}</p>
      <p>Type: {{ hoveredTour.visitor.type }}</p>
      <p>Slot: {{ hoveredTour.slot }}</p>
      <p>Date: {{ hoveredTour.date }}</p>
    </div>
  </div>
</template>
