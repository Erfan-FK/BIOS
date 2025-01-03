import { defineStore } from "pinia";
import { ref } from "vue";
import {useAuthStore} from './authStore';
import fairController from "@/controllers/fairController";

export const useFairStore = defineStore("fair", () => {
  const fairs = ref([]);
  const authStore = useAuthStore();


  const fetchFairs = async () => {
    try {
      const response = await fairController.getFairs();
      fairs.value = response.data;
    } catch (err) {
      console.error("Error fetching fairs:", err);
    }
  };

  const createFairRequest = async (data) => {
  const requestBody = {
    status : 'pending',
    date : data.date,
    visitor: authStore.user.profile_id,
    explanation: data.explanation,
  }
  await fairController.sendFairRequest(requestBody);
  }


  const approveFairRequest = async (id) => {
    try {
      await fairController.approveFairRequest(id);
      const fair = fairs.value.find((fair) => fair.id === id);
      if (fair) fair.status = "approved";
    } catch (err) {
      console.error("Error approving fair request:", err);
      throw err;
    }
  };

  const rejectFairRequest = async (id, reason) => {
    try {
      await fairController.rejectFairRequest(id, { reason });
      const fair = fairs.value.find((fair) => fair.id === id);
      if (fair) fair.status = "rejected";
    } catch (err) {
      console.error("Error rejecting fair request:", err);
      throw err;
    }
  };

  return {
    fairs,
    fetchFairs,
    createFairRequest,
    approveFairRequest,
    rejectFairRequest,
  };
});
