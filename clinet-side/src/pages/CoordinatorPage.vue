<script setup>
import { ref } from 'vue';
import SidebarNav from '@/components/SidebarNav.vue';
import guides from "@/components/advisorPage/Guides.vue";
import pastTours from "@/components/advisorPage/PastTours.vue";
import editProfile from "@/components/EditProfile.vue";
import scheduleTours from "@/components/advisorPage/ScheduleTours.vue";
import Messaging from "@/components/messaging/Messaging.vue";
import UpcomingTours from "@/components/advisorPage/UpcomingTours.vue";
import {Briefcase, CalendarCheck, Calendar, Frame, UserPen, MessageCircle} from 'lucide-vue-next';

const coordinatorPageNavbarItems = [
  { name: "UpcomingTours", label: "Upcoming Tours", icon: Briefcase },
  { name: "ScheduleTours", label: "Schedule Tours", icon: Calendar },
  { name: "Messages", label: "Messages", icon: MessageCircle },
  { name: "PastTours", label: "Past Tours", icon: Frame },
  { name: "EditProfile", label: "Edit Profile", icon: UserPen },
  { name: "Guides", label: "Guides", icon: CalendarCheck },
];

const currentComponent = ref("UpcomingTours");

const handleItemSelected = (selectedItem) => {
  currentComponent.value = selectedItem;
};

const componentsMap = {
  UpcomingTours: UpcomingTours,
  PastTours: pastTours,
  Messages: Messaging,
  ScheduleTours: scheduleTours,
  Guides: guides,
  EditProfile: editProfile,
}
const coordinatorId = ref(0);
</script>

<template>
  <div class="flex h-screen">
    <SidebarNav
        :items="coordinatorPageNavbarItems"
        :selectedItem="currentComponent"
        @itemSelected="handleItemSelected"
    />
    <div class="flex-1 ml-56 mt-16">
      <component :is="componentsMap[currentComponent]" />
    </div>
  </div>
  <div class="absolute bottom-0 left-0">
    <input
        v-model="coordinatorId"
        type="number" />
  </div>
</template>