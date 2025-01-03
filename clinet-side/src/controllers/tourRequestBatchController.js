import apiClient from '@/services/APIClient';

const tourRequestBatchController = {
    getTourRequestBatches: () => apiClient.get('/api/tour_request_batch/'),
    createTourRequestBatch: (data) => apiClient.post('/api/tour_request_batch/', data),
    getTourRequestBatchById: (id) => apiClient.get(`/api/tour_request_batch/${id}/`),
    updateTourRequestBatch: (id, data) => apiClient.put(`/api/tour_request_batch/${id}/`, data),
    partialUpdateTourRequestBatch: (id, data) => apiClient.patch(`/api/tour_request_batch/${id}/`, data),
    deleteTourRequestBatch: (id) => apiClient.delete(`/api/tour_request_batch/${id}/`),
    createTourRequestsBatch: (data) => apiClient.post(`/api/tour_request_batch/create-with-requests/`, data),
    scheduleTourRequestBatch: (id,data) => apiClient.post(`/api/tour_request_batch/${id}/schedule/`, data),
    getTourRequestBatchOfTour: (id) => apiClient.get(`/api/tour_request_batch/by-tour/${id}/`, id),
    getTourApprovedRequestBatches: () => apiClient.get('/api/tour_request_batch/approved/'),
    getTourPendingRequestBatches: () => apiClient.get('/api/tour_request_batch/pending/'),
};

export default tourRequestBatchController;
