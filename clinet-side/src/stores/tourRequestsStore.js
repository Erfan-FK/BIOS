// stores/tourRequestsStore.js
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "./authStore";
import tourRequestBatchController from "@/controllers/tourRequestBatchController";
import visitorController from "@/controllers/visitorController";
import tourController from "@/controllers/tourController"; // Added import
import { toast } from "vue-sonner"; // Ensure toast is imported

export const useTourRequestStore = defineStore("tourRequest", () => {
  const authStore = useAuthStore();

  const slots = ["09.00 AM", "11.00 AM", "13.30 PM", "16.00 PM"];

  const tourRequestBatches = ref([]);

  const addTourRequest = (tourRequest) => {
    tourRequestBatches.value.push({
      id: tourRequestBatches.value.length + 1,
      ...tourRequest,
    });
  };

  const removeTourRequest = (id, rejectionReason) => {
    const requestBody = {
      rejection_reason: rejectionReason,
      status: "rejected",
    };
    tourRequestBatches.value = tourRequestBatches.value.filter(
      (batch) => batch.id !== id
    );
    tourRequestBatchController.partialUpdateTourRequestBatch(id, requestBody);
  };

  const createTourRequests = async (form) => {
    const requestBody = {
      visitor_id: authStore.user.profile_id,
      dates: form.selectedSlots.map((slot) => slot.date),
      time_slots: form.selectedSlots.map((slot) => slots[slot.slot]),
      additional_notes: form.notes,
      number_of_visitors: form.numStudents,
    };

    await tourRequestBatchController.createTourRequestsBatch(requestBody);
  };


  const fetchTourRequestBatches = async () => {
    const response = await tourRequestBatchController.getTourRequestBatches();
    tourRequestBatches.value = response?.data.map((batch) => {
      return {
        id: batch.id,
        visitor: batch.visitor,
        dateRange: `${batch.tour_requests[0].date} - ${
          batch.tour_requests[batch.tour_requests.length - 1].date
        }`,
        tourRequests: batch.tour_requests,
        visitorCount: batch.number_of_visitors,
        additionalRequests: batch.additional_notes,
        status: batch.status,
      };
    });
  };
    const fetchPendingTourRequestBatches = async () => {
        const response = await tourRequestBatchController.getTourPendingRequestBatches();
        tourRequestBatches.value = response?.data.map((batch) => {
            return {
                id: batch.id,
                visitor: batch.visitor,
                dateRange: `${batch.tour_requests[0].date} - ${batch.tour_requests[batch.tour_requests.length - 1].date}`,
                tourRequests: batch.tour_requests,
                visitorCount: batch.number_of_visitors,
                additionalRequests: batch.additional_notes,
                status: batch.status,
            };
        });
    }

    const fetchApprovedTourRequestBatches = async () => {
        const response = await tourRequestBatchController.getTourApprovedRequestBatches();
        tourRequestBatches.value = response?.data.map((batch) => {
            return {
                id: batch.id,
                visitor: batch.visitor,
                dateRange: `${batch.tour_requests[0].date} - ${batch.tour_requests[batch.tour_requests.length - 1].date}`,
                tourRequests: batch.tour_requests,
                visitorCount: batch.number_of_visitors,
                additionalRequests: batch.additional_notes,
                status: batch.status,
            };
        });
    }
    
  const fetchTourBatchesOfVisitor = async () => {
    try {
      const response = await visitorController.getTourRequestBatches(
        authStore.user.profile_id
      );

      tourRequestBatches.value = response.data.map((batch) => {
        return {
          id: batch.id,
          status: batch.status,
          numberOfVisitors: batch.number_of_visitors,
          rejectionReason: batch.rejection_reason,
          additionalNotes: batch.additional_notes,
          scheduledDate: batch.tour?.date || null,
          scheduledTimeSlot: batch.tour ? slots[batch.tour.time_slot_id] : null,
          scheduledTourId: batch.tour?.id || null, // Include Tour ID
          tourRequests: batch.tour_requests,
        };
      });
    } catch (error) {
      console.error("Failed to fetch tour batches of visitor:", error);
      toast.error("Failed to fetch tour batches.");
    }
  };

  const approveTourRequest = async (id) => {
    const requestBody = {
      status: "approved",
    };
    await tourRequestBatchController.partialUpdateTourRequestBatch(
      id,
      requestBody
    );
  };

  const rejectTourRequestBatch = async (batch) => {
    try {
      if (batch.status === "scheduled" && batch.scheduledTourId) {
        // Delete the associated Tour object
        await tourController.deleteTour(batch.scheduledTourId);
        // Update the batch status to 'cancelled'
        await tourRequestBatchController.partialUpdateTourRequestBatch(
          batch.id,
          { status: "cancelled" } // Corrected status
        );
      } else if (["pending", "approved"].includes(batch.status)) {
        // Update the batch status to 'cancelled'
        await tourRequestBatchController.partialUpdateTourRequestBatch(
          batch.id,
          { status: "cancelled" } // Corrected status
        );
      } else {
        throw new Error("Cannot reject a batch with this status.");
      }
      toast.success("Tour request rejected successfully.");
      await fetchTourBatchesOfVisitor(); // Refresh the data
    } catch (error) {
      console.error("Failed to reject tour request:", error);
      toast.error("Failed to reject tour request.");
    }
  };

  const scheduleTourRequestBatch = async (id, tour) => {
    await tourRequestBatchController.scheduleTourRequestBatch(id, tour);
  };
    const getTourRequestBatchOfTour = async (tourId) => {
        const response = await tourRequestBatchController.getTourRequestBatchOfTour(tourId);
        const batch = response.data;
        console.log(batch)
        return {
            id: batch.id,
            visitor: batch.visitor,
            dateRange: `${batch.tour_requests[0].date} - ${batch.tour_requests[batch.tour_requests.length - 1].date}`,
            tourRequests: batch.tour_requests,
            visitorCount: batch.number_of_visitors,
            additionalRequests: batch.additional_notes,
            status: batch.status,
        };
    }

    return {
        tourRequestBatches,
        slots,
        addTourRequest,
        removeTourRequest,
        createTourRequests,
        fetchPendingTourRequestBatches,
        fetchTourRequestBatches,
        approveTourRequest,
        scheduleTourRequestBatch,
        fetchTourBatchesOfVisitor,
        getTourRequestBatchOfTour,
        fetchApprovedTourRequestBatches,
        rejectTourRequestBatch
    };
});