<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useAuthStore } from "@/stores/authStore";

const lastScroll = ref(0);
const isHeaderVisible = ref(true);

const authStore = useAuthStore();

const userProfileRoute = computed(() => {
  if (!authStore.userRole) return "/"; // Fallback to home if role is undefined

  const roleRouteMap = {
    guide: "/guide",
    advisor: "/advisor",
    secretary: "/secretary",
    director: "/director",
    visitor: "/visitor",
  };

  return roleRouteMap[authStore.userRole] || "/";
});

const handleScroll = () => {
  const currentScroll = window.pageYOffset;

  if (currentScroll <= 0) {
    isHeaderVisible.value = true;
  } else if (currentScroll > lastScroll.value) {
    isHeaderVisible.value = false;
  } else {
    isHeaderVisible.value = true;
  }

  lastScroll.value = currentScroll;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
</script>

<template>
  <header
    :class="[
      'bg-red-700 fixed w-full top-0 left-0 z-50 transition-transform duration-300',
      { '-translate-y-full': !isHeaderVisible },
    ]"
  >
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between py-4">
        <!-- Left: App Name -->
        <div class="flex items-center gap-4">
          <router-link to="/" class="text-white text-2xl font-bold">
            Bilkent Information System
          </router-link>
        </div>

        <!-- Right: Navigation and Auth -->
        <div class="hidden md:flex md:items-center md:gap-6">
          <!-- Auth Section -->
          <div class="flex items-center gap-6">
            <template v-if="!authStore.isLoggedIn">
              <!-- Logged-Out State -->
              <router-link
                to="/login"
                class="text-zinc-300 font-bold transition hover:text-white flex items-center gap-1"
              >
                Log In
              </router-link>
            </template>
            <template v-else>
              <!-- Logged-In State: Profile Section -->
              <router-link
                :to="userProfileRoute"
                class="flex items-center gap-3 px-2 rounded-md transition-colors duration-300 hover:bg-red-600 cursor-pointer"
              >
                <!-- Profile Picture -->
                <img
                  :src="authStore.user.profilePicture"
                  alt="Profile"
                  class="w-10 h-10 rounded-full object-cover border-2 border-transparent"
                />

                <!-- User Information -->
                <div class="flex flex-col">
                  <!-- User Name -->
                  <span class="font-semibold text-white">
                    {{ authStore.user.name }}
                  </span>
                  <!-- User Role -->
                  <span class="text-sm text-gray-200">
                    {{ authStore.user.role }}
                  </span>
                </div>
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
