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
import { SelectLabel } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Select, SelectTrigger, SelectContent, SelectGroup, SelectItem, SelectValue } from "@/components/ui/select";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { RangeCalendar } from "@/components/ui/range-calendar/index.js";
import { CalendarIcon } from "lucide-vue-next";
import { format } from "date-fns";
import  { useTourStore } from "@/stores/tourStore";
import { storeToRefs } from "pinia";
import { useGuideStore } from "@/stores/guideStore";

const tourStore = useTourStore();
const guideStore = useGuideStore();
const { tours } = storeToRefs(tourStore);

onMounted(() => {
  tourStore.getCompletedTours();
  tours.value = tourStore.tours;
});

const searchQuery = ref("");
const selectedType = ref("All");
const dateRange = ref({ start: null, end: null }); 

const filteredTours = computed(() => {
  return tours?.value?.tours?.filter((tour) => {
    const matchesStatus = tour.status === "COMPLETED"; // Check if status is 'COMPLETED'
    const matchesSearch =
      searchQuery.value === "" ||
      (tour.visitor.highSchoolName &&
        tour.visitor.highSchoolName.toLowerCase().includes(searchQuery.value.toLowerCase()));
    const matchesType =
      selectedType.value === "All" || tour.visitor.type === selectedType.value;

    // Fixing the date range comparison
    const tourDate = new Date(tour.date); // Convert tour.date to Date object
    const matchesDateRange =
      (!dateRange.value.start && !dateRange.value.end) || // No range selected
      (dateRange.value.start && dateRange.value.end && // Both start and end selected
        tourDate >= new Date(dateRange.value.start) &&
        tourDate <= new Date(dateRange.value.end));

    return matchesStatus && matchesSearch && matchesType && matchesDateRange;
  });
});


const isReviewModalOpen = ref(false);
const isGuidesModalOpen = ref(false);

const selectedTour = ref(null);
const selectedTourGuides = ref([]);
const selectedReview = ref(null);

const openReviewModal = async (currTour) => {
  selectedReview.value = await tourStore.getReviewOfTour(currTour.id);
  isReviewModalOpen.value = true;
  selectedTour.value = currTour;
};

const openGuidesModal = async (currTour) => {
  selectedTourGuides.value = await guideStore.getGuidesByIds(currTour.guides);
  isGuidesModalOpen.value = true;
  selectedTour.value = currTour;
};

const closeModals = () => {
  isReviewModalOpen.value = false;
  isGuidesModalOpen.value = false;
  selectedTour.value = null;
  selectedTourGuides.value = [];
  selectedReview.value = null;
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return "";
  const date = new Date(timestamp);
  return date.toLocaleString("en-GB", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Past Tours</h2>
        <p class="text-md text-gray-600 mt-2">View details of completed tours.</p>
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
            <TableHead class="font-bold text-red-700">Date</TableHead>
            <TableHead class="font-bold text-red-700">Time Slot</TableHead>
            <TableHead class="font-bold text-red-700">Visitor Name</TableHead>
            <TableHead class="font-bold text-red-700">Visitor Type</TableHead>
            <TableHead class="font-bold text-red-700">High School</TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(tour, index) in filteredTours" :key="tour.id">
            <TableCell>{{ index + 1 }}</TableCell>
            <TableCell>{{ tour.date }}</TableCell>
            <TableCell>{{ tour.slot }}</TableCell>
            <TableCell>{{ tour.visitor.user.name }}</TableCell>
            <TableCell>{{ tour.visitor.type }}</TableCell>
            <TableCell>{{ tour.visitor.highSchoolName || "N/A" }}</TableCell>
            <TableCell class="flex space-x-2">
              <Button
                variant="primary"
                :disabled="!tour.review"
                class="bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300"
                @click="tour.review && openReviewModal(tour)"
              >
                View Review
              </Button>
              <Button
                variant="primary"
                class="bg-blue-600 text-white hover:bg-blue-700"
                @click="openGuidesModal(tour)"
              >
                View Guides
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>

  <div
    v-if="isReviewModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Review Details</h2>
      <p><strong>Review:</strong> {{ selectedReview.review }}</p>
      <p><strong>Rating:</strong> {{ selectedReview.reviewRating }}</p>
      <p><strong>Timestamp:</strong> {{ formatTimestamp(selectedReview.timestamp) }}</p>
      <Button variant="secondary" class="mt-4" @click="closeModals">Close</Button>
    </div>
  </div>

  <div
    v-if="isGuidesModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-1/2">
      <h2 class="text-xl font-bold mb-4">Guides Details</h2>
      <ul>
        <li
          v-for="guide in selectedTourGuides"
          :key="guide.id"
          class="mb-4 border-b pb-2"
        >
          <p><strong>Name:</strong> {{ guide.name }}</p>
          <p><strong>Rating:</strong> {{ guide.rating }}</p>
        </li>
      </ul>
      <Button variant="secondary" class="mt-4" @click="closeModals">Close</Button>
    </div>
  </div>
</template>

<style scoped>
</style>
