<script setup>
import { ref, computed, onMounted } from "vue";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectValue,
  SelectLabel,
} from "@/components/ui/select";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { RangeCalendar } from "@/components/ui/range-calendar/index.js";
import { CalendarIcon } from "lucide-vue-next";
import { format } from "date-fns";
import { storeToRefs } from "pinia";
import { useGuideStore } from "@/stores/guideStore";
import { useTourRequestStore } from "@/stores/tourRequestsStore.js";
import { useTourStore } from "@/stores/tourStore.js";
import { useAdvisorStore } from "@/stores/advisorStore.js";
import { useAuthStore } from "@/stores/authStore.js";
import ScheduleModal from "./ScheduleModal.vue";

// Stores
const tourRequestStore = useTourRequestStore();
const guideStore = useGuideStore();
const advisorStore = useAdvisorStore();
const authStore = useAuthStore();

const { tourRequestBatches } = storeToRefs(tourRequestStore);
const { advisor } = storeToRefs(advisorStore);
const { user } = storeToRefs(authStore);

const searchQuery = ref("");
const selectedType = ref("All");
const dateRange = ref({ start: null, end: null });

onMounted(async () => {
  await tourRequestStore.fetchApprovedTourRequestBatches();
  await guideStore.fetchGuides();
  if (user.value?.profile_id) {
    await advisorStore.fetchAdvisor(user.value.profile_id);
  }
});

// Compute filtered tour requests
const filteredTourRequests = computed(() => {
  return tourRequestBatches.value.filter((tour) => {
    const matchesSearch =
        searchQuery.value === "" ||
        (tour.visitor.highSchoolName &&
            tour.visitor.highSchoolName.toLowerCase().includes(searchQuery.value.toLowerCase()));

    const matchesType =
        selectedType.value === "All" || tour.visitor.type === selectedType.value;

    const inDateRange =
        (!dateRange.value.start && !dateRange.value.end) ||
        (new Date(tour.date) >= dateRange.value.start &&
            new Date(tour.date) <= dateRange.value.end);

    const isApproved = tour.status === "approved";
    return matchesSearch && matchesType && inDateRange && isApproved;
  });
});

const isVisitorDetailsModalOpen = ref(false);
const isScheduleModalOpen = ref(false);
const selectedTourRequestBatch = ref(null);

const openVisitorDetailsModal = (tour) => {
  isVisitorDetailsModalOpen.value = true;
  selectedTourRequestBatch.value = tour;
};

const openScheduleModal = (tour) => {
  isScheduleModalOpen.value = true;
  selectedTourRequestBatch.value = tour;
};

const closeModals = async () => {
  isVisitorDetailsModalOpen.value = false;
  isScheduleModalOpen.value = false;
  selectedTourRequestBatch.value = null;
};
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Schedule Tours  </h2>
        <p class="text-md text-gray-600 mt-2">Schedule the certain dates and slots of tour requests.</p>
      </div>
      <div class="flex items-center gap-4">
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by High School"
            class="w-[300px] p-2 border border-gray-300 rounded-lg"
        />
        <Select v-model="selectedType">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="Filter by Visitor Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Filter by Visitor Type</SelectLabel>
              <SelectItem value="All">All</SelectItem>
              <SelectItem value="individual">Individual</SelectItem>
              <SelectItem value="high-school">High School</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>

        <Popover>
          <PopoverTrigger as-child>
            <Button variant="outline" class="w-[250px] h-10 text-left">
              <CalendarIcon class="mr-2" />
              {{ dateRange.start ? format(dateRange.start, "yyyy-MM-dd") : "Start Date" }} -
              {{ dateRange.end ? format(dateRange.end, "yyyy-MM-dd") : "End Date" }}
            </Button>
          </PopoverTrigger>
          <PopoverContent class="w-auto p-0">
            <RangeCalendar v-model="dateRange" class="rounded-md border" initial-focus />
          </PopoverContent>
        </Popover>
      </div>
    </div>

    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">#</TableHead>
            <TableHead class="font-bold text-red-700">Visitor Name</TableHead>
            <TableHead class="font-bold text-red-700">High School</TableHead>
            <TableHead class="font-bold text-red-700">Requested Date Range</TableHead>
            <TableHead class="font-bold text-red-700">Visitor Type</TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(tour, index) in filteredTourRequests" :key="tour.id">
            <TableCell>{{ index + 1 }}</TableCell>
            <TableCell>{{ tour.visitor.user.name }}</TableCell>
            <TableCell>{{ tour.visitor.highSchoolName }}</TableCell>
            <TableCell>{{ tour.dateRange }}</TableCell>
            <TableCell>{{ tour.visitor.type }}</TableCell>
            <TableCell class="flex space-x-2">
              <Button
                  variant="primary"
                  class="bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300"
                  @click="openVisitorDetailsModal(tour)"
              >
                Visitor Details
              </Button>
              <Button
                  variant="primary"
                  class="bg-blue-600 text-white hover:bg-blue-700"
                  @click="openScheduleModal(tour)"
              >
                Schedule Tour
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>

  <!-- Visitor Details Modal -->
  <div
      v-if="isVisitorDetailsModalOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Visitor Details</h2>
      <div v-if="selectedTourRequestBatch">
        <p><strong>Name:</strong> {{ selectedTourRequestBatch.visitor.user.name }}</p>
        <p><strong>Email:</strong> {{ selectedTourRequestBatch.visitor.user.email }}</p>
        <p><strong>Contact Number:</strong> {{ selectedTourRequestBatch.visitor.contactNumber }}</p>
      </div>
      <Button variant="secondary" class="mt-4" @click="closeModals">Close</Button>
    </div>
  </div>

  <!-- Schedule Modal Component -->
  <ScheduleModal
      :isOpen="isScheduleModalOpen"
      :selectedTourRequestBatch="selectedTourRequestBatch"
      @close="closeModals"
  />
</template>


<style scoped>
/* Add any component-specific styles here */
</style>
