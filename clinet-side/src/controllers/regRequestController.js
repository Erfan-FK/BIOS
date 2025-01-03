import apiClient from "@/services/APIClient.js";

const regRequestController = {
    getRegRequests: () => apiClient.get('/api/reg_request/'),
    createRegRequest: (data) => apiClient.post('/api/reg_request/', data),
    getRegRequestById: (id) => apiClient.get(`/api/reg_request/${id}/`),
    updateRegRequest: (id, data) => apiClient.put(`/api/reg_request/${id}/`, data),
    partialUpdateRegRequest: (id, data) => apiClient.patch(`/api/reg_request/${id}/`, data),
    deleteRegRequest: (id) => apiClient.delete(`/api/reg_request/${id}/`),
    approveRegRequest: (id) => apiClient.post(`/api/reg_request/${id}/approve/`),
    rejectRegRequest: (id, data) => apiClient.post(`/api/reg_request/${id}/reject/`, data), 
};

export default regRequestController;