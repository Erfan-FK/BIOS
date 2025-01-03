<script setup>
import ChatList from "@/components/messaging/ChatList.vue";
import ChatWindow from "@/components/messaging/ChatWindow.vue";
</script>

<template>
  <div class="flex h-full">
    <div class="w-1/3 border-r border-gray-200">
      <ChatList />
    </div>
    <div class="flex-1">
      <ChatWindow />
    </div>
  </div>
</template>
