<script setup>
import { ref } from "vue";
import SidebarNav from "@/components/SidebarNav.vue";
import DataPage from "@/components/directorPage/DataPage.vue";
import editProfile from "@/components/EditProfile.vue";
import FairRequests from "@/components/directorPage/FairRequests.vue";
import FairCalendar from "@/components/directorPage/FairCalendar.vue";
import Messaging from "@/components/messaging/Messaging.vue";
import { UserPen, Database, CalendarIcon, Briefcase, MessageCircle } from "lucide-vue-next";

// State to manage the current component
const currentComponent = ref("DataPage");

// Function to handle sidebar item selection
const handleItemSelected = (selectedItem) => {
  currentComponent.value = selectedItem;
};

// Map of components for dynamic rendering
const componentsMap = {
  DataPage: DataPage,
  Messages: Messaging,
  FairRequests: FairRequests,
  FairCalendar: FairCalendar,
  EditProfile: editProfile,
};

// Navbar items for the director page sidebar
const directorPageNavbarItems = [
  { name: "FairCalendar", label: "Fair Calendar", icon: CalendarIcon },
  { name: "FairRequests", label: "Fair Requests", icon: Briefcase },
  { name: "DataPage", label: "Data Page", icon: Database },
  { name: "Messages", label: "Messages", icon: MessageCircle },
  { name: "EditProfile", label: "Edit Profile", icon: UserPen },
];
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <SidebarNav :items="directorPageNavbarItems" :selectedItem="currentComponent" @itemSelected="handleItemSelected" />
    <div class="flex-grow ml-56 mt-16">
      <component :is="componentsMap[currentComponent]" />
    </div>
  </div>
</template>

<style>
/* Add styles for this page if needed */
</style>
