<script setup>
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/userStore";
import SidebarNav from "@/components/SidebarNav.vue";
import Messaging from "@/components/messaging/Messaging.vue";
import UpcomingTours from "@/components/guidePage/UpcomingTours.vue";
import AvailabilitySchedule from "@/components/AvailabilitySchedule.vue";
import PastTours from "@/components/guidePage/PastTours.vue";
import EditProfile from "@/components/EditProfile.vue";
import Calendar from "@/components/Calendar.vue";
import Review from "@/components/guidePage/Review.vue";

import {
  Calendar as CalendarIcon,
  Star,
  Briefcase,
  MessageCircle,
  UserPen,
  CalendarCheck,
  ClipboardList,
} from "lucide-vue-next";

const userStore = useUserStore();
const currentComponent = ref("Schedule");

const guidePageNavbarItems = [
  { name: "Schedule", label: "Schedule", icon: CalendarIcon },
  { name: "UpcomingTours", label: "Upcoming Tours", icon: Briefcase },
  {name: "PastTours", label: "Past Tours", icon: ClipboardList},
  { name: "Messages", label: "Messages", icon: MessageCircle },
  { name: "AvailabilitySchedule", label: "Availability", icon: CalendarCheck },
  { name: "Review", label: "Reviews", icon: Star },
  { name: "EditProfile", label: "Edit Profile", icon: UserPen },
];

onMounted(() => {
  userStore.fetchProfile();
});

const handleItemSelected = (selectedItem) => {
  currentComponent.value = selectedItem;
};

const componentsMap = {
  Schedule: Calendar,
  UpcomingTours: UpcomingTours,
  PastTours: PastTours,
  Messages: Messaging,
  AvailabilitySchedule: AvailabilitySchedule,
  Review: Review,
  EditProfile: EditProfile,
};
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar with a fixed width -->
    <SidebarNav
      :items="guidePageNavbarItems"
      :selectedItem="currentComponent"
      @itemSelected="handleItemSelected"
    />

    <!-- Main content area that grows to fill the rest of the screen -->
    <div class="flex-grow ml-56 pt-16">
      <component :is="componentsMap[currentComponent]" />
    </div>
  </div>
</template>
