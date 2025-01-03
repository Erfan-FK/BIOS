<script setup>
import { ref } from 'vue';
import HeatMap from '@/components/directorPage/HeatMapTurkey.vue';
import PieChart from './PieChart.vue';
import RowBarChart from './RowBarChart.vue';
import GeneralOverview from './GeneralOverview.vue';
import ScholarshipDist from './ScholarshipDist.vue';
import LoyaltyAnalysis from './LoyaltyAnalysis.vue';
import AcademicExcellence from './AcademicExcellence.vue';
import YearlyTrends from './YearlyTrends.vue';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import Button from '../ui/button/Button.vue';

const selectedDataRepresentation = ref("GeneralOverview");

const componentsMap = {
  HeatMap: HeatMap,
  PieChart: PieChart,
  RowBarChart: RowBarChart,
  GeneralOverview: GeneralOverview,
  ScholarshipDist: ScholarshipDist,
  LoyaltyAnalysis: LoyaltyAnalysis,
  AcademicExcellence: AcademicExcellence,
  YearlyTrends: YearlyTrends
};

const representationLabels = {
  HeatMap: "Heat Map",
  PieChart: "Pie Chart",
  RowBarChart: "Row Bar Chart",
};
</script>

<template>
  <div class="flex flex-col  justify-center h-full w-full">
    <div class="p-4">
      <h1 class="text-xl font-bold">{{ representationLabels[selectedDataRepresentation] }}</h1>
    </div>
    <div class="flex items-center justify-center pt-5">
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button variant="outline">
            Select Data Representation
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56">
          <DropdownMenuLabel>Data Representations</DropdownMenuLabel>
          <DropdownMenuSeparator/>
          <DropdownMenuRadioGroup v-model="selectedDataRepresentation">
            <DropdownMenuRadioItem value="GeneralOverview">
              General Overview
            </DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="HeatMap">
              Heat Map
            </DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="ScholarshipDist">
              Scholarship Distribution
            </DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="LoyaltyAnalysis">
              Loyalty Analysis
            </DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="AcademicExcellence">
              Academic Excellence
            </DropdownMenuRadioItem>
            <DropdownMenuRadioItem value="YearlyTrends">
              Yearly Trends
            </DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
    <div class="mt-8 w-full h-full">
      <component :is="componentsMap[selectedDataRepresentation]" />
    </div>
  </div>
</template>