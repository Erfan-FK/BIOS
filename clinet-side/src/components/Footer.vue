<script setup>
</script>

<template>
    <footer class="bg-gray-900 text-white py-8">
        <div
            class="container mx-auto flex justify-between items-center flex-col md:flex-row space-y-6 md:space-y-0 px-4 sm:px-8 md:px-16 lg:px-24">
            <!-- Left: Logo and University Info -->
            <div class="flex items-center space-x-4">
                <img src="@/assets/BilkentLogo.png" alt="Bilkent University Logo" class="w-16 h-16">
                <div>
                    <h3 class="text-xl font-semibold">Bilkent University</h3>
                    <p class="text-sm text-gray-300">Ankara, Turkey</p>
                    <p class="text-sm text-gray-300">info@bilkent.edu.tr</p>
                </div>
            </div>

            <!-- Right: Links -->
            <div class="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6">
                <a href="https://bilkent.edu.tr" target="_blank"
                    class="text-gray-400 hover:text-red-600 transition">University Homepage</a>
                <a href="/terms-of-service" class="text-gray-400 hover:text-red-600 transition">Terms of Service</a>
                <a href="/privacy-policy" class="text-gray-400 hover:text-red-600 transition">Privacy Policy</a>
                <a href="/copyright" class="text-gray-400 hover:text-red-600 transition">© 2024 Bilkent University</a>
            </div>
        </div>
    </footer>
</template>