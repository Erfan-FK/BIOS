<script setup>
import { ref, computed, onMounted } from "vue";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectTrigger, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectValue } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useTourRequestStore } from "@/stores/tourRequestsStore.js";
import { storeToRefs } from "pinia";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { toast } from "vue-sonner";

const tourRequestStore = useTourRequestStore();
const { tourRequestBatches } = storeToRefs(tourRequestStore);

onMounted(async () => {
  await tourRequestStore.fetchTourBatchesOfVisitor();
});

const expandedBatchId = ref(null);
const selectedStatus = ref("all"); // Default filter: show all

const toggleDetails = (batchId) => {
  if (expandedBatchId.value === batchId) {
    expandedBatchId.value = null;
  } else {
    expandedBatchId.value = batchId;
  }
};

const closeDetails = () => {
  expandedBatchId.value = null;
};

const getExpandedBatch = computed(() => {
  return tourRequestBatches.value.find((batch) => batch.id === expandedBatchId.value) || null;
});

const getDateRange = (requests) => {
  if (!requests || requests.length === 0) return "N/A";
  const dates = requests.map((request) => new Date(request.date));
  const minDate = new Date(Math.min(...dates));
  const maxDate = new Date(Math.max(...dates));
  return `${minDate.toISOString().split("T")[0]} - ${maxDate.toISOString().split("T")[0]}`;
};

// Sort batches by the latest date in tourRequests
const sortedTourBatches = computed(() => {
  return [...tourRequestBatches.value].sort((a, b) => {
    const latestDateA = Math.max(...a.tourRequests.map((req) => new Date(req.date).getTime()));
    const latestDateB = Math.max(...b.tourRequests.map((req) => new Date(req.date).getTime()));
    return latestDateB - latestDateA; // Sort descending
  });
});

// Filter batches by selected status
const filteredTourBatches = computed(() => {
  if (selectedStatus.value === "all") {
    return sortedTourBatches.value;
  }
  return sortedTourBatches.value.filter((batch) => batch.status === selectedStatus.value);
});

// Confirmation Dialog State
const confirmDialog = ref({
  visible: false,
  title: '',
  message: '',
  batch: null,
});

// Loading State
const isRejecting = ref(false);

// Open Confirmation Dialog
const openConfirmDialog = (batch) => {
  confirmDialog.value = {
    visible: true,
    title: 'Reject Tour Request',
    message: 'Are you sure you want to reject this tour request?',
    batch: batch,
  };
};

// Close Confirmation Dialog
const closeConfirmDialog = () => {
  confirmDialog.value = {
    visible: false,
    title: '',
    message: '',
    batch: null,
  };
};

// Handle Confirm Rejection
const handleConfirmReject = async () => {
  if (!confirmDialog.value.batch) {
    toast.error("No batch selected for rejection.");
    closeConfirmDialog();
    return;
  }

  isRejecting.value = true;

  try {
    await tourRequestStore.rejectTourRequestBatch(confirmDialog.value.batch);
    // No need to show another toast here as the store already does
  } catch (error) {
    // The store handles the error toast
  } finally {
    isRejecting.value = false;
    closeConfirmDialog();
  }
};

// Reject Tour Request Batch
const rejectTourRequestBatch = async (batch) => {
  openConfirmDialog(batch);
};
</script>

