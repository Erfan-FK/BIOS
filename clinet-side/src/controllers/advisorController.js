import apiClient from '@/services/APIClient';

const advisorController = {
    getAdvisors: () => apiClient.get('/api/advisor/'),
    createAdvisor: (advisorData) => apiClient.post('/api/advisor/', advisorData),
    getAdvisorById: (id) => apiClient.get(`/api/advisor/${id}/`),
    updateAdvisor: (id, advisorData) => apiClient.put(`/api/advisor/${id}/`, advisorData),
    partialUpdateAdvisor: (id, advisorData) => apiClient.patch(`/api/advisor/${id}/`, advisorData),
    deleteAdvisor: (id) => apiClient.delete(`/api/advisor/${id}/`),
    getWorkingHours: (data) => apiClient.post(`/api/advisor/send-guide-report/`, data),
};

export default advisorController;
