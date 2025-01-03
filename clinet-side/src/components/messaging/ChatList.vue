<script setup>
import { ref, computed, onMounted } from "vue";
import { useMessagingStore } from "@/stores/messagingStore.js";
import { useAuthStore } from "@/stores/authStore.js";
import Button from "../ui/button/Button.vue";
import { toast } from "vue-sonner";

const messagingStore = useMessagingStore();
const authStore = useAuthStore();

const activeChatId = computed(() => messagingStore.activeChatId);
const searchQuery = ref("");
const selectedFilter = ref("All");
const showNewChatModal = ref(false);
const showBroadcastModal = ref(false);
const broadcastMessage = ref("");
const selectedContacts = ref([]);

onMounted(async () => {
  if (authStore.user?.id) {
    await messagingStore.fetchChatsForUser(authStore.user.id); // Fetch all chats for the current user
    await messagingStore.fetchBroadcastMessages(); // Fetch all broadcast messages
  }
});

// Contacts for the new chat or broadcast modal
const contacts = computed(() => {
  return messagingStore.contactsList.filter(
    (contact) => contact.id !== authStore.user.id
  );
});

// Filtered and sorted chats
const filteredChats = computed(() => {
  const allChats = [
    ...messagingStore.chats,
    ...messagingStore.broadcastMessages
      .filter((msg) => msg.sender.id !== authStore.user.id) // Exclude broadcasts sent by the current user
      .map((msg) => ({
        id: msg.id,
        isBroadcast: true,
        name: "Broadcast",
        timestamp: msg.timestamp,
        content: msg.content,
        message: msg,
      })),
  ];

  return allChats
    .filter((chat) => {
      // Handle search query filtering
      const matchesSearchQuery = chat.isBroadcast
        ? chat.content.toLowerCase().includes(searchQuery.value.toLowerCase())
        : chat.participant1?.name
            .toLowerCase()
            .includes(searchQuery.value.toLowerCase()) ||
          chat.participant2?.name
            .toLowerCase()
            .includes(searchQuery.value.toLowerCase());

      if (!matchesSearchQuery) return false;

      // Apply selected filter
      if (selectedFilter.value === "Broadcast") {
        return chat.isBroadcast;
      } 
      if (selectedFilter.value === "Direct") {
        return !chat.isBroadcast;
      }

      return true; // Default: include all chats
    })
    .sort((a, b) => {
      // Sort by the latest timestamp
      const aTimestamp = new Date(a.timestamp || a.created_at);
      const bTimestamp = new Date(b.timestamp || b.created_at);
      return bTimestamp - aTimestamp;
    });
});

// Select an existing chat
const selectChat = async (chatId, isBroadcast = false) => {
  if (isBroadcast) {
    messagingStore.setActiveBroadcast(chatId); // Set the active broadcast message
  } else {
    messagingStore.setActiveChat(chatId); // Set the active direct chat
  }
};

// Broadcast message sending logic
const sendBroadcastMessage = async () => {
  try {
    await messagingStore.sendMessage(
      null,
      broadcastMessage.value,
      "broadcast",
      selectedContacts.value
    );
    toast("Broadcast message sent successfully!");
    closeBroadcastModal();
  } catch (error) {
    console.error("Error sending broadcast message:", error);
    toast("Failed to send broadcast message. Please try again later.");
  }
};

const toggleContactSelection = (contactId) => {
  if (selectedContacts.value.includes(contactId)) {
    selectedContacts.value = selectedContacts.value.filter(
      (id) => id !== contactId
    );
  } else {
    selectedContacts.value.push(contactId);
  }
};

const openNewChatModal = async () => {
  showNewChatModal.value = true;
  await messagingStore.fetchContacts();
};

const closeNewChatModal = () => {
  showNewChatModal.value = false;
};

const openBroadcastModal = async () => {
  showBroadcastModal.value = true;
  await messagingStore.fetchContacts();
};

const closeBroadcastModal = () => {
  showBroadcastModal.value = false;
  broadcastMessage.value = "";
  selectedContacts.value = [];
};

const createNewChat = async (contactId) => {
  const existingChat = messagingStore.chats.find((chat) => {
    return (
      (chat.participant1.id === contactId &&
        chat.participant2.id === authStore.user.id) ||
      (chat.participant2.id === contactId &&
        chat.participant1.id === authStore.user.id)
    );
  });

  if (existingChat) {
    toast("Chat already exists with this contact.");
    closeNewChatModal();
    return;
  }

  // Create a new chat if none exists
  try {
    await messagingStore.createChat(contactId);
    toast("New chat started successfully!");
    closeNewChatModal();
  } catch (error) {
    console.error("Error creating new chat:", error);
  }
};
</script>

