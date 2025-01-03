import { defineStore } from "pinia";
import tourReportController from "@/controllers/tourReportController";
import { useAuthStore } from "@/stores/authStore";

export const useTourReportStore = defineStore("tourReport", () => {
    const createReport = async (report, finishedAtHour, finishedAtMinute, tour) => {
        const authStore = useAuthStore();
        const guide = authStore.user.profile_id;
        const data = {
            report,
            finishedAtHour,
            finishedAtMinute,
            tour,
            guide,
        }
        await tourReportController.postTourReport(data);
    };

    const getReportByTourId = async (tourId) => {
        try {
            const response = await tourReportController.getReportByTourId(tourId);
            return response.data;
        } catch (error) {
        }
    }

    return { createReport, getReportByTourId };
});
