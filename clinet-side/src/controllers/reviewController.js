import apiClient from "@/services/APIClient";

const reviewController = {
  getGuideReviews: (guideId) => apiClient.get(`/api/reviews/guide/${guideId}/`),
  postReview: (id, data) => apiClient.post(`/api/tour/${id}/post-review/`, data),
};

export default reviewController;
