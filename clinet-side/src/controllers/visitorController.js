import apiClient from '@/services/APIClient';

const visitorController = {
    getVisitors: () => apiClient.get('/api/visitor/'),
    createVisitor: (data) => apiClient.post('/api/visitor/', data),
    getVisitorById: (id) => apiClient.get(`/api/visitor/${id}/`),
    updateVisitor: (id, data) => apiClient.put(`/api/visitor/${id}/`, data),
    partialUpdateVisitor: (id, data) => apiClient.patch(`/api/visitor/${id}/`, data),
    deleteVisitor: (id) => apiClient.delete(`/api/visitor/${id}/`),
    getTourRequestBatches: (id) => apiClient.get(`/api/visitor/${id}/tour-request-batches/`),
};

export default visitorController;
