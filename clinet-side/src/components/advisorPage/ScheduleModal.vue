<script setup>
import {ref, computed, watch} from "vue";
import {format, addDays} from "date-fns";
import {storeToRefs} from "pinia";

import {useGuideStore} from "@/stores/guideStore";
import {useTourRequestStore} from "@/stores/tourRequestsStore.js";
import {useAdvisorStore} from "@/stores/advisorStore.js";

import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectValue,
  SelectLabel,
} from "@/components/ui/select";
import {Button} from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle
} from "@/components/ui/dialog/index.js";
import {Star} from "lucide-vue-next";
import {useTourStore} from "@/stores/tourStore.js";

// Props
const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  selectedTourRequestBatch: {
    type: Object,
    default: null
  },
  selectedDayOffset: {
    type: Number,
    default: null
  },
  selectedSlotIndex: {
    type: Number,
    default: null
  },
  selectedGuides: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['close']);

// Stores
const tourRequestStore = useTourRequestStore();
const guideStore = useGuideStore();
const advisorStore = useAdvisorStore();
const tourStore = useTourStore();

const {guides} = storeToRefs(guideStore);
const {advisor} = storeToRefs(advisorStore);

// Local States
const daysToShow = [0, 1, 2, 3, 4];  // 5 days starting from the base date
const slotIndices = [0, 1, 2, 3];   // 4 slots

const baseDate = computed(() => {
  if (!props.selectedTourRequestBatch?.tourRequests?.[0]?.date) return null;
  return new Date(props.selectedTourRequestBatch.tourRequests[0].date);
});

const guideSearchQuery = ref("");
const guideSortOption = ref("name-asc");
const showSaveDialog = ref(false);

const internalDayOffset = ref(props.selectedDayOffset);
const internalSlotIndex = ref(props.selectedSlotIndex);
const internalSelectedGuides = ref([...props.selectedGuides]);

// Reset internal states when tour batch changes
watch(() => props.selectedTourRequestBatch, () => {
  internalDayOffset.value = props.selectedDayOffset;
  internalSlotIndex.value = props.selectedSlotIndex;
  internalSelectedGuides.value = [...props.selectedGuides];
});

const emitClose = async () => {
  emit('close');
  await guideStore.fetchGuides();
};

// Helper functions
const getMondayBasedWeekday = (date) => {
  return (date.getDay() + 6) % 7;
};

const getDateForOffset = (offset) => {
  if (!baseDate.value) return null;
  return addDays(baseDate.value, offset);
};

const getMondayBasedWeekdayForOffset = (offset) => {
  const d = getDateForOffset(offset);
  return d ? getMondayBasedWeekday(d) : null;
};

const isAuthorized = (dayOffset) => {
  const weekday = getMondayBasedWeekdayForOffset(dayOffset);
  return weekday !== null && advisor.value?.authorizedDay?.includes(weekday);
};

const selectedTourAndSlotIsRequested = (dayOffset, slotIndex) => {
  if (!props.selectedTourRequestBatch?.tourRequests || !baseDate.value) return false;
  const targetDate = format(getDateForOffset(dayOffset), 'yyyy-MM-dd');
  const slotTime = tourRequestStore.slots[slotIndex];
  return props.selectedTourRequestBatch.tourRequests.some(
      (tr) => tr.date === targetDate && tr.time_slot === slotTime
  );
};

const handleCellClick = (dayOffset, slotIndex) => {
  internalDayOffset.value = null;
  internalSlotIndex.value = null;
  if (!selectedTourAndSlotIsRequested(dayOffset, slotIndex) || !isAuthorized(dayOffset)) return;
  internalDayOffset.value = dayOffset;
  internalSlotIndex.value = slotIndex;
  internalSelectedGuides.value = [];
};

