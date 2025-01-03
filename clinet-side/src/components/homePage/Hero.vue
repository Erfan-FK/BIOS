<script setup>
import Button from '@/components/ui/button/Button.vue';
</script>

<template>
    <div>
        <!-- Hero Section -->
        <div class="relative h-screen">
            <img src="@\assets\bilkent-university-bg.jpg" alt="Bilkent University" class="w-full h-full object-cover opacity-80">
            <div class="absolute inset-0 bg-black bg-opacity-40 flex flex-col justify-center items-center">
                <h1 class="text-white text-5xl font-bold drop-shadow-lg mb-4">Discover Bilkent University</h1>
                <p class="text-white text-xl font-light drop-shadow-md mb-6">Explore our campus or join an online meeting with our team</p>
                <router-link to="/register" class="bg-red-600 hover:bg-red-700 text-white font-bold py-[0.6rem] px-6 rounded-full text-lg transition-all">
                  Request a Tour
                </router-link>
              </div>
        </div>
    </div>
</template>