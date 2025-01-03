import apiClient from '@/services/APIClient';

const tourRequestController = {
    getTourRequests: () => apiClient.get('/api/tour_request/'),
    createTourRequest: (data) => apiClient.post('/api/tour_request/', data),
    getTourRequestById: (id) => apiClient.get(`/api/tour_request/${id}/`),
    updateTourRequest: (id, data) => apiClient.put(`/api/tour_request/${id}/`, data),
    partialUpdateTourRequest: (id, data) => apiClient.patch(`/api/tour_request/${id}/`, data),
    deleteTourRequest: (id) => apiClient.delete(`/api/tour_request/${id}/`),
};

export default tourRequestController;
