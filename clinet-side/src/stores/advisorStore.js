import { defineStore } from 'pinia';
import { ref } from 'vue';
import {useAuthStore} from './authStore';
import advisorController from "@/controllers/advisorController.js";

export const useAdvisorStore = defineStore('advisor', () => {
    const advisor = ref(null);
    const authStore = useAuthStore();


    const fetchAdvisor = async (advisorId) => {
        const response = await advisorController.getAdvisorById(advisorId);
        advisor.value = response.data;
    };

    const sendWorkingHours = async () => {
        try {
            const requestBody = {
                email: authStore.user.email,
      }
          const response = await advisorController.getWorkingHours(requestBody);
          return response.data;
        } catch (err) {
          console.error('Error fetching data:', err);
        }
    };
    return { advisor, fetchAdvisor, sendWorkingHours };
});
