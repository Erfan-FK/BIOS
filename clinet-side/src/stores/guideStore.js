import { defineStore } from "pinia";
import { ref } from "vue";
import  guideController from "@/controllers/guideController";

export const useGuideStore = defineStore("guideProfile", () => {

  const guides = ref([]);
  
  const fetchGuides = async () => {
    try {
      const response = await guideController.getGuides();
      guides.value = response.data;
    } catch (error) {
      console.error("Failed to fetch guides:", error);
      throw error;
    }
  }

  const getGuidesByIds = async (guideIds) => {
    try {
      const response = await guideController.getGuidesbyIdList(guideIds);
      return response.data;
    } catch (error) {
      console.error("Failed to fetch guides by IDs:", error);
      throw error;
    }
  }

  const getGuides = async () => {
    try {
      const response = await guideController.getGuides();
      guides.value = response.data;
    } catch (error) {
      console.error("Failed to fetch guides:", error);
      throw error;
    }
  }
  
  return {
    getGuidesByIds, fetchGuides, getGuides, guides
  };
});
