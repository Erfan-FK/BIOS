<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useTourRequestStore } from "@/stores/tourRequestsStore";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { storeToRefs } from "pinia";
import { toast } from "vue-sonner";

const tourRequestStore = useTourRequestStore();

onMounted(async () => {
  try {
    await tourRequestStore.fetchPendingTourRequestBatches();
  } catch (error) {
    console.error("Error fetching tour requests:", error);
    toast.error("Failed to fetch tour requests.");
  }
});

const { tourRequestBatches } = storeToRefs(tourRequestStore);

const searchQuery = ref("");
const selectedFilter = ref("All");

watch(selectedFilter, () => {
  searchQuery.value = "";
});

const filteredRequests = computed(() => {
  return tourRequestBatches.value.filter((request) => {
    const matchesSearch =
        searchQuery.value === "" ||
        request.schoolName.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesFilter =
        selectedFilter.value === "All" || request.type === selectedFilter.value;
    const isPending = request.status === "pending";
    return matchesSearch && matchesFilter && isPending;
  });
});

const isViewModalOpen = ref(false);
const isRejectModalOpen = ref(false);
const isApproveModalOpen = ref(false);

const selectedRequest = ref(null);
const rejectionReason = ref("");
const requestToApprove = ref(null); 
const isProcessing = ref(false); 

const openViewModal = (request) => {
  selectedRequest.value = request;
  isViewModalOpen.value = true;
};

const openRejectModal = (request) => {
  selectedRequest.value = request;
  isRejectModalOpen.value = true;
};

const openApproveModal = (request) => { 
  requestToApprove.value = request;
  isApproveModalOpen.value = true;
};

const determineTypeString = (type) => {
  switch (type) {
    case "high-school":
      return "High School";
    case "individual":
      return "Individual";
    default:
      return "Unknown";
  }
};

const approveRequest = async () => {
  if (isProcessing.value || !requestToApprove.value) return;
  isProcessing.value = true;
  try {
    await tourRequestStore.approveTourRequest(requestToApprove.value.id);
    await tourRequestStore.fetchPendingTourRequestBatches();
    toast.success("Tour request approved successfully!");
    isApproveModalOpen.value = false;
    requestToApprove.value = null;
  } catch (error) {
    console.error("Error approving tour request:", error);
    toast.error("Failed to approve tour request.");
  } finally {
    isProcessing.value = false;
  }
};

const rejectRequest = async () => {
  if (isProcessing.value) return; // Prevent multiple clicks
  if (selectedRequest.value) {
    if (!rejectionReason.value.trim()) {
      toast.error("Rejection reason cannot be empty.");
      return;
    }
    isProcessing.value = true;
    try {
      await tourRequestStore.removeTourRequest(
          selectedRequest.value.id,
          rejectionReason.value
      );
      // await tourRequestStore.fetchTourRequestBatches();
      toast.success("Tour request rejected successfully!");
      rejectionReason.value = "";
      isRejectModalOpen.value = false;
      selectedRequest.value = null;
    } catch (error) {
      console.error("Error rejecting tour request:", error);
      toast.error("Failed to reject tour request.");
    } finally {
      isProcessing.value = false;
    }
  }
};

const closeModals = () => {
  isViewModalOpen.value = false;
  isRejectModalOpen.value = false;
  isApproveModalOpen.value = false; // Close approve modal if open
  requestToApprove.value = null;
};
</script>

