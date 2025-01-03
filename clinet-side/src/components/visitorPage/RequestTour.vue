<script setup>
import {Label} from "@/components/ui/label";
import {Button} from "@/components/ui/button";
import "@vuepic/vue-datepicker/dist/main.css";
import {
  NumberField,
  NumberFieldContent,
  NumberFieldDecrement,
  NumberFieldIncrement,
  NumberFieldInput,
} from "@/components/ui/number-field";
import {ref, computed, watch} from "vue";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover";
import {RangeCalendar} from "@/components/ui/range-calendar/index.js";
import {addDays, format, eachDayOfInterval} from 'date-fns';
import {CalendarIcon} from 'lucide-vue-next';
import {Checkbox} from "@/components/ui/checkbox/index.js";
import {useTourRequestStore} from "@/stores/tourRequestsStore.js";
import { toast } from "vue-sonner";

const minimumDate = addDays(new Date(), 14);
const dateRangeError = ref(""); // Error message for invalid date range
const tourRequestsStore = useTourRequestStore();

const form = ref({
  dateRange: { start: null, end: null },
  selectedSlots: [],
  numStudents: 0,
  notes: "",
});

const popoverVisible = ref(false);

// Watch date range to enforce a maximum of 5 days and show warning
watch(() => form.value.dateRange, (newRange) => {
  if (newRange.start && newRange.end) {
    const differenceInDays = Math.ceil(
        (new Date(newRange.end) - new Date(newRange.start)) / (1000 * 60 * 60 * 24)
    );
    const diffError = differenceInDays >= 5;
    const minimumError = new Date(newRange.start) < minimumDate || new Date(newRange.end) < minimumDate;

    if (minimumError) {
      form.value.dateRange = { start: null, end: null };
      dateRangeError.value = "You can only select dates 2 weeks from today.";
    } else if (diffError) {
      form.value.dateRange = { start: null, end: null };
      dateRangeError.value = "You can select a maximum range of 5 days.";
    } else {
      dateRangeError.value = "";
      form.value.selectedSlots = [];
    }
    popoverVisible.value = false;
  }
});

const resetForm = () => {
  form.value = {
    dateRange: {start: null, end: null},
    selectedSlots: [],
    numStudents: 0,
    notes: "",
  };
  dateRangeError.value = ""; // Clear any error
};

const submit = () => {
  // Validation: Check if date range is selected
  if (!form.value.dateRange.start || !form.value.dateRange.end) {
    toast.error("Date range is required.", {
      description: "Please select a valid date range before submitting.",
    });
    return;
  }

  // Validation: Check if at least one time slot is selected
  if (form.value.selectedSlots.length === 0) {
    toast.error("Time slot selection is required.", {
      description: "Please select at least one time slot for the tour.",
    });
    return;
  }

  // Validation: Check if the number of students is greater than zero
  if (form.value.numStudents <= 0) {
    toast.error("Invalid number of students.", {
      description: "Please enter a valid number of students greater than zero.",
    });
    return;
  }

  // If all validations pass, submit the form
  tourRequestsStore.createTourRequests(form.value);
  resetForm();
  toast.success("Tour request submitted successfully!", {
    description: "Your tour request has been created.",
  });
};


const daysInRange = computed(() => {
  if (form.value.dateRange.start && form.value.dateRange.end) {
    return eachDayOfInterval({start: form.value.dateRange.start, end: form.value.dateRange.end});
  }
  return [];
});

const slots = tourRequestsStore.slots;

const toggleSelection = (day, slotId) => {
  const formattedDay = format(day, 'yyyy-MM-dd');
  const slotObject = { date: formattedDay, slot: slotId };

  const index = form.value.selectedSlots.findIndex(
      (item) => item.date === slotObject.date && item.slot === slotObject.slot
  );

  if (index > -1) {
    form.value.selectedSlots.splice(index, 1);
  } else {
    form.value.selectedSlots.push(slotObject);
  }
};

const isSelected = (day, slotId) => {
  const formattedDay = format(day, 'yyyy-MM-dd');
  return form.value.selectedSlots.some(
      (item) => item.date === formattedDay && item.slot === slotId
  );
};
</script>

