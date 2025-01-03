import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import regRequestController from "@/controllers/regRequestController.js";

export const useRegRequestStore = defineStore("regRequestStore", () => {
    const registrationRequests = ref([]);
    const isLoaded = ref(false);
    const authStore = useAuthStore();

    // Fetch Registration Requests
    const fetchRegRequests = async () => {
        if (!authStore.user.id) {
            console.error("User ID is not available.");
            return;
        }

        try {
            let response;
            if (authStore.userRole === "secretary") 
                response = await regRequestController.getRegRequests();

            registrationRequests.value = response?.data.map((data) => ({
                id: data.id,
                name: data.name,
                email: data.email,
                phoneNo: data.phone_no,
                userType: data.user_type,
                highSchoolName: data.high_school_name,
                city: data.city,
                submittedAt: data.submitted_at,
            }));
            isLoaded.value = true;
        } catch (error) {
            console.error("Failed to fetch reg requests:", error.response?.data || error.message);
            isLoaded.value = false;
        }
    };

    // Approve Registration Request
    const approveRegRequest = async (id) => {
        try {
            console.log(`Approving registration request with ID: ${id}`); // Debug Log
            const response = await regRequestController.approveRegRequest(id);
            console.log("Approve Response:", response); // Debug Log

            // Remove the approved request from the list
            registrationRequests.value = registrationRequests.value.filter(
                (request) => request.id !== id
            );
        } catch (error) {
            console.error("Error approving registration request:", error.response?.data || error.message);
            throw error; // Optionally rethrow the error
        }
    };

    const rejectRegRequest = async (id, data) => {
        try {
          console.log(`Rejecting registration request with ID: ${id}`); // Debug Log
      
          const response = await regRequestController.rejectRegRequest(id, data);
      
          // Safely log and return the backend response
          console.log("Backend Response:", response.data.message);
          console.log("Rejection Reason:", response.data.reason);
      
          // Remove the rejected request from the list
          registrationRequests.value = registrationRequests.value.filter(
            (request) => request.id !== id
          );
      
          return response; // Return the response object
        } catch (error) {
          console.error("Error rejecting registration request:", error.response?.data || error.message);
          alert("Failed to reject the request. Please try again.");
          throw error; // Re-throw the error to propagate it
        }
      };
      
    
    

    return {
        registrationRequests,
        isLoaded,
        fetchRegRequests,
        approveRegRequest,
        rejectRegRequest,
    };
});
