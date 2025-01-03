import {defineStore} from "pinia";
import {ref} from "vue";
import guideController from "@/controllers/guideController.js";
import tourController from "@/controllers/tourController.js";

export const useGuidesStore = defineStore('guides', () => {
  const getGuideById = async (id) => {
    try {
      const response = await guideController.getGuideById(id);
      return response.data;
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  const getAvailableGuides = async (day, slot) => {
    try {
      const response = await guideController.getGuidesAtDayAndSlot(day, slot);
      return response.data;
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  }

  return { getGuideById, getAvailableGuides };
});