<template>
  <!-- Fixed height container -->
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <!-- Header with filter dropdown and search -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Requested Tours</h2>
        <p class="text-md text-gray-600 mt-2">
          Manage and review tour requests.
        </p>
      </div>

      <div class="flex items-center gap-4">
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by School Name"
            class="w-[250px] p-2 border border-gray-300 rounded-lg"
        />
        <Select v-model="selectedFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="Filter" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Filter Options</SelectLabel>
              <SelectItem value="All">All Tours</SelectItem>
              <SelectItem value="High School">High School</SelectItem>
              <SelectItem value="Individual">Individual</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Table displaying tour requests -->
    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">#</TableHead>
            <TableHead class="font-bold text-red-700">Applicant Name</TableHead>
            <TableHead class="font-bold text-red-700">School Name</TableHead>
            <TableHead class="font-bold text-red-700">Date Range</TableHead>
            <TableHead class="font-bold text-red-700">Visitor Count</TableHead>
            <TableHead class="font-bold text-red-700">Type</TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow
              v-for="(request, index) in filteredRequests"
              :key="request.id"
          >
            <TableCell>{{ index + 1 }}</TableCell>
            <TableCell>{{ request.visitor.user.name }}</TableCell>
            <TableCell>{{ request.visitor.highSchoolName }}</TableCell>
            <TableCell>{{ request.dateRange }}</TableCell>
            <TableCell class="text-center">{{ request.visitorCount }}</TableCell>
            <TableCell>{{ determineTypeString(request.visitor.type) }}</TableCell>
            <TableCell class="text-right">
              <Button
                  variant="primary"
                  class="bg-blue-600 text-white hover:bg-blue-700 mr-2"
                  @click="openViewModal(request)"
              >
                View
              </Button>
              <Button
                  variant="success"
                  class="bg-green-600 text-white hover:bg-green-700 mr-2"
                  @click="openApproveModal(request)"
              :disabled="isProcessing"
              >
              Approve
              </Button>
              <Button
                  variant="destructive"
                  class="bg-red-600 text-white hover:bg-red-700"
                  @click="openRejectModal(request)"
                  :disabled="isProcessing"
              >
                Reject
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>

  <!-- View Modal -->
  <div
      v-if="isViewModalOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Tour Request Details</h2>
      <p><strong>Applicant Name:</strong> {{ selectedRequest?.visitor.user.name }}</p>
      <p><strong>School Name:</strong> {{ selectedRequest?.visitor.highSchoolName }}</p>
      <p><strong>Email:</strong> {{ selectedRequest?.visitor.user.email }}</p>
      <p><strong>Date Range:</strong> {{ selectedRequest?.dateRange }}</p>
      <p><strong>Visitor Count:</strong> {{ selectedRequest?.visitorCount }}</p>
      <p><strong>Type:</strong> {{ determineTypeString(selectedRequest?.visitor.type) }}</p>
      <p><strong>Additional Requests:</strong> {{ selectedRequest?.additionalRequests }}</p>
      <Button variant="secondary" class="mt-4" @click="closeModals">Close</Button>
    </div>
  </div>

  <!-- Reject Modal -->
  <transition name="fade">
    <div
        v-if="isRejectModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
        <h2 class="text-xl font-bold mb-4">Reject Tour Request</h2>
        <p><strong>Applicant Name:</strong> {{ selectedRequest?.visitor.user.name }}</p>
        <textarea
            v-model="rejectionReason"
            placeholder="Enter the reason for rejection"
            class="w-full border border-gray-300 rounded-lg p-2 mt-4"
            rows="4"
        ></textarea>
        <div class="flex justify-end space-x-4 mt-4">
          <Button variant="secondary" @click="closeModals">Cancel</Button>
          <Button
              variant="destructive"
              @click="rejectRequest"
              :disabled="isProcessing"
          >
            Submit
          </Button>
        </div>
      </div>
    </div>
  </transition>


  <!-- Approve Confirmation Modal -->
  <transition name="fade">
    <div
        v-if="isApproveModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-1/3">
        <h2 class="text-xl font-bold mb-4">Confirm Approval</h2>
        <p>Are you sure you want to approve the tour request from <strong>{{ requestToApprove?.visitor.user.name }}</strong> of <strong>{{ requestToApprove?.schoolName }}</strong>?</p>
        <div class="flex justify-end space-x-4 mt-6">
          <Button variant="secondary" @click="closeModals">Cancel</Button>
          <Button
              variant="default"
              @click="approveRequest"
              :disabled="isProcessing"
          >
            Confirm
          </Button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
/* Add custom styles if needed */
</style>