const filteredGuides = computed(() => {
  if (internalDayOffset.value === null || internalSlotIndex.value === null) return [];
  const weekday = getMondayBasedWeekdayForOffset(internalDayOffset.value);
  if (weekday === null) return [];

  const availabilityIndex = weekday * 4 + internalSlotIndex.value;
  let availableGuides = guides.value.filter((guide) => guide.availability[availabilityIndex]);

  // Apply search filter
  if (guideSearchQuery.value.trim() !== "") {
    const query = guideSearchQuery.value.trim().toLowerCase();
    availableGuides = availableGuides.filter((guide) => {
      const nameMatch = guide.user.name.toLowerCase().includes(query);
      const ratingMatch = guide.rating.toString().includes(query);
      return nameMatch || ratingMatch;
    });
  }

  // Apply sorting
  switch (guideSortOption.value) {
    case "name-asc":
      availableGuides.sort((a, b) => a.user.name.localeCompare(b.user.name));
      break;
    case "name-desc":
      availableGuides.sort((a, b) => b.user.name.localeCompare(a.user.name));
      break;
    case "rating-asc":
      availableGuides.sort((a, b) => a.rating - b.rating);
      break;
    case "rating-desc":
      availableGuides.sort((a, b) => b.rating - a.rating);
      break;
    default:
      break;
  }

  return availableGuides;
});

const handleGuideClick = (guide) => {
  if (internalSelectedGuides.value.includes(guide.id)) {
    internalSelectedGuides.value = internalSelectedGuides.value.filter((id) => id !== guide.id);
    return;
  }
  internalSelectedGuides.value.push(guide.id);
};

const confirmSchedule = async () => {
  showSaveDialog.value = false;
  if (
      props.selectedTourRequestBatch &&
      typeof internalDayOffset.value === 'number' &&
      typeof internalSlotIndex.value === 'number' &&
      internalSelectedGuides.value.length
  ) {
    const dateToSchedule = format(getDateForOffset(internalDayOffset.value), 'yyyy-MM-dd');
    const payload = {
      visitor_id: props.selectedTourRequestBatch.visitor.id,
      date: dateToSchedule,
      slot: tourRequestStore.slots[internalSlotIndex.value],
      status: "ASSIGNED",
      guides: internalSelectedGuides.value
    };
    await tourRequestStore.scheduleTourRequestBatch(props.selectedTourRequestBatch.id, payload);
    await tourStore.fetchTours()
    await tourRequestStore.fetchApprovedTourRequestBatches();
  }
  emitClose();
};
</script>