<template>
  <section class="flex justify-center items-center mt-12">
    <!-- Form Section -->
    <div class="bg-white px-8 py-6 rounded-lg shadow-xl border border-gray-200 w-full max-w-lg">
      <div class="text-center mb-6">
        <h2 class="text-3xl font-bold">
          Request a <span class="text-red-600">Tour</span>
        </h2>
        <p class="text-gray-600 mt-2 text-sm">
          Fill out this form to request a tour. For more details,
          <router-link to="/faq" class="text-red-500 font-bold hover:underline">
            See FAQ
          </router-link>
        </p>
      </div>

      <!-- Tour Request Form -->
      <form class="space-y-4">
        <!-- Date Range and Number of People Row -->
        <div class="grid grid-cols-2 gap-4">
          <div class="col-span-1">
            <Label for="dateRange" class="font-medium text-gray-700 text-sm">
              Request Date Range
            </Label>
            <Popover :open="popoverVisible">
              <PopoverTrigger as-child>
                <Button variant="outline" class="w-full h-10 text-left" @click="popoverVisible = !popoverVisible">
                  <CalendarIcon class="mr-2"/>
                  {{ form.dateRange.start ? format(form.dateRange.start, 'dd/MM/yyyy') : 'Start Date' }} -
                  {{ form.dateRange.end ? format(form.dateRange.end, 'dd/MM/yyyy') : 'End Date' }}
                </Button>
              </PopoverTrigger>
              <PopoverContent class="w-auto p-0">
                <RangeCalendar v-model="form.dateRange" class="rounded-md border" initial-focus/>
              </PopoverContent>
            </Popover>
            <p v-if="dateRangeError" class="text-xs text-red-500 mt-1">
              {{ dateRangeError }}
            </p>
          </div>

          <div>
            <Label for="numPeople" class="font-medium text-gray-700 text-sm">
              Number of People
            </Label>
            <NumberField id="numPeople" v-model="form.numStudents" class="w-full">
              <NumberFieldContent>
                <NumberFieldDecrement v-show="form.numStudents > 0"/>
                <NumberFieldInput/>
                <NumberFieldIncrement/>
              </NumberFieldContent>
            </NumberField>
          </div>
        </div>

        <!-- Select Time Slots -->
        <div v-show="form.dateRange.start !== null && form.dateRange.end !== null">
          <Label for="dateRange" class="font-medium text-gray-700 text-sm">
            Select Time Slots
          </Label>
          <!-- Header Row -->
          <div class="header flex font-bold mb-2">
            <div class="timeslot w-1/4">Timeslot</div>
            <div v-for="(slot, index) in slots" :key="index" class="slot text-center w-1/4">
              {{ slot }}
            </div>
          </div>

          <!-- Days and Slots -->
          <div class="body space-y-2">
            <div v-for="day in daysInRange" :key="day" class="day-row flex items-center">
              <div class="day w-1/4 font-medium">
                {{ format(day, 'dd/MM') }}
              </div>
              <!-- Slots Grid -->
              <div class="w-3/4 grid grid-cols-4 gap-2">
                <div
                  v-for="(slot, index) in slots"
                  :key="index"
                  class="flex items-center justify-center h-10 border border-gray-300 cursor-pointer 
                         hover:border-green-500 hover:bg-green-100 transition-colors duration-200 ease-in-out"
                  :class="{'bg-green-500 text-white': isSelected(day, index)}"
                  @click="toggleSelection(day, index)"
                >
                  <!-- You can optionally display the slot time or a check icon when selected -->
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Additional Notes -->
        <div>
          <Label for="notes" class="font-medium text-gray-700 text-sm">Additional Notes</Label>
          <textarea
            id="notes"
            v-model="form.notes"
            placeholder="Any additional information"
            class="w-full h-20 px-4 py-2 border rounded-lg"
          ></textarea>
        </div>

        <div class="flex justify-end space-x-4">
          <Button class="bg-gray-400 text-white px-6 py-2 rounded-lg hover:bg-gray-500" @click.prevent="resetForm">
            Reset Form
          </Button>
          <Button type="submit" class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700" @click.prevent="submit">
            Submit Request
          </Button>
        </div>
      </form>
    </div>
  </section>
</template>

