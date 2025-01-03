// controllers/tourController.js
import apiClient from "@/services/APIClient";

const tourController = {
  getTours: () => apiClient.get("/api/tour/"),
  getToursByGuide: (guideId) => apiClient.get(`/api/tour/guide-tours/${guideId}/`),
  getToursByAdvisor: (advisorId) => apiClient.get(`/api/tour/advisor-tours/${advisorId}/`),
  createTour: (data) => apiClient.post("/api/tour/", data),
  getTourById: (id) => apiClient.get(`/api/tour/${id}/`),
  updateTour: (id, data) => apiClient.put(`/api/tour/${id}/`, data),
  partialUpdateTour: (id, data) => apiClient.patch(`/api/tour/${id}/`, data),
  deleteTour: (id) => apiClient.delete(`/api/tour/${id}/`),
  rejectTour: (id, guideId) => apiClient.post(`/api/tour/${id}/reject/`, { guide_id: guideId }),
  getCompletedTours: (id) => apiClient.get(`/api/tour/${id}/completed-tours-of-advisor/`),
  getReviewOfTour: (tourId) => apiClient.get(`/api/tour/${tourId}/get-review/`),
  createReviewOfTour: (tourId, data) => apiClient.post(`/api/tour/${tourId}/post-review/`, data),
  getToursByVisitor: (id) => apiClient.get(`/api/tour/visitor-tours/${id}/`),
};

export default tourController;
