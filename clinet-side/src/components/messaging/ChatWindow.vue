<script setup>
import { ref, computed, watch, nextTick, onMounted } from "vue";
import { useMessagingStore } from "@/stores/messagingStore.js";
import { useAuthStore } from "@/stores/authStore";
import { toast } from "vue-sonner";

const messagingStore = useMessagingStore();
const authStore = useAuthStore();
const newMessage = ref("");

// Reference to the message container
const messageContainer = ref(null);

// Scroll to bottom function
const scrollToBottom = () => {
  if (messageContainer.value) {
    messageContainer.value.scrollTo({
      top: messageContainer.value.scrollHeight,
      behavior: "smooth",
    });
  }
};

// On mounted, scroll to bottom
onMounted(() => {
  scrollToBottom();
});

// Compute activeChat
const activeChat = computed(() => {
  if (messagingStore.activeBroadcastId) {
    // Find the active broadcast message
    const broadcast = messagingStore.broadcastMessages.find(
      (msg) => msg.id === messagingStore.activeBroadcastId
    );
    if (broadcast) {
      return {
        isBroadcast: true,
        ...broadcast,
      };
    }
  }

  // Handle direct chats
  const chat = messagingStore.chats.find(
    (chat) => chat.id === messagingStore.activeChatId
  );
  if (chat) {
    return {
      isBroadcast: false,
      ...chat,
      user:
        authStore.user.id === chat.participant1.id
          ? chat.participant2
          : chat.participant1,
    };
  }
  return null;
});

// Sort messages chronologically
const sortedMessages = computed(() => {
  if (!activeChat.value || !activeChat.value.messages) return [];
  return activeChat.value.messages.slice().sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
});

// Watch for new messages to scroll to bottom
watch(
  () => activeChat.value?.messages?.length,
  async (newLength, oldLength) => {
    if (newLength > oldLength) {
      await nextTick();
      scrollToBottom();
    }
  }
);

// Watch for activeChat changes to scroll to bottom
watch(
  activeChat,
  async () => {
    await nextTick();
    scrollToBottom();
  }
);

// Handle sending messages
const handleSendMessage = async () => {
  if (newMessage.value.trim() === "") return;

  if (messagingStore.activeBroadcastId) {
    toast("Cannot send messages to broadcasts");
    return;
  }

  await messagingStore.sendMessage(
    activeChat.value.id,
    newMessage.value,
    "direct"
  );

  newMessage.value = "";
  await nextTick(scrollToBottom); // Ensure the new message is visible
};

// Format timestamp
const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString("en-US", {
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  });
};
</script>

<template>
  <div v-if="activeChat" class="flex flex-col h-full">
    <!-- Header -->
    <div class="flex items-center p-4 bg-red-600 text-white">
      <img
        v-if="activeChat.isBroadcast"
        :src="activeChat.sender.profile_picture"
        alt="Sender Avatar"
        class="w-10 h-10 rounded-full"
      />
      <img
        v-else
        :src="activeChat.user.profile_picture"
        alt="User Avatar"
        class="w-10 h-10 rounded-full"
      />
      <div class="ml-4 font-bold">
        {{ activeChat.isBroadcast ? activeChat.sender.name : activeChat.user.name }}
      </div>
    </div>

    <!-- Messages -->
    <div
      ref="messageContainer"
      class="flex-1 p-4 overflow-y-auto bg-white flex flex-col hide-scrollbar"
    >
      <div
        v-if="activeChat.isBroadcast"
        class="flex flex-col items-start mb-4 rounded-lg"
      >
        <p class="px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
          {{ activeChat.content }}
        </p>
        <div class="text-xs text-gray-500">
          {{ formatTimestamp(activeChat.timestamp) }}
        </div>
      </div>

      <!-- Use sortedMessages instead of activeChat.messages -->
      <div
        v-for="message in sortedMessages"
        :key="message.id"
        :class="[ 
          'flex flex-col mb-4 group',
          message.sender?.id === authStore.user.id ? 'items-end' : 'items-start',
        ]"
      >
        <div
          :class="[ 
            'px-4 py-2 rounded-lg',
            message.sender?.id === authStore.user.id
              ? 'bg-red-100 text-gray-800 rounded-br-lg'
              : 'bg-gray-200 text-gray-800 rounded-bl-lg',
          ]"
        >
          {{ message.content }}
        </div>
        <div class="text-xs text-gray-500 mt-1">
          {{ formatTimestamp(message.timestamp) }}
        </div>
      </div>
    </div>

    <!-- Input -->
    <div class="flex items-center p-4 bg-gray-100">
      <input
        v-model="newMessage"
        @keyup.enter="handleSendMessage"
        type="text"
        placeholder="Type a message"
        class="flex-1 p-2 border border-gray-300 rounded-full"
        :disabled="!!messagingStore.activeBroadcastId"
      />
      <button
        @click="handleSendMessage"
        class="ml-4 px-4 py-2 bg-red-600 text-white rounded-full hover:bg-red-700"
        :disabled="!!messagingStore.activeBroadcastId"
      >
        Send
      </button>
    </div>
  </div>
  <div
    v-else
    class="flex items-center justify-center h-full text-gray-600 text-lg"
  >
    Select a chat to start messaging
  </div>
</template>


<style>
/* Hide scrollbar for Chrome, Safari and Opera */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.hide-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

/* .flex-1 {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.flex.flex-col.gap-4 > div {
  transition: transform 0.2s ease-out, opacity 0.2s ease-in-out;
}

.flex.flex-col.gap-4 > div:hover {
  transform: scale(1.02);
} */
</style>