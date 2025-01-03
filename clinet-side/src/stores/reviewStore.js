import { defineStore } from "pinia";
import { ref } from "vue";
import reviewController from "@/controllers/reviewController";
import { useAuthStore } from "@/stores/authStore";

export const useReviewStore = defineStore("review", () => {
  const reviews = ref([]);

  // Fetch reviews for the current guide
  const fetchReviews = async () => {
    const authStore = useAuthStore();
    const guideId = authStore.user.profile_id;

    try {
      const response = await reviewController.getGuideReviews(guideId);
      reviews.value = response.data;
    } catch (error) {
      console.error("Failed to fetch reviews:", error);
    }
  };

  return { reviews, fetchReviews };
});
