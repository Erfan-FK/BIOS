<script setup>
import { ref, defineProps, defineEmits } from "vue";
import { LogOut } from "lucide-vue-next";
import { useAuthStore } from "@/stores/authStore";
import { toast } from "vue-sonner";

const props = defineProps({
  items: {
    type: Array,
    required: true,
    default: () => [],
  },
  selectedItem: {
    type: String,
    default: "",
  },
});

const emit = defineEmits(["itemSelected"]);

const authStore = useAuthStore();

// State for logout confirmation dialog
const showLogoutDialog = ref(false);

// Function to handle item selection
const selectItem = (item) => {
  if (item.action === "logout") {
    showLogoutDialog.value = true; // Show the confirmation dialog
  } else {
    emit("itemSelected", item.name);
  }
};

// Function to confirm logout
const confirmLogout = async () => {
  try {
    await authStore.logout(); // Perform the logout action
    toast.success("Logged out successfully!");
    showLogoutDialog.value = false; // Close the dialog
  } catch (error) {
    toast.error("Failed to log out. Please try again.");
    console.error("Logout error:", error);
  }
};
</script>

<template>
  <aside
    class="fixed top-16 bottom-0 left-0 z-10 w-56 bg-white shadow-md rounded-br-lg p-4 flex flex-col"
  >
    <nav class="flex-1">
      <ul class="space-y-4 mt-4">
        <li
          v-for="item in [
            ...props.items,
            {
              name: 'logout',
              label: 'Log Out',
              icon: LogOut,
              action: 'logout',
            },
          ]"
          :key="item.name"
          @click="selectItem(item)"
          :class="[
            'flex items-center px-4 py-4 rounded-lg cursor-pointer transition-colors duration-200',
            props.selectedItem === item.name
              ? 'bg-red-100 text-red-700 shadow-md'
              : 'text-gray-700 hover:bg-red-600 hover:text-white',
          ]"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          {{ item.label }}
        </li>
      </ul>
    </nav>
    <!-- Confirmation Dialog -->
    <div
      v-if="showLogoutDialog"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-20"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full">
        <h2 class="text-lg font-bold mb-4">Confirm Logout</h2>
        <p class="text-gray-600 mb-6">Are you sure you want to log out?</p>
        <div class="flex justify-end gap-4">
          <button
            @click="showLogoutDialog = false"
            class="px-4 py-2 rounded bg-gray-200 hover:bg-gray-300 text-gray-700"
          >
            Cancel
          </button>
          <button
            @click="confirmLogout"
            class="px-4 py-2 rounded bg-red-600 hover:bg-red-700 text-white"
          >
            Log Out
          </button>
        </div>
      </div>
    </div>
    <!-- Profile Section -->
    <div
      class="flex items-center gap-4 px-4 py-4 rounded-lg bg-gray-100 shadow-sm mt-4"
    >
      <img
        :src="authStore.user.profilePicture"
        alt="Profile Picture"
        class="w-12 h-12 rounded-full border-2 border-red-700 object-cover"
      />
      <div class="flex-1">
        <p class="text-gray-900 text-sm font-bold">{{ authStore.user.name }}</p>
      </div>
    </div>
  </aside>
</template>