<template>
  <div class="flex flex-col h-full bg-gray-100 text-gray-800">
    <!-- Header -->
    <div class="p-4 border-b border-red-600 flex justify-between items-center">
      <h1 class="text-xl font-bold text-black">Chats</h1>
      <div class="flex items-center space-x-4">
        <!-- New Chat Button -->
        <Button
          class="w-8 h-8 flex items-center justify-center bg-red-500 text-white rounded-full"
          @click="openNewChatModal"
        >
          +
        </Button>
        <!-- New Broadcast Button -->
        <Button
          class="px-4 py-2 bg-red-500 text-white rounded-lg"
          @click="openBroadcastModal"
        >
          New Broadcast
        </Button>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="p-4">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Search or start new chat"
        class="w-full p-2 rounded-lg bg-gray-200 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500"
      />
    </div>

    <!-- Filters -->
    <div class="p-4 flex space-x-2">
      <button
        v-for="filter in ['All', 'Broadcast', 'Direct']"
        :key="filter"
        @click="selectedFilter = filter"
        :class="[
          'px-4 py-2 rounded-full border',
          selectedFilter === filter
            ? 'bg-red-500 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
        ]"
      >
        {{ filter }}
      </button>
    </div>

    <!-- Chat List -->
    <div
      class="overflow-y-auto h-full no-scrollbar bg-white flex-1 border-t border-gray-300"
    >
      <div
        v-for="chat in filteredChats"
        :key="chat.id"
        @click="selectChat(chat.id, chat.isBroadcast)"
        :class="[
          'flex items-center p-4 cursor-pointer transition-colors duration-200',
          chat.id === activeChatId ||
          (chat.isBroadcast && chat.id === messagingStore.activeBroadcastId)
            ? 'bg-red-100 border-l-4 border-red-500'
            : 'hover:bg-gray-100',
        ]"
      >
        <!-- Profile Picture or Broadcast Icon -->
        <img
          v-if="!chat.isBroadcast"
          :src="
            chat.participant1.id !== authStore.user.id
              ? chat.participant1.profile_picture
              : chat.participant2.profile_picture
          "
          alt="Avatar"
          class="w-12 h-12 rounded-full"
        />
        <div
          v-else
          class="w-12 h-12 rounded-full bg-red-500 text-white flex items-center justify-center font-bold"
        >
          B
        </div>

        <!-- Chat Info -->
        <div class="ml-4 flex-1">
          <div class="flex justify-between items-center">
            <div class="font-bold text-gray-800">
              {{
                chat.isBroadcast
                  ? "Broadcast"
                  : chat.participant1.id !== authStore.user.id
                  ? chat.participant1.name
                  : chat.participant2.name
              }}
            </div>
            <!-- Broadcast Label -->
            <div
              v-if="chat.isBroadcast"
              class="text-xs bg-red-200 text-red-800 px-2 py-1 rounded-full"
            >
              Broadcast
            </div>
          </div>
          <div class="text-gray-600 text-sm">
            {{
              chat.isBroadcast
                ? chat.content
                : chat.messages?.slice(-1)[0]?.content
            }}
          </div>
        </div>
      </div>
    </div>

    <!-- New Chat Modal -->
    <div
      v-if="showNewChatModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-2/3 max-w-lg">
        <h2 class="text-xl font-bold mb-4 text-gray-800">Start New Chat</h2>
        <div class="h-64 overflow-y-auto no-scrollbar">
          <div
            v-for="contact in contacts"
            :key="contact.id"
            class="p-4 mb-2 rounded-lg cursor-pointer bg-gray-100 hover:bg-gray-200 flex items-center gap-4"
            @click="createNewChat(contact.id), closeNewChatModal()"
          >
            <!-- Profile Picture -->
            <img
              :src="contact.profile_picture"
              alt="Profile Picture"
              class="w-12 h-12 rounded-full object-cover"
            />
            <!-- User Details -->
            <div>
              <p class="font-bold">{{ contact.name }}</p>
              <p class="text-sm text-gray-500">{{ contact.email }}</p>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <Button
            class="font-bold px-4 py-2 rounded bg-red-500 text-white h-10 w-24"
            @click="closeNewChatModal"
          >
            Close
          </Button>
        </div>
      </div>
    </div>

    <!-- Broadcast Modal -->
    <div
      v-if="showBroadcastModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-2/3 max-w-lg">
        <h2 class="text-xl font-bold mb-4 text-gray-800">
          Send Broadcast Message
        </h2>
        <div class="mb-4">
          <textarea
            v-model="broadcastMessage"
            placeholder="Type your broadcast message here..."
            class="w-full p-2 rounded-lg bg-gray-200 text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-red-500"
            rows="4"
          ></textarea>
        </div>
        <div class="h-64 overflow-y-auto no-scrollbar mb-4">
          <div
            v-for="contact in contacts"
            :key="contact.id"
            :class="[
              'p-4 mb-2 rounded-lg cursor-pointer flex items-center gap-4',
              selectedContacts.includes(contact.id)
                ? 'bg-red-500 text-white'
                : 'bg-gray-100 hover:bg-gray-200',
            ]"
            @click="toggleContactSelection(contact.id)"
          >
            <!-- Profile Picture -->
            <img
              :src="contact.profile_picture"
              alt="Profile Picture"
              class="w-12 h-12 rounded-full object-cover"
            />
            <!-- Contact Details -->
            <div>
              <p class="font-bold">{{ contact.name }}</p>
              <p
                class="text-sm"
                :class="
                  selectedContacts.includes(contact.id)
                    ? 'text-white'
                    : 'text-gray-500'
                "
              >
                {{ contact.role }}
              </p>
            </div>
          </div>
        </div>
        <div class="mt-6 flex justify-end space-x-2">
          <Button class="px-4 py-2 rounded" @click="closeBroadcastModal">
            Cancel
          </Button>
          <Button
            class="px-4 py-2 rounded bg-red-500 text-white"
            :disabled="!broadcastMessage || selectedContacts.length === 0"
            @click="sendBroadcastMessage"
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
