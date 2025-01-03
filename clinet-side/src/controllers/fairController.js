import apiClient from "@/services/APIClient.js";

const fairController = {
  getFairRequests: () => apiClient.get('/api/fair/'),
  sendFairRequest: (data) => apiClient.post('/api/fair/', data),
  approveFairRequest: (id) => apiClient.put(`/api/fair/${id}/approve/`),
  rejectFairRequest: (id, data) => apiClient.put(`/api/fair/${id}/reject/`, data),
  getFairs: () => apiClient.get('/api/fair/'),
};

export default fairController;