import apiClient from '@/services/APIClient';

const guideController = {
    getGuides: () => apiClient.get('/api/guide/'),
    createGuide: (data) => apiClient.post('/api/guide/', data),
    getGuideById: (id) => apiClient.get(`/api/guide/${id}/`),
    updateGuide: (id, data) => apiClient.put(`/api/guide/${id}/`, data),
    partialUpdateGuide: (id, data) => apiClient.patch(`/api/guide/${id}/`, data),
    deleteGuide: (id) => apiClient.delete(`/api/guide/${id}/`),
    getGuidesAtDayAndSlot: (day, slot) => apiClient.get(`/api/guide/?day=${day}&slot=${slot}/available_guides/`),

    getGuideAvailability: (id) => apiClient.get(`/api/guide/${id}/available_slots/`),
    addAvailability: (id, day, slot) => apiClient.post(`/api/guide/${id}/add-availability/`, { day, slot }),
    removeAvailability: (id, day, slot) => apiClient.post(`/api/guide/${id}/remove-availability/`, { day, slot }),
    getGuidesAtDayAndSlot: (day, slot) => apiClient.get(`/api/guide/available_guides/?day=${day}&slot=${slot}`),
    updateAvailability: (id, sourceDay, sourceSlot, targetDay, targetSlot) =>
        apiClient.post(`/api/guide/${id}/update-availability/`, {
          source_day: sourceDay,
          source_slot: sourceSlot,
          target_day: targetDay,
          target_slot: targetSlot,
        }),
    getGuidesbyIdList: (idList) => apiClient.get(`/api/guide/guides-by-id-list/?guide_ids=${idList}`),

};

export default guideController;
