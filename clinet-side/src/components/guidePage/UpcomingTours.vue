<script setup>
import { ref, computed, onMounted } from "vue";
import { useTourStore } from "@/stores/tourStore.js";
import { useTourReportStore } from "@/stores/tourReportStore.js";
import { useAuthStore } from "@/stores/authStore.js"; // Import auth store
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
  TableCell,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
  SelectLabel,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { RangeCalendar } from "@/components/ui/range-calendar/index.js";
import { CalendarIcon } from "lucide-vue-next";
import { format, differenceInDays } from "date-fns";
import VueTimepicker from 'vue3-timepicker';
import 'vue3-timepicker/dist/VueTimepicker.css';
import { toast } from "vue-sonner";

// Initialize Stores
const tourStore = useTourStore();
const tourReportStore = useTourReportStore();
const authStore = useAuthStore(); // Auth store

// Reactive References
const searchQuery = ref("");
const selectedType = ref("All");
const dateRange = ref({ start: null, end: null });

const isAddReportModalOpen = ref(false); // Add Report Modal
const isViewReportModalOpen = ref(false); // View Report Modal
const selectedTour = ref(null);
const finishTime = ref("");
const reportText = ref("");

const reportMap = ref({}); // Reactive map to store the user's report by tour ID
const isProcessing = ref(false); // To prevent multiple simultaneous actions

// Fetch Tours and Reports on Mount
onMounted(async () => {
  try {
    await tourStore.fetchTours();
    await fetchReportsForAllTours();
  } catch (error) {
    console.error("Error fetching tours or reports:", error);
    toast.error("Failed to load tours or reports.");
  }
});

// Function to fetch reports for all tours and populate reportMap with only the current user's report
const fetchReportsForAllTours = async () => {
  try {
    const tours = tourStore.tours;
    const promises = tours.map(tour => tourReportStore.getReportByTourId(tour.id));
    const reportsArrays = await Promise.all(promises);

    reportsArrays.forEach((reportsArray, index) => {
      const tourId = tours[index].id;
      if (Array.isArray(reportsArray) && reportsArray.length > 0) {
        // Find the report for the logged-in user
        const userReport = reportsArray.find(report => report.guide === authStore.user.profile_id);
        if (userReport) {
          reportMap.value[tourId] = userReport;
        }
      }
    });
  } catch (error) {
    console.error("Error fetching reports for tours:", error);
    toast.error("Failed to load tour reports.");
  }
};

// Computed property to filter tours based on search, type, and date range
const filteredTours = computed(() => {
  return tourStore.tours.filter((tour) => {
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

    const isAfterToday = new Date(tour.date) > new Date();

    return matchesSearch && matchesType && matchesDateRange && isAfterToday;
  });
});

// Check if the current user has a report for the given tour
const hasReport = (tour) => {
  console.log(reportMap.value[tour.id]);
  return reportMap.value[tour.id] !== undefined;
};

// Function to open Add Report Modal
const openAddReportModal = (tour) => {
  selectedTour.value = tour;
  finishTime.value = "";
  reportText.value = "";
  isAddReportModalOpen.value = true;
};

// Function to open View Report Modal (only called if hasReport(tour) is true)
const openViewReportModal = (tour) => {
  selectedTour.value = tour;
  const report = reportMap.value[tour.id];
  if (report) {
    const hour = report.finishedAtHour;
    const minute = report.finishedAtMinute;
    const amPm = hour < 12 ? "AM" : "PM";
    finishTime.value = `${hour}:${minute < 10 ? '0' + minute : minute}${amPm}`;
    reportText.value = report.report;
  }
  isViewReportModalOpen.value = true;
};

// Function to close both modals
const closeModals = () => {
  isAddReportModalOpen.value = false;
  isViewReportModalOpen.value = false;
  selectedTour.value = null;
  finishTime.value = "";
  reportText.value = "";
};

const submitReport = async () => {
  // Ensure a tour is selected
  if (!selectedTour.value) return;

  // Trim and retrieve input values
  const finishTimeValue = finishTime.value?.trim();
  const reportTextValue = reportText.value?.trim();

  // Validate inputs
  if (!finishTimeValue || !reportTextValue) {
    toast.error("Please provide both finish time and report text.");
    return;
  }

  // Split finishTime into hours and minutes
  const [finishHour, finishMinute] = finishTimeValue.split(":").map(Number);

  // Optional: Validate the time format
  if (
      isNaN(finishHour) ||
      isNaN(finishMinute) ||
      finishHour < 0 ||
      finishHour > 23 ||
      finishMinute < 0 ||
      finishMinute > 59
  ) {
    toast.error("Please provide a valid finish time in HH:MM format.");
    return;
  }

  isProcessing.value = true;
  try {
    // Create the new report
    const newReport = await tourReportStore.createReport(
        reportTextValue,
        finishHour,
        finishMinute,
        selectedTour.value.id
    );

    // Update the report map with the new report
    reportMap.value[selectedTour.value.id] = newReport;

    // Notify success and close modals
    toast.success("Report submitted successfully!");
    await fetchReportsForAllTours();
    closeModals();
  } catch (error) {
    console.error("Error submitting report:", error);
    toast.error("Failed to submit the report.");
  } finally {
    isProcessing.value = false;
  }
};


