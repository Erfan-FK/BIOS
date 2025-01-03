import { defineStore } from "pinia";
import { ref } from "vue";
import guideController from "@/controllers/guideController";
import { useAuthStore } from "@/stores/authStore";

export const useAvailabilityScheduleStore = defineStore("availability", () => {
  const selectedSlots = ref([]);
  const authStore = useAuthStore();

  // Updated daysOfWeek to start from Monday
  const daysOfWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
  const timeSlots = [
    "9:00 am - 11:00 am",
    "11:00 am - 1:00 pm",
    "1:30 pm - 4:00 pm",
    "4:00 pm - 5:30 pm",
  ];

  const fetchAvailability = async () => {
    if (!authStore.user.profile_id) return;

    const response = await guideController.getGuideAvailability(authStore.user.profile_id);
    const availabilityArray = response.data; // Array of 28 ints (0 or 1)

    selectedSlots.value = []; // Clear current slots

    for (let index = 0; index < availabilityArray.length; index++) {
      if (availabilityArray[index] === 1) {
        const dayIndex = Math.floor(index / 4);
        const slotIndex = index % 4;
        const day = daysOfWeek[dayIndex];
        const slot = timeSlots[slotIndex];
        selectedSlots.value.push({ day, timeSlot: slot });
      }
    }
  };

  const toggleAvailability = async (day, timeSlot) => {
    if (!authStore.user.profile_id) return;

    const existingIndex = selectedSlots.value.findIndex(
      (slot) => slot.day === day && slot.timeSlot === timeSlot
    );

    const dayIndex = daysOfWeek.indexOf(day);
    const slotIndex = timeSlots.indexOf(timeSlot);
    const index = dayIndex * 4 + slotIndex;

    if (existingIndex === -1) {
      // Slot not available, so add it
      await guideController.addAvailability(authStore.user.profile_id, dayIndex, slotIndex);
      selectedSlots.value.push({ day, timeSlot });
    } else {
      // Slot currently available, so remove it
      await guideController.removeAvailability(authStore.user.profile_id, dayIndex, slotIndex);
      selectedSlots.value.splice(existingIndex, 1);
    }
  };

  const updateSlotAvailability = async (sourceDay, sourceTimeSlot, targetDay, targetTimeSlot) => {
    if (!authStore.user.profile_id) return;
  
    const sourceDayIndex = daysOfWeek.indexOf(sourceDay);
    const sourceSlotIndex = timeSlots.indexOf(sourceTimeSlot);
    const targetDayIndex = daysOfWeek.indexOf(targetDay);
    const targetSlotIndex = timeSlots.indexOf(targetTimeSlot);
  
    try {
      const response = await guideController.updateAvailability(
        authStore.user.profile_id,
        sourceDayIndex,
        sourceSlotIndex,
        targetDayIndex,
        targetSlotIndex
      );
  
      const sourceIndexInSelected = selectedSlots.value.findIndex(
        (slot) => slot.day === sourceDay && slot.timeSlot === sourceTimeSlot
      );
      if (sourceIndexInSelected !== -1) {
        selectedSlots.value.splice(sourceIndexInSelected, 1); // Remove source slot
      }
      selectedSlots.value.push({ day: targetDay, timeSlot: targetTimeSlot }); // Add target slot
    } catch (error) {
      console.error("Error updating slot availability:", error);
    }
  };

  const isAvailable = (day, timeSlot) => {
    return selectedSlots.value.some(
      (slot) => slot.day === day && slot.timeSlot === timeSlot
    );
  };

  return { selectedSlots, toggleAvailability, isAvailable, fetchAvailability, updateSlotAvailability };
});