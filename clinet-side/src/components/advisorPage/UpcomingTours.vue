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
import {useTourStore} from "@/stores/tourStore";
import {storeToRefs} from "pinia";
import {useGuideStore} from "@/stores/guideStore";
import ScheduleModal from "@/components/advisorPage/ScheduleModal.vue";
import {useTourRequestStore} from "@/stores/tourRequestsStore.js";
import {useAdvisorStore} from "@/stores/advisorStore.js";
import {useAuthStore} from "@/stores/authStore.js";
import {differenceInDays} from "date-fns";

const tourStore = useTourStore();
const tourRequestStore = useTourRequestStore();
const guideStore = useGuideStore();
const authStore = useAuthStore();
const advisorStore = useAdvisorStore();
const {tours} = storeToRefs(tourStore);
const {user} = storeToRefs(authStore);


onMounted(async () => {
  await tourStore.fetchTours()
  await guideStore.fetchGuides();
  if (user.value?.profile_id) {
    await advisorStore.fetchAdvisor(user.value.profile_id);
  }
});


const searchQuery = ref("");
const selectedType = ref("All");
const dateRange = ref({start: null, end: null});

const filteredTours = computed(() => {
  return tours?.value?.tours?.filter((tour) => {
    const matchesStatus = tour.status === "ASSIGNED"; // Check if status is 'COMPLETED'
    const matchesSearch =
        searchQuery.value === "" ||
        (tour.visitor.highSchoolName &&
            tour.visitor.highSchoolName.toLowerCase().includes(searchQuery.value.toLowerCase()));
    const matchesType =
        selectedType.value === "All" || tour.visitor.type === selectedType.value;
    const matchesDateRange =
        (!dateRange.value.start && !dateRange.value.end) ||
        (new Date(tour.date) >= dateRange.value.start &&
            new Date(tour.date) <= dateRange.value.end);
    return matchesStatus && matchesSearch && matchesType && matchesDateRange;
  });
});

const isScheduleModalOpen = ref(false);

const selectedTour = ref(null);
const selectedTourRequestBatch = ref(null);

const dayOffset = ref(null);
const slotIndex = ref(null);
const selectedGuides = ref([]);

const openRescheduleModal = async (currTour) => {
  selectedTour.value = currTour;
  slotIndex.value = parseInt(currTour.time_slot_id,10);
  selectedGuides.value = currTour.guides;
  selectedTourRequestBatch.value = await tourRequestStore.getTourRequestBatchOfTour(selectedTour.value.id);
  dayOffset.value = differenceInDays(selectedTourRequestBatch.value.tourRequests[0].date, currTour.date);
  isScheduleModalOpen.value = true;
};

const closeModals = () => {
  isScheduleModalOpen.value = false;
  selectedTour.value = null;
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
        <h2 class="text-xl font-bold">Upcoming Tours</h2>
        <p class="text-md text-gray-600 mt-2">View details of upcoming tours.</p>
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
              <CalendarIcon class="mr-2"/>
              {{ dateRange.start ? format(dateRange.start, "yyyy-MM-dd") : "Start Date" }} -
              {{ dateRange.end ? format(dateRange.end, "yyyy-MM-dd") : "End Date" }}
            </Button>
          </PopoverTrigger>
          <PopoverContent class="w-auto p-0">
            <RangeCalendar v-model="dateRange" class="rounded-md border" initial-focus/>
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
            <TableCell class="flex space-x-2 justify-end">
              <Button
                  variant="primary"
                  class="bg-blue-600 text-white hover:bg-blue-700"
                  @click="openRescheduleModal(tour)"
              >
                Reschedule/View/Change Guides
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>
  </div>

  <ScheduleModal
      :isOpen="isScheduleModalOpen"
      :selectedTourRequestBatch="selectedTourRequestBatch"
      :selectedDayOffset="dayOffset"
      :selectedSlotIndex="slotIndex"
      :selectedGuides="selectedGuides"
      @close="closeModals"
  />
</template>

<style scoped>
</style>
