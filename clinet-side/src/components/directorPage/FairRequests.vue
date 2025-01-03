<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { useFairStore } from "@/stores/fairStore";
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

const fairStore = useFairStore();


const { fairs } = storeToRefs(fairStore);

onMounted(async() => {
  await fairStore.fetchFairs();
});
const searchQuery = ref("");

const filteredFairs = computed(() => {
  return fairs.value.filter((fair) => {
    const matchesSearch =
      searchQuery.value === "" ||
      fair?.visitor?.highSchoolName?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const isPending = fair.status === "pending";
    return matchesSearch && isPending;
  });
});

const isViewModalOpen = ref(false);
const isRejectModalOpen = ref(false);

const selectedFair = ref(null);
const rejectionReason = ref("");

const openViewModal = (fair) => {
  selectedFair.value = fair;
  console.log(selectedFair.value);
  isViewModalOpen.value = true;
};

const openRejectModal = (fair) => {
  selectedFair.value = fair;
  isRejectModalOpen.value = true;
};

const approveFair = (id) => {
  fairStore.approveFairRequest(id);
};

const rejectFair = async () => {
  if (selectedFair.value) {
    await fairStore.rejectFair(selectedFair.value.id, rejectionReason.value);
    await fairStore.fetchFairs();
    rejectionReason.value = "";
    isRejectModalOpen.value = false;
  }
};

const closeModals = () => {
  isViewModalOpen.value = false;
  isRejectModalOpen.value = false;
};
</script>

<template>
  <!-- Fixed height container -->
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <!-- Header with filter dropdown and search -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Requested Fairs</h2>
        <p class="text-md text-gray-600 mt-2">
          Manage and review fair requests.
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
              <SelectItem value="All">All Fairs</SelectItem>
              <SelectItem value="pending">Pending Fairs</SelectItem>
              <SelectItem value="rejected">Rejected Fairs</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Table displaying fair requests -->
    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">#</TableHead>
            <TableHead class="font-bold text-red-700">Applicant Name</TableHead>
            <TableHead class="font-bold text-red-700">School Name</TableHead>
            <TableHead class="font-bold text-red-700 text-right">Phone Number</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow
            v-for="(fair, index) in filteredFairs"
            :key="fair.id"
          >
            <TableCell>{{ index + 1 }}</TableCell>
            <TableCell>{{ fair.visitor.user.name }}</TableCell>
            <TableCell>{{ fair.visitor.highSchoolName }}</TableCell>
            <TableCell class="text-right">{{ fair.visitor.contactNumber }}</TableCell>
            <TableCell class="text-right">
              <Button
                variant="primary"
                class="bg-blue-600 text-white hover:bg-blue-700 mr-2"
                @click="openViewModal(fair)"
              >
                View
              </Button>
              <Button
                variant="success"
                class="bg-green-600 text-white hover:bg-green-700 mr-2"
                @click="approveFair(fair.id)"
              >
                Approve
              </Button>
              <Button
                variant="destructive"
                class="bg-red-600 text-white hover:bg-red-700"
                @click="openRejectModal(fair)"
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
      <h2 class="text-xl font-bold mb-4">Fair Request Details</h2>
      <p><strong>Applicant Name:</strong> {{ selectedFair.visitor.user.name }}</p>
      <p><strong>School Name:</strong> {{ selectedFair.visitor.highSchoolName }}</p>
      <p><strong>Email:</strong> {{ selectedFair?.visitor.user.email }}</p>
      <Button variant="secondary" class="mt-4" @click="closeModals">Close</Button>
    </div>
  </div>

  <!-- Reject Modal -->
  <div
    v-if="isRejectModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Reject Fair Request</h2>
      <p><strong>Applicant Name:</strong> {{ selectedFair.visitor.user.name }}</p>
      <textarea
        v-model="rejectionReason"
        placeholder="Enter the reason for rejection"
        class="w-full border border-gray-300 rounded-lg p-2 mt-4"
        rows="4"
      ></textarea>
      <div class="flex justify-end space-x-4 mt-4">
        <Button variant="secondary" @click="closeModals">Cancel</Button>
        <Button variant="destructive" @click="rejectFair">Submit</Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>