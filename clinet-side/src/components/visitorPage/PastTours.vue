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
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover";
import { RangeCalendar } from "@/components/ui/range-calendar/index.js";
import { CalendarIcon } from "lucide-vue-next";
import { useTourStore } from "@/stores/tourStore";
import { useGuideStore } from "@/stores/guideStore";
import { storeToRefs } from "pinia";

import { toast } from "vue-sonner";

const tourStore = useTourStore();
const guideStore = useGuideStore();
const { tours } = storeToRefs(tourStore);

onMounted(() => {
  tourStore.fetchTours();
});

const searchQuery = ref("");
const selectedType = ref("All");
const dateRange = ref({ start: null, end: null });

const filteredTours = computed(() => {
  return tours.value.filter((tour) => {
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
const isAddReviewModalOpen = ref(false);

const selectedTour = ref(null);
const selectedTourGuides = ref([]);
const reviewText = ref("");
const reviewRating = ref(0);
const reviewDetails = ref(null);

const openAddReviewModal = (tour) => {
  isAddReviewModalOpen.value = true;
  selectedTour.value = tour;
  reviewText.value = "";
  reviewRating.value = 0;
};

const closeAddReviewModal = () => {
  isAddReviewModalOpen.value = false;
  selectedTour.value = null;
  reviewText.value = "";
  reviewRating.value = 0;
};

const openReviewModal = async (tour) => {
  if (tour.review) {
    isReviewModalOpen.value = true;
    reviewDetails.value = await tourStore.getReviewOfTour(tour.id);
  } else {
    toast.error("No review found for this tour.");
  }
};

const closeReviewModal = () => {
  isReviewModalOpen.value = false;
  reviewDetails.value = null;
};

const submitReview = async () => {
  if (!selectedTour.value) return;
  const reviewData = {
    review: reviewText.value,
    reviewRating: reviewRating.value,
  };
  try {
    await tourStore.createReviewOfTour(selectedTour.value.id, reviewData);
    toast.success("Review successfully added!");
    closeAddReviewModal();
    await tourStore.fetchTours(); // Refresh tours after adding the review
  } catch (error) {
    console.error("Error adding review:", error.message);
    toast.error("Failed to add review.");
  }
};

const openGuidesModal = async (tour) => {
  isGuidesModalOpen.value = true;
  selectedTour.value = tour;
  selectedTourGuides.value = await guideStore.getGuidesByIds(tour.guides);
};

const closeGuidesModal = () => {
  isGuidesModalOpen.value = false;
  selectedTour.value = null;
  selectedTourGuides.value = [];
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
    <!-- Filter Bar -->
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
            <SelectValue placeholder="Filter by Visitor Type"/>
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="All">All</SelectItem>
              <SelectItem value="individual">Individual</SelectItem>
              <SelectItem value="high-school">High School</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>

        <Popover>
          <PopoverTrigger as-child>
            <button class="w-[250px] h-10 text-left border border-gray-300 px-4 py-2 rounded-lg">
              <CalendarIcon class="mr-2"/>
              {{ dateRange.start ? format(dateRange.start, "yyyy-MM-dd") : "Start Date" }} -
              {{ dateRange.end ? format(dateRange.end, "yyyy-MM-dd") : "End Date" }}
            </button>
          </PopoverTrigger>
          <PopoverContent class="w-auto p-0">
            <RangeCalendar v-model="dateRange" class="rounded-md border" initial-focus/>
          </PopoverContent>
        </Popover>
      </div>
    </div>

    <!-- Table -->
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
            <TableCell>{{ tour.visitor.type === 'high-school' ? "High School" : "Individual" }}</TableCell>
            <TableCell>{{ tour.visitor.highSchoolName || "N/A" }}</TableCell>
            <TableCell class="flex justify-center space-x-2">
              <button
                  v-if="!tour.review"
                  class="bg-blue-600 text-white hover:bg-blue-700 text-lg px-6 py-3 rounded"
                  @click="openAddReviewModal(tour)"
              >
                Add Review
              </button>
              <button
                  v-else
                  class="bg-green-600 text-white hover:bg-green-700 text-lg px-6 py-3 rounded"
                  @click="openReviewModal(tour)"
              >
                View Review
              </button>
              <button
                  class="bg-blue-600 text-white hover:bg-blue-700 text-lg px-6 py-3 rounded"
                  @click="openGuidesModal(tour)"
              >
                View Guides
              </button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Add Review Modal -->
    <div
        v-if="isAddReviewModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-[400px]">
        <h2 class="text-xl font-bold mb-4">Add Review</h2>
        <textarea
            v-model="reviewText"
            placeholder="Write your review here..."
            class="w-full p-2 border border-gray-300 rounded-lg mb-4"
            rows="4"
        ></textarea>
        <div class="flex items-center gap-4 mb-4">
          <label class="font-bold">Rating:</label>
          <input
              type="range"
              v-model="reviewRating"
              min="0"
              max="5"
              step="0.1"
              class="w-full"
          />
          <span class="text-lg font-bold">{{ reviewRating }}</span>
        </div>
        <div class="flex justify-between">
          <button class="bg-gray-300 text-black px-4 py-2 rounded" @click="closeAddReviewModal">
            Cancel
          </button>
          <button class="bg-blue-600 text-white px-4 py-2 rounded" @click="submitReview">
            Submit
          </button>
        </div>
      </div>
    </div>

    <!-- View Review Modal -->
    <div
        v-if="isReviewModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-[400px]">
        <h2 class="text-xl font-bold mb-4">Review Details</h2>
        <p><strong>Review:</strong> {{ reviewDetails?.review || "No review available" }}</p>
        <p><strong>Rating:</strong> {{ reviewDetails?.reviewRating || "N/A" }}</p>
        <p><strong>Timestamp:</strong> {{ formatTimestamp(reviewDetails?.timestamp) }}</p>
        <button
            class="bg-blue-600 text-white px-4 py-2 rounded mt-4"
            @click="closeReviewModal"
        >
          Close
        </button>
      </div>
    </div>

    <!-- View Guides Modal -->
    <div
        v-if="isGuidesModalOpen"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-[400px]">
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
        <button
            class="bg-blue-600 text-white px-4 py-2 rounded mt-4"
            @click="closeGuidesModal"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
