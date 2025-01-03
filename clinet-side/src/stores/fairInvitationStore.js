import { defineStore } from "pinia";
import { ref } from "vue";
import fairController from "@/controllers/fairController.js";

export const useFairRequestStore = defineStore("fairInvitationStore", () => {
  const invitations = ref([]);

  const createFairInvitation = async (data) => {
    try {
      const response = await fairController.sendFairRequest(data);
      invitations.value.push(response.data); // Add the new invitation to the store
      return response.data;
    } catch (error) {
      console.error("Failed to create fair invitation:", error.response?.data || error.message);
      throw error;
    }
  };

  const fetchFairInvitations = async () => {
    try {
      const response = await fairController.getFairRequests();
      invitations.value = response.data;
    } catch (error) {
      console.error("Failed to fetch fair invitations:", error.response?.data || error.message);
    }
  };

  return {
    invitations,
    createFairInvitation,
    fetchFairInvitations,
  };
});
