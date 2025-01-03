<script setup>
import { ref, computed } from "vue";
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
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

// Sample log data
const logs = ref([
  {
    logID: 1,
    guideID: 101,
    tourID: 123,
    counselorID: null,
    advisorID: 201,
    type: "Tour Assignment",
    timestamp: "2024-12-09 12:30:00",
  },
  {
    logID: 2,
    guideID: null,
    tourID: null,
    counselorID: 302,
    advisorID: 201,
    type: "Rejection",
    timestamp: "2024-12-09 13:00:00",
  },
  {
    logID: 3,
    guideID: 102,
    tourID: 124,
    counselorID: null,
    advisorID: null,
    type: "Tour Assignment",
    timestamp: "2024-12-08 14:15:00",
  },
  {
    logID: 4,
    guideID: null,
    tourID: null,
    counselorID: 303,
    advisorID: 202,
    type: "Registration",
    timestamp: "2024-12-08 15:00:00",
  },
]);

const searchQuery = ref("");
const selectedFilter = ref("All");
const selectedType = ref("All");

// Generate log strings
const generatedLogStrings = computed(() => {
  return logs.value.map((log) => {
    let message = `[${log.timestamp}] `;
    if (log.type === "Tour Assignment") {
      message += `Guide #${log.guideID} was assigned to Tour #${log.tourID}`;
    } else if (log.type === "Rejection") {
      message += `Counselor #${log.counselorID} was rejected by Advisor #${log.advisorID}`;
    } else if (log.type === "Registration") {
      message += `Counselor #${log.counselorID} registered with Advisor #${log.advisorID}`;
    }
    return { ...log, message };
  });
});

// Filtered logs
const filteredLogs = computed(() => {
  return generatedLogStrings.value.filter((log) => {
    const matchesSearch =
      searchQuery.value === "" ||
      log.message.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesFilter =
      (selectedFilter.value === "All" || log.tourID == selectedFilter.value) &&
      (selectedType.value === "All" || log.type === selectedType.value);
    return matchesSearch && matchesFilter;
  });
});
</script>

<template>
    <!-- Logs Page -->
    <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <!-- Header with filter dropdown and search -->
      <div class="flex justify-between items-center p-6 border-b border-gray-300">
        <div>
          <h2 class="text-xl font-bold">System Logs</h2>
          <p class="text-md text-gray-600 mt-2">
            View and filter system logs.
          </p>
        </div>
  
        <div class="flex flex-col items-center gap-2">
          <div class="flex items-center gap-4">
            <div class="flex flex-col items-center">
              <span class="text-sm text-gray-500 mb-1">Search by keyword</span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search logs"
                class="w-[250px] p-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div class="flex flex-col items-center">
              <span class="text-sm text-gray-500 mb-1">Filter by Tour</span>
              <Select v-model="selectedFilter">
                <SelectTrigger class="w-[180px]">
                  <SelectValue placeholder="Filter by Tour ID" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Filter by Tour ID</SelectLabel>
                    <SelectItem value="All">All</SelectItem>
                    <SelectItem value="123">Tour #123</SelectItem>
                    <SelectItem value="124">Tour #124</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
            <div class="flex flex-col items-center">
              <span class="text-sm text-gray-500 mb-1">Filter by Log Type</span>
              <Select v-model="selectedType">
                <SelectTrigger class="w-[180px]">
                  <SelectValue placeholder="Filter by Type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectLabel>Filter by Type</SelectLabel>
                    <SelectItem value="All">All</SelectItem>
                    <SelectItem value="Tour Assignment">Tour Assignment</SelectItem>
                    <SelectItem value="Rejection">Rejection</SelectItem>
                    <SelectItem value="Registration">Registration</SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Table displaying logs -->
      <div class="flex-grow overflow-y-auto p-6 pt-2">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead class="font-bold text-red-700">#</TableHead>
              <TableHead class="font-bold text-red-700">Log Message</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow
              v-for="(log, index) in filteredLogs"
              :key="log.logID"
            >
              <TableCell>{{ index + 1 }}</TableCell>
              <TableCell>{{ log.message }}</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </div>
    </div>
  </template>
  
  <style scoped>
  /* Adjust spacing and alignment */
  .flex-col.items-center > div {
    align-items: center;
  }
  
  .text-sm.mb-1 {
    margin-bottom: 4px;
  }
  </style>
  