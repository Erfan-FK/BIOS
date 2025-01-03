<script setup>
import { ref, computed, watch, onMounted } from "vue";
import {
  Table,
  TableBody,
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
import { useRegRequestStore } from "@/stores/regRequestStore.js";
import { storeToRefs } from "pinia";
import { toast } from "vue-sonner";

const regRequestStore = useRegRequestStore();

onMounted(async () => {
  await regRequestStore.fetchRegRequests();
});

const { registrationRequests } = storeToRefs(regRequestStore);

const searchQuery = ref("");
const selectedFilter = ref("All");

watch(selectedFilter, () => {
  searchQuery.value = "";
});

const filteredRequests = computed(() => {
  return registrationRequests.value.filter((request) => {
    const matchesSearch =
      searchQuery.value === "" ||
      request.highSchoolName?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesFilter =
      selectedFilter.value === "All" || request.userType === selectedFilter.value;
    return matchesSearch && matchesFilter;
  });
});

const isViewModalOpen = ref(false);
const isRejectModalOpen = ref(false);

const selectedRequest = ref(null);
const rejectionReason = ref("");

const openViewModal = (request) => {
  selectedRequest.value = request;
  isViewModalOpen.value = true;
};

const openRejectModal = (request) => {
  selectedRequest.value = request;
  isRejectModalOpen.value = true;
};

const approveRequest = async (id) => {
  try {
    await regRequestStore.approveRegRequest(id);
    registrationRequests.value = registrationRequests.value.filter(
      (request) => request.id !== id
    );
    toast.success("Request approved successfully!");
  } catch (error) {
    console.error("Failed to approve request:", error.response?.data || error.message);
  }
};

const rejectRequest = async () => {
  try {
    if (!rejectionReason.value) {
      return toast.error("Please enter a reason for rejection.");
    }
    
    const response = await regRequestStore.rejectRegRequest(selectedRequest.value.id, {
      reason: rejectionReason.value,
    });

    registrationRequests.value = registrationRequests.value.filter(
      (request) => request.id !== selectedRequest.value.id
    );

    rejectionReason.value = "";
    isRejectModalOpen.value = false;

    toast.success("Request rejected successfully!");
  } catch (error) {
    console.error("Failed to reject request:", error.response?.data || error.message);
  }
};


const closeModals = () => {
  isViewModalOpen.value = false;
  isRejectModalOpen.value = false;
};
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Registration Requests</h2>
        <p class="text-md text-gray-600 mt-2">Manage and review registration requests.</p>
      </div>

      <div class="flex items-center gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by High School"
          class="w-[250px] p-2 border border-gray-300 rounded-lg"
        />
        <Select v-model="selectedFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="Filter" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Filter Options</SelectLabel>
              <SelectItem value="All">All Types</SelectItem>
              <SelectItem value="individual">Individual Student</SelectItem>
              <SelectItem value="high_school_counsellor">High School Counsellor</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>

    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">#</TableHead>
            <TableHead class="font-bold text-red-700">Name</TableHead>
            <TableHead class="font-bold text-red-700">City</TableHead>
            <TableHead class="font-bold text-red-700">High School</TableHead>
            <TableHead class="font-bold text-red-700">Email</TableHead>
            <TableHead class="font-bold text-red-700">Type</TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(request, index) in filteredRequests" :key="request.id">
            <TableCell>{{ index + 1 }}</TableCell>
            <TableCell>{{ request.name }}</TableCell>
            <TableCell>{{ request.city }}</TableCell>
            <TableCell>{{ request.highSchoolName || "N/A" }}</TableCell>
            <TableCell>{{ request.email }}</TableCell>
            <TableCell>{{ request.userType === 'high_school_counsellor' ? 'High School Councellor' : "Individual" }}</TableCell>
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
                @click="approveRequest(request.id)"
              >
                Approve
              </Button>
              <Button
                variant="destructive"
                class="bg-red-600 text-white hover:bg-red-700"
                @click="openRejectModal(request)"
              >
                Reject
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>

  <div
    v-if="isViewModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Registration Request Details</h2>
      <p><strong>Name:</strong> {{ selectedRequest?.name }}</p>
      <p><strong>City:</strong> {{ selectedRequest?.city }}</p>
      <p><strong>High School:</strong> {{ selectedRequest?.highSchoolName || "N/A" }}</p>
      <p><strong>Email:</strong> {{ selectedRequest?.email }}</p>
      <p><strong>Phone:</strong> {{ selectedRequest?.phoneNo }}</p>
      <p><strong>Type:</strong> {{ selectedRequest?.userType }}</p>
      <p><strong>Submitted At:</strong> {{ selectedRequest?.submittedAt }}</p>
      <Button variant="secondary" class="mt-4" @click="closeModals">Close</Button>
    </div>
  </div>

  <div
    v-if="isRejectModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Reject Registration Request</h2>
      <p><strong>Name:</strong> {{ selectedRequest?.name }}</p>
      <textarea
        v-model="rejectionReason"
        placeholder="Enter the reason for rejection"
        class="w-full border border-gray-300 rounded-lg p-2 mt-4"
        rows="4"
      ></textarea>
      <div class="flex justify-end space-x-4 mt-4">
        <Button variant="secondary" @click="closeModals">Cancel</Button>
        <Button variant="destructive" @click="rejectRequest">Submit</Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>
