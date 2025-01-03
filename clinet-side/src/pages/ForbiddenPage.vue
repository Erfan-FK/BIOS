<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">

    <!-- Main Content -->
    <div class="flex flex-col items-center justify-center px-4 py-12 md:py-24">
      <!-- Image -->
      <img
        src="@/assets/shalnotpass.jpg"
        alt="Access Denied"
        class="w-64 h-64 object-contain mb-8 animate-pulse"
      />

      <!-- Title -->
      <h1 class="text-5xl font-extrabold text-red-600 mb-4">
        403 Forbidden
      </h1>

      <!-- Funny Message -->
      <p class="text-lg text-gray-700 mb-6 text-center max-w-md">
        Oops! It seems like you've tried to enter a restricted area. Maybe you need the magic password?
      </p>

      <!-- Navigation Button -->
      <router-link to="/" class="inline-block px-6 py-3 bg-red-600 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 transition duration-300">
        Take Me Home
      </router-link>
    </div>
  </div>
</template>
