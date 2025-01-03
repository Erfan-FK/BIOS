import apiClient from "@/services/APIClient";

const tourReportController = {
    postTourReport: (data) => apiClient.post("/api/tour_report/", data),
    getReportByTourId: (id) => apiClient.get(`/api/tour_report/by-tour/${id}/`),
};

export default tourReportController;
