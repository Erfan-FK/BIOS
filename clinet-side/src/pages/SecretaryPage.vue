<script setup>
import { ref } from 'vue';
import SidebarNav from '@/components/SidebarNav.vue';
import tourRequests from '@/components/secretaryPage/TourRequests.vue';
import regRequests from '@/components/secretaryPage/RegRequests.vue';
import CreateUser from '@/components/secretaryPage/ManageAccounts.vue';
// import logPage from '@/components/LogPage.vue';
import editProfile from "@/components/EditProfile.vue";
import Messaging from "@/components/messaging/Messaging.vue";
import {Briefcase, Vote, Captions, UserPen, MessageCircle} from 'lucide-vue-next';

const secretaryPageNavbarItems = [
  { name: "TourRequests", label: "Requested Tours", icon: Briefcase },
  { name: "RegRequests", label: "Requested Registrations", icon: Vote },
  { name: "Messages", label: "Messages", icon: MessageCircle },
  // { name: "LogPage", label: "Information Page", icon: Captions },
  { name: "CreateUser", label: "Manage Accounts", icon: Captions },
  {name: "EditProfile", label: "Edit Profile", icon: UserPen},
];

const currentComponent = ref("TourRequests");

const handleItemSelected = (selectedItem) => {
  currentComponent.value = selectedItem;
};

const componentsMap = {
    TourRequests: tourRequests,
    RegRequests: regRequests,
    Messages: Messaging,
    // LogPage: logPage,
    CreateUser: CreateUser,
    EditProfile: editProfile,
}
</script>

<template>
  <div class="flex h-screen">
    <SidebarNav
        :items="secretaryPageNavbarItems"
        :selectedItem="currentComponent"
        @itemSelected="handleItemSelected"
    />
    <div class="flex-1 ml-56 mt-16">
      <component :is="componentsMap[currentComponent]" />
    </div>
  </div>
</template>