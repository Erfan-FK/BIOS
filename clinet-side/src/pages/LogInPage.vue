<script setup>
import Button from "@/components/ui/button/Button.vue";
import Input from "@/components/ui/input/Input.vue";
import { IdCard, Eye, EyeOff } from "lucide-vue-next";
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useRouter } from "vue-router";

const router = useRouter();
const authStore = useAuthStore();
const email = ref("");
const password = ref("");
const forgotPassword = ref(false);
const passwordVisible = ref(false);

onMounted(() => {
  if (authStore.isLoggedIn) {
    router.push(`/${authStore.userRole}`);
  }
});

const toggleForgotPassword = () => {
  forgotPassword.value = !forgotPassword.value;
};

const handleSubmit = async () => {
  try {
    await authStore.login(email.value, password.value);
  } catch (error) {
    alert("Invalid credentials");
  }
};

const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};
</script>

<template>
  <section class="relative flex flex-wrap h-screen items-center bg-gray-200">
    <!-- Form Section -->
    <div class="w-1/2 px-8 py-24">
      <div
        class="mx-auto max-w-lg bg-white p-8 rounded-lg shadow-xl border border-gray-200"
      >
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold">
            Welcome Back to <span class="text-red-600">BIOS</span>
          </h1>
          <p class="mt-4 text-gray-600">
            Sign in with your credentials to manage tasks within the Bilkent
            Information System.
          </p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label for="email" class="sr-only">Email</label>
            <div class="relative">
              <Input
                type="email"
                id="email"
                v-model="email"
                class="w-full h-12 rounded-lg border-gray-300 p-4 pr-12 text-base shadow focus:ring-2 focus:ring-blue-400"
                placeholder="Email"
              />
              <span
                class="absolute inset-y-0 right-0 grid place-content-center pr-4"
              >
                <IdCard
                  class="w-5 h-5"
                  :class="email ? 'text-black' : 'text-gray-400'"
                />
              </span>
            </div>
          </div>

          <div v-if="!forgotPassword">
            <label for="password" class="sr-only">Password</label>
            <div class="relative">
              <Input
                :type="passwordVisible ? 'text' : 'password'"
                id="password"
                v-model="password"
                class="w-full h-12 rounded-lg border-gray-300 p-4 pr-12 text-base shadow focus:ring-2"
                placeholder="Password"
              />
              <span
                @click="togglePasswordVisibility"
                class="absolute inset-y-0 right-0 grid place-content-center pr-4 cursor-pointer"
              >
                <Eye
                  v-if="!passwordVisible"
                  class="w-5 h-5"
                  :class="password ? 'text-black' : 'text-gray-400'"
                />
                <EyeOff
                  v-else
                  class="w-5 h-5"
                  :class="password ? 'text-black' : 'text-gray-400'"
                />
              </span>
            </div>
          </div>

          <div class="flex flex-col gap-4">
            <Button
              class="rounded-lg bg-red-600 px-5 py-3 text-white shadow hover:bg-red-700 font-bold"
              type="submit"
              variant="link"
            >
              {{ forgotPassword ? "Send Reset Link" : "Sign In" }}
            </Button>
            <Button
                variant="link"
                type="button"
                @click="toggleForgotPassword"
                class="text-red-600 hover:text-red-700 text-sm self-center"
            >
              {{ forgotPassword ? "Back to Login" : "Forgot Password?" }}
            </Button>
            <p class="text-sm text-left">
              Don't have an account?
              <router-link
                to="/register"
                class="text-red-600 hover:text-red-700 font-bold"
              >
                Sign Up
              </router-link>
            </p>
          </div>
        </form>
      </div>
    </div>

    <!-- Image Section -->
    <div class="relative h-64 w-full sm:h-96 lg:h-full lg:w-1/2">
      <img
        alt="Bilkent Campus"
        src="@/assets/ihsan-statue.png"
        class="absolute inset-0 h-full w-full object-cover filter brightness-75 contrast-125 saturate-125 shadow-2xl"
      />
    </div>
  </section>
</template>

<style scoped>
/* Add any additional styles if needed */
</style>