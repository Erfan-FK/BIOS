<!-- components/AvailabilityComponent.vue -->

<script setup>
import { ref, onMounted } from "vue";
import { Plus, Trash2, Check } from "lucide-vue-next";
import { useAvailabilityScheduleStore } from "@/stores/availabilityScheduleStore";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

const availabilityStore = useAvailabilityScheduleStore();
onMounted(() => {
  availabilityStore.fetchAvailability();
});

// Updated daysOfWeek to start from Monday
const daysOfWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
const timeSlots = [
  "9:00 am - 11:00 am",
  "11:00 am - 1:00 pm",
  "1:30 pm - 4:00 pm",
  "4:00 pm - 5:30 pm",
];

const showAddDialog = ref(false);
const showDeleteDialog = ref(false);
const showUpdateDialog = ref(false);

const currentSlot = ref({ day: "", slot: "" });
const updateSlot = ref({ source: null, target: null });

// Open Add Dialog
const openAddDialog = (day, slot) => {
  currentSlot.value = { day, slot };
  showAddDialog.value = true;
};

// Open Delete Dialog
const openDeleteDialog = (day, slot) => {
  currentSlot.value = { day, slot };
  showDeleteDialog.value = true;
};

// Confirm Add
const confirmAdd = () => {
  availabilityStore.toggleAvailability(
    currentSlot.value.day,
    currentSlot.value.slot
  );
  showAddDialog.value = false;
};

// Confirm Delete
const confirmDelete = () => {
  availabilityStore.toggleAvailability(
    currentSlot.value.day,
    currentSlot.value.slot
  );
  showDeleteDialog.value = false;
};

// Cancel Action
const cancelAction = () => {
  showAddDialog.value = false;
  showDeleteDialog.value = false;
  showUpdateDialog.value = false;
};

// Handle Drag Start
const handleDragStart = (day, timeSlot) => {
  if (availabilityStore.isAvailable(day, timeSlot)) {
    updateSlot.value.source = { day, timeSlot };
  }
};

// Handle Drop
const handleDrop = (targetDay, targetSlot) => {
  const sourceSlot = updateSlot.value.source;

  if (
    sourceSlot &&
    availabilityStore.isAvailable(sourceSlot.day, sourceSlot.timeSlot) &&
    !availabilityStore.isAvailable(targetDay, targetSlot)
  ) {
    updateSlot.value.target = { day: targetDay, timeSlot: targetSlot };
    showUpdateDialog.value = true; // Show confirmation dialog
  }
};

// Confirm Slot Update
const confirmUpdate = async () => {
  const { source, target } = updateSlot.value;

  if (source && target) {
    await availabilityStore.updateSlotAvailability(
      source.day,
      source.timeSlot,
      target.day,
      target.timeSlot
    );
  }

  // Close dialog and reset state
  showUpdateDialog.value = false;
  updateSlot.value = { source: null, target: null };
};
</script>

<template>
  <div class="flex flex-col w-full h-full bg-white rounded-lg shadow-lg">
    <!-- Header Section -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Available Schedule</h2>
        <p class="text-md text-gray-600 mt-2">
          Select the time slots you are available to guide tours or drag and
          drop to update availability.
        </p>
      </div>
    </div>

    <!-- Availability Calendar Grid -->
    <div class="grid grid-cols-8 gap-4 p-6 h-full">
      <!-- Time Slot Labels Column -->
      <div class="flex flex-col">
        <div class="text-center font-bold text-black mb-2 text-lg">
          Time Slots
        </div>
        <div
          v-for="slot in timeSlots"
          :key="slot"
          class="flex items-center justify-center h-full font-semibold text-black text-lg"
        >
          {{ slot }}
        </div>
      </div>

      <!-- Days of the Week Columns -->
      <div
        v-for="day in daysOfWeek"
        :key="day"
        class="flex flex-col space-y-6 h-full"
      >
        <div class="text-center font-bold text-black mb-2 text-lg">
          {{ day }}
        </div>
        <div
          v-for="slot in timeSlots"
          :key="slot"
          class="group flex items-center justify-center h-full border border-gray-200 rounded-lg cursor-pointer transition-all duration-200"
          :class="{
            'bg-green-500': availabilityStore.isAvailable(day, slot),
            'hover:bg-gray-100 border-dashed': !availabilityStore.isAvailable(
              day,
              slot
            ),
          }"
          draggable="true"
          @dragstart="handleDragStart(day, slot)"
          @dragover.prevent
          @drop="handleDrop(day, slot)"
          @click="
            availabilityStore.isAvailable(day, slot)
              ? openDeleteDialog(day, slot)
              : openAddDialog(day, slot)
          "
        >
          <div
            v-if="availabilityStore.isAvailable(day, slot)"
            class="relative flex items-center justify-center"
          >
            <div class="absolute">
              <Check class="text-white w-6 h-6 group-hover:invisible" />
            </div>
            <div class="absolute">
              <Trash2
                class="text-white w-6 h-6 invisible group-hover:visible"
              />
            </div>
          </div>
          <div v-else>
            <Plus class="text-gray-400 w-6 h-6" />
          </div>
        </div>
      </div>
    </div>

    <!-- Add Slot Dialog -->
    <Dialog v-model:open="showAddDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle class="text-xl font-semibold"
            >Confirm Slot Addition</DialogTitle
          >
          <DialogDescription class="text-md">
            Are you sure you want to add availability for
            <span class="font-semibold">{{ currentSlot.day }}</span>
            <span class="font-semibold">{{ currentSlot.slot }}</span
            >?
          </DialogDescription>
        </DialogHeader>
        <DialogFooter class="space-x-4">
          <Button class="px-6 py-2 text-lg" @click="cancelAction"
            >Cancel</Button
          >
          <Button
            class="bg-green-500 hover:bg-green-600 text-white px-6 py-2 text-lg"
            @click="confirmAdd"
          >
            Confirm
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Delete Slot Dialog -->
    <Dialog v-model:open="showDeleteDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle class="text-xl">Confirm Slot Deletion</DialogTitle>
          <DialogDescription class="text-md">
            Are you sure you want to remove availability for
            <span class="font-semibold">{{ currentSlot.day }}</span>
            <span class="font-semibold">{{ currentSlot.slot }}</span
            >?
          </DialogDescription>
        </DialogHeader>
        <DialogFooter class="space-x-4">
          <Button class="px-6 py-2 text-lg" @click="cancelAction"
            >Cancel</Button
          >
          <Button
            class="bg-red-500 hover:bg-red-600 text-white px-6 py-2 text-lg"
            @click="confirmDelete"
          >
            Confirm
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Update Slot Dialog -->
    <Dialog v-model:open="showUpdateDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle class="text-xl font-semibold"
            >Confirm Slot Update</DialogTitle
          >
          <DialogDescription class="text-md">
            Are you sure you want to move availability from
            <span class="font-semibold">{{ updateSlot.source?.day }}</span> -
            <span class="font-semibold">{{ updateSlot.source?.timeSlot }}</span>
            to
            <span class="font-semibold">{{ updateSlot.target?.day }}</span> -
            <span class="font-semibold">{{ updateSlot.target?.timeSlot }}</span
            >?
          </DialogDescription>
        </DialogHeader>
        <DialogFooter class="space-x-4">
          <Button class="px-6 py-2 text-lg" @click="cancelAction"
            >Cancel</Button
          >
          <Button
            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 text-lg"
            @click="confirmUpdate"
          >
            Confirm
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </div>
</template>
