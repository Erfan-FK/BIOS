<script setup>
import { ref } from 'vue';
import requestTour from '@/components/visitorPage/RequestTour.vue';
import {CalendarCheck, UserPen, ClipboardList, Monitor} from 'lucide-vue-next';
import editProfile from "@/components/EditProfile.vue";
import trackTours from "@/components/visitorPage/TrackTours.vue";
import SidebarNav from '@/components/SidebarNav.vue';
// import PastTours from '@/components/visitorPage/PastTours.vue';
import { MessageCircle } from 'lucide-vue-next';
import Messaging from "@/components/messaging/Messaging.vue";
import RequestFair from '@/components/visitorPage/RequestFair.vue';

const visitorPageNavbarItems = [
  { name: "RequestTour", label: "Request Tour", icon: CalendarCheck },
  // { name: "PastTours", label: "Past Tours", icon: ClipboardList },
  { name: "Messages", label: "Messages", icon: MessageCircle },
  { name: "RequestFair", label: "Request Fair", icon: CalendarCheck },
  { name: "TrackTours", label: "Track Tours", icon: Monitor },
  { name: "EditProfile", label: "Edit Profile", icon: UserPen },
];

const currentComponent = ref("RequestTour");

const handleItemSelected = (selectedItem) => {
  currentComponent.value = selectedItem;
};

const componentsMap = {
  RequestTour: requestTour,
  Messages: Messaging,
  // PastTours: PastTours,
  TrackTours: trackTours,
  EditProfile: editProfile,
  RequestFair: RequestFair
}


</script>

<template>
    <div class="flex h-screen">
      <SidebarNav
          :items="visitorPageNavbarItems"
          :selectedItem="currentComponent"
          @itemSelected="handleItemSelected"
      />
      <div class="flex-1 ml-56 mt-16">
        <component :is="componentsMap[currentComponent]" />
      </div>
    </div>
  </template>