// Placeholder reject function (just as in original code)
const rejectTour = (tour) => {
  // Implement your reject logic here
  toast("This is where you'd reject the tour.");
};
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <!-- Filter Bar -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Upcoming Tours</h2>
        <p class="text-md text-gray-600 mt-2">View and manage all upcoming tours assigned to you.</p>
      </div>

      <div class="flex items-center gap-4">
        <!-- Search by High School -->
        <input
            v-model="searchQuery"
            type="text"
            placeholder="Search by High School"
            class="w-[300px] p-2 border border-gray-300 rounded-lg"
        />

        <!-- Visitor Type Filter (All / individual / high-school) -->
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

        <!-- Date Range Filter -->
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

    <!-- Tours Table -->
    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">Name</TableHead>
            <TableHead v-if="selectedType === 'high-school'" class="font-bold text-red-700">
              Responsible Person
            </TableHead>
            <TableHead v-if="selectedType === 'high-school'" class="font-bold text-red-700">
              Group Count
            </TableHead>
            <TableHead class="font-bold text-red-700">Date</TableHead>
            <TableHead class="font-bold text-red-700">Slot</TableHead>
            <TableHead class="text-right font-bold text-red-700">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="tour in filteredTours" :key="tour.id">
            <TableCell class="font-bold">
              {{
                tour.visitor.type === "high-school"
                    ? tour.visitor.highSchoolName
                    : `Visitor #${tour.visitor.id}`
              }}
            </TableCell>
            <TableCell v-if="selectedType === 'high-school'">
              {{ tour.visitor.contactNumber || 'N/A' }}
            </TableCell>
            <TableCell v-if="selectedType === 'high-school'">
              {{ tour.guides.length }}
            </TableCell>
            <TableCell>
              {{
                new Date(tour.date).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                })
              }}
            </TableCell>
            <TableCell>{{ tour.slot }}</TableCell>
            <TableCell class="text-right">
              <Button
                  variant="default"
                  @click="hasReport(tour) ? openViewReportModal(tour) : openAddReportModal(tour)"
                  class="mr-1 bg-blue-600 hover:bg-blue-500"
                  :disabled="(!hasReport(tour)) && (new Date(tour.date) > new Date())"
              >
                {{ hasReport(tour) ? "View Report" : "Report" }}
              </Button>
              <Button
                  variant="destructive"
                  @click="rejectTour(tour)"
                  :disabled="(new Date(tour.date) - new Date()) / (1000 * 60 * 60 * 24) < 14"
              >
                Reject
              </Button>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Add Report Modal -->
    <div
        v-if="isAddReportModalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-white rounded-lg shadow-lg p-6 w-[400px]">
        <h2 class="text-xl font-bold mb-4">Add Report</h2>
        <div class="mb-4">
          <label class="block mb-2 font-semibold">Finish Time:</label>
          <VueTimepicker
              type="time"
              v-model="finishTime"
              class="w-full rounded-lg"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-2 font-semibold">Report Text:</label>
          <textarea
              v-model="reportText"
              rows="4"
              class="w-full border border-gray-300 rounded-lg p-2"
              placeholder="Enter report details..."
          ></textarea>
        </div>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="closeModals">Cancel</Button>
          <Button
              variant="default"
              @click="submitReport"
              :disabled="isProcessing"
          >
            Submit Report
          </Button>
        </div>
      </div>
    </div>

    <!-- View Report Modal -->
    <div
        v-if="isViewReportModalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
    >
      <div class="bg-white rounded-lg shadow-lg p-6 w-[400px]">
        <h2 class="text-xl font-bold mb-4">View Report</h2>
        <p><strong>Finish Time:</strong> {{ finishTime }}</p>
        <p class="mt-4"><strong>Report Text:</strong></p>
        <p class="whitespace-pre-wrap">{{ reportText }}</p>
        <div class="flex justify-end mt-6">
          <Button variant="outline" @click="closeModals">Close</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom styles can be added here */
</style>
