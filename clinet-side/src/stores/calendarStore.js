// stores/calendarStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCalendarStore = defineStore("calendar", () => {
  const currentDate = ref(new Date());
  const viewMode = ref("month");

  // Change to the next day
  const nextDay = () => {
    currentDate.value = new Date(
      currentDate.value.setDate(currentDate.value.getDate() + 1)
    );
  };

  // Change to the previous day
  const previousDay = () => {
    currentDate.value = new Date(
      currentDate.value.setDate(currentDate.value.getDate() - 1)
    );
  };

  // Set the view mode
  const setViewMode = (mode) => {
    viewMode.value = mode;
  };

  // Set the current date (for month navigation)
  const setCurrentDate = (date) => {
    currentDate.value = date;
  };

  return {
    currentDate,
    viewMode,
    nextDay,
    previousDay,
    setViewMode,
    setCurrentDate, 
  };
});