<template>
  <section class="flex justify-center items-start mt-12 relative">
    <div class="bg-white px-8 py-6 rounded-lg shadow-xl border border-gray-200 w-full max-w-4xl">
      <!-- Heading -->
      <div class="text-center mb-6">
        <h2 class="text-3xl font-bold">
          Track <span class="text-red-600">Tours</span>
        </h2>
        <p class="text-gray-600 mt-2 text-sm">
          Monitor the status of your tour requests below.
        </p>
      </div>

      <!-- Filter Dropdown -->
      <div class="flex justify-end mb-6">
        <Select v-model="selectedStatus">
          <SelectTrigger class="w-[150px]">
            <SelectValue placeholder="Filter by Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Filter by Status</SelectLabel>
              <SelectItem value="all">All</SelectItem>
              <SelectItem value="pending">Pending</SelectItem>
              <SelectItem value="approved">Approved</SelectItem>
              <SelectItem value="rejected">Rejected</SelectItem>
              <SelectItem value="scheduled">Scheduled</SelectItem>
              <SelectItem value="cancelled">Cancelled</SelectItem> <!-- Added 'cancelled' option -->
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>

      <!-- Tour Requests Table -->
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">Date Range</TableHead>
            <TableHead class="font-bold text-red-700">Status</TableHead>
            <TableHead class="font-bold text-red-700">Number of Visitors</TableHead>
            <TableHead class="font-bold text-red-700">Notes</TableHead>
            <TableHead class="font-bold text-red-700">Rejection Note</TableHead>
            <TableHead class="font-bold text-red-700">Actions</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          <TableRow v-for="batch in filteredTourBatches" :key="batch.id">
            <TableCell class="font-bold">{{ getDateRange(batch.tourRequests) }}</TableCell>
            <TableCell>
              <span
                class="capitalize font-bold px-2 py-1 rounded"
                :class="{
                  'bg-yellow-100 text-yellow-700': batch.status === 'pending',
                  'bg-green-100 text-green-700': batch.status === 'approved',
                  'bg-red-100 text-red-700': batch.status === 'rejected',
                  'bg-blue-100 text-blue-700': batch.status === 'scheduled',
                  'bg-gray-100 text-gray-700': batch.status === 'cancelled', // Added style for 'cancelled'
                }"
              >
                {{ batch.status }}
              </span>
            </TableCell>
            <TableCell class="text-center">{{ batch.numberOfVisitors }}</TableCell>
            <TableCell>{{ batch.additionalNotes || "" }}</TableCell>
            <TableCell>{{ batch.rejectionReason || "" }}</TableCell>
            <TableCell>
              <!-- Scheduled Batches: Display Scheduled Info and Reject Button -->
              <div v-if="batch.status === 'scheduled'" class="flex flex-row items-center space-x-2">
                <p class="text-blue-600 font-bold text-center">
                  {{ batch.scheduledDate }}
                </p>
                <p class="text-blue-600 font-bold text-center">
                  {{ batch.scheduledTimeSlot }}
                </p>
                <!-- Reject Button -->
                <Button
                  variant="destructive"
                  class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                  @click="rejectTourRequestBatch(batch)"
                  :disabled="isRejecting"
                >
                  <span v-if="isRejecting">Rejecting...</span>
                  <span v-else>Reject</span>
                </Button>
              </div>

              <!-- Non-Scheduled Batches: Display View Details and Reject Button -->
              <div v-else class="flex flex-row items-center space-x-2">
                <Button
                  variant="outline"
                  class="text-blue-600 border-blue-600 hover:bg-blue-100"
                  @click="toggleDetails(batch.id)"
                >
                  View Details
                </Button>
                <!-- Reject Button: Only Show if Status is Not 'rejected' or 'cancelled' -->
                <Button
                  v-if="!['rejected', 'cancelled'].includes(batch.status)"
                  variant="destructive"
                  class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                  @click="rejectTourRequestBatch(batch)"
                  :disabled="isRejecting"
                >
                  <span v-if="isRejecting">Rejecting...</span>
                  <span v-else>Reject</span>
                </Button>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Confirmation Dialog -->
    <Dialog v-model:open="confirmDialog.visible">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{{ confirmDialog.title }}</DialogTitle>
        </DialogHeader>
        <p class="text-sm text-gray-600">
          {{ confirmDialog.message }}
        </p>
        <DialogFooter class="space-x-4">
          <Button
            variant="secondary"
            class="bg-gray-500 hover:bg-gray-600 text-white"
            @click="closeConfirmDialog"
            :disabled="isRejecting"
          >
            Cancel
          </Button>
          <Button
            variant="destructive"
            class="bg-red-500 hover:bg-red-600 text-white"
            @click="handleConfirmReject"
            :disabled="isRejecting"
          >
            <span v-if="isRejecting">Rejecting...</span>
            <span v-else>Reject</span>
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Details Modal -->
    <transition name="fade">
      <div
        v-if="expandedBatchId"
        class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50"
      >
        <div class="bg-white p-6 rounded-lg shadow-lg w-96">
          <h4 class="font-bold text-lg text-gray-800 mb-4">Requested Tours</h4>
          <ul class="list-disc pl-5 mb-4">
            <li
              v-for="request in getExpandedBatch?.tourRequests || []"
              :key="request.id"
            >
              {{ request.date }} - {{ request.time_slot }}
            </li>
          </ul>
          <Button
            class="bg-red-600 text-white hover:bg-red-700 w-full"
            @click="closeDetails"
          >
            Close
          </Button>
        </div>
      </div>
    </transition>
  </section>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