<template>
  <div
      v-if="isOpen"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-[90%] max-w-5xl">
      <div class="flex gap-4 flex-grow">
        <div class="overflow-x-auto flex-1">
          <h2 class="text-xl font-bold mb-4">Schedule Tour</h2>
          <label class="font-medium text-gray-700 text-sm mb-2 block">Select Time Slots</label>

          <!-- Header Row -->
          <div class="header flex font-bold mb-2">
            <!-- First column for "Time Slot" -->
            <div class="timeslot w-1/4 p-2">Time Slot</div>
            <!-- Columns for each day -->
            <div
                v-for="dayOffset in daysToShow"
                :key="dayOffset"
                class="slot text-center p-2 font-bold flex-1"
                :class="{'bg-gray-200': !isAuthorized(dayOffset)}"
            >
              <span v-if="baseDate">
                {{ format(getDateForOffset(dayOffset), 'EEEE dd/MM') }}
              </span>
            </div>
          </div>

          <!-- Body -->
          <div class="body space-y-2">
            <!-- Each row represents a time slot -->
            <div
                v-for="slotIndex in slotIndices"
                :key="slotIndex"
                class="day-row flex items-center hover:bg-green-50 transition-colors duration-200 ease-in-out"
            >
              <!-- First column: the time slot name -->
              <div class="day w-1/4 font-medium p-2">
                {{ tourRequestStore.slots[slotIndex] }}
              </div>
              <!-- Columns for each day -->
              <div class="w-3/4 grid grid-cols-5 gap-2">
                <div
                    v-for="dayOffset in daysToShow"
                    :key="dayOffset"
                    class="flex items-center justify-center h-10 border border-gray-300 cursor-pointer hover:border-green-500 hover:bg-green-100 transition-colors duration-200 ease-in-out p-2"
                    :class="{
                    'bg-green-500': selectedTourAndSlotIsRequested(dayOffset, slotIndex) && isAuthorized(dayOffset),
                    'bg-gray-200': !isAuthorized(dayOffset) && !selectedTourAndSlotIsRequested(dayOffset, slotIndex),
                    'bg-gray-600': !isAuthorized(dayOffset) && selectedTourAndSlotIsRequested(dayOffset, slotIndex),
                    'bg-pink-500 border-pink-500 hover:border-pink-500 hover:bg-pink-100 text-white': internalDayOffset === dayOffset && internalSlotIndex === slotIndex
                  }"
                    @click="handleCellClick(dayOffset, slotIndex)"
                >
                  <p v-if="internalSlotIndex===slotIndex && internalDayOffset===dayOffset">
                    {{ internalSelectedGuides.length ? internalSelectedGuides.length : '' }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="border-l-2 border-gray-300 ml-2"></div>

        <!-- Guide Selection -->
        <div class="p-2 w-1/3">
          <label class="font-medium text-gray-700 text-sm mb-2 block">Select a Guide</label>

          <!-- Search and Sort Controls -->
          <div class="flex flex-col space-y-2 mb-4">
            <!-- Search Input -->
            <input
                v-model="guideSearchQuery"
                type="text"
                placeholder="Search by name or rating"
                class="p-2 border border-gray-300 rounded-lg"
            />

            <!-- Sort Dropdown -->
            <Select v-model="guideSortOption">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Sort Guides"/>
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>Sort By</SelectLabel>
                  <SelectItem value="name-asc">Name (A-Z)</SelectItem>
                  <SelectItem value="name-desc">Name (Z-A)</SelectItem>
                  <SelectItem value="rating-asc">Rating (Low to High)</SelectItem>
                  <SelectItem value="rating-desc">Rating (High to Low)</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <!-- Scrollable Guide List -->
          <div class="h-48 overflow-y-auto rounded-md shadow-sm">
            <ul>
              <li v-for="guide in filteredGuides" :key="guide.id" class="mt-2">
                <button
                    @click="handleGuideClick(guide)"
                    class="flex items-center border-2 w-full text-left px-4 py-2 hover:bg-green-50 transition-colors duration-200 ease-in-out rounded-md"
                    :class="{'outline-none bg-pink-100 border-pink-500 hover:border-pink-500 hover:bg-pink-100': internalSelectedGuides.includes(guide.id)}"
                >
                  <img :src="guide.user.profile_picture" alt="Guide" class="w-8 h-8 rounded-full mr-3 border-white"/>
                  <span class="font-medium text-gray-800 flex-1">{{ guide.user.name }}</span>
                  <span class="flex items-center space-x-1 ml-2">
                    <span class="font-semibold text-gray-900">{{ guide.rating.toFixed(1) }}</span>
                    <Star class="w-5 h-5 text-yellow-400 fill-current"/>
                  </span>
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <div class="flex gap-2 mt-4">
        <Button variant="secondary" @click="emitClose">Close</Button>
        <Button variant="default" @click="showSaveDialog = true">Save</Button>
      </div>

      <!-- Confirm Save Dialog -->
      <Dialog v-model:open="showSaveDialog">
        <DialogContent>
          <DialogHeader>
            <DialogTitle class="text-xl font-semibold">Confirm Save</DialogTitle>
            <DialogDescription class="text-md">
              Are you sure you want to save this schedule and create a tour?
            </DialogDescription>
          </DialogHeader>
          <DialogFooter class="space-x-4">
            <Button class="px-6 py-2 text-lg" @click="showSaveDialog = false">Cancel</Button>
            <Button class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 text-lg" @click="confirmSchedule">
              Confirm
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  </div>
</template>

<style scoped>
/* Add any component-specific styles here */
</style>
