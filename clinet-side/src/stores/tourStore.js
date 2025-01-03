// stores/tourStore.js
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "@/stores/authStore";
import tourController from "@/controllers/tourController.js";
import reviewController from "@/controllers/reviewController.js";

export const useTourStore = defineStore("tourStore", () => {
  const tours = ref([]);
  const isLoaded = ref(false);
  const authStore = useAuthStore();

  // Fetch tours based on user role
  const fetchTours = async () => {

    if (!authStore.user.id) {
      console.error("User ID is not available.");
      return;
    }

    try {
      let response;
      switch (authStore.userRole) {
        case "guide":
          response = await tourController.getToursByGuide(authStore.user.profile_id);
          break;
        case "advisor":
          response = await tourController.getToursByAdvisor(authStore.user.profile_id);
          break;
        case "coordinator":
          response = await tourController.getTours();
          break;
        case "visitor":
          response = await tourController.getToursByVisitor(authStore.user.profile_id);
          break;
        default:
          console.warn("Unsupported role for fetching tours.");
          tours.value = [];
          return;
      }

      tours.value = response.data;
      console.log(tours.value);
      isLoaded.value = true;
    } catch (error) {
      console.error("Failed to fetch tours:", error.response?.data || error.message);
      isLoaded.value = false;
    }
  };

  // Get tours filtered by date
  const getToursOnDate = (date) => {
    const formattedDate = date.toISOString().split("T")[0];
    return tours.value.filter((tour) => tour.date === formattedDate).sort((a, b) => a.id - b.id);
  };

  // Get a single tour by ID
  const getTourById = (id) => {
    return tours.value.find((tour) => tour.id === id);
  };

  // Update a specific tour
  const updateTour = async (tour) => {
    const id = tour.id;
    delete tour.id; // Remove the ID before sending the payload
    try {
      await tourController.updateTour(id, tour);
      console.log("Tour updated successfully.");
      await fetchTours(); // Refresh the tours
    } catch (error) {
      console.error("Error updating tour:", error.response?.data || error.message);
    }
  };

  // Clear all tours (useful for logout or switching users)
  const clearTours = () => {
    tours.value = [];
    isLoaded.value = false;
  };

  const handleRejectTour = async (tour) => {
    const timeLeft = (new Date(tour.date) - new Date()) / (1000 * 60 * 60 * 24);
    if (timeLeft >= 14) {
      try {
        await tourController.rejectTour(tour.id, authStore.user.profile_id);
        // Re-fetch tours or update local state
        await fetchTours();
        console.log(`Tour ${tour.id} rejected and set to unassigned.`);
      } catch (error) {
        console.error("Failed to reject tour:", error.response?.data || error.message);
      }
    }
  };

  const getCompletedTours = async () => {
    try {
      const response = await tourController.getCompletedTours(authStore.user.profile_id);
      console.log(response.data)
      tours.value = response.data;
    } catch (error) {
      console.error(error.message);
    }
  }

  const getReviewOfTour = async (tourId) => {
    try {
      const response = await tourController.getReviewOfTour(tourId);
      return response.data;
    } catch (error) {
      console.error(error.message);
    }
  }

  const createReviewOfTour = async (tourId, data) => {
    try {
      console.log(tourId, data);
      data["tour_id"] = tourId;
      const response = await reviewController.postReview(tourId, data);
      return response.data;
    } catch (error) {
      console.error(error.message);
    }
  }

  const createTour = async (tour) => {
    try {
      await tourController.createTour(tour);
      console.log("Tour created successfully.");
      await fetchTours();
    } catch (error) {
      console.error("Error creating tour:", error.response?.data || error.message);
    }
  }

  return { tours, fetchTours, getToursOnDate, getTourById, updateTour, clearTours, handleRejectTour, isLoaded, getCompletedTours, getReviewOfTour, createReviewOfTour, createTour };
});
