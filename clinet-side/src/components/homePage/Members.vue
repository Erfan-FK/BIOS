<script setup>
import { Github, Linkedin } from 'lucide-vue-next';
</script>

<template>
    <div class="bg-gray-100 py-16">
        <div class="container mx-auto">
            <h2 class="text-4xl font-bold text-center mb-12">Meet Our Team</h2>
            <div class="grid grid-cols-3 gap-8">
                <!-- First row of three members -->
                <div class="text-center">
                    <img src="https://via.placeholder.com/150" alt="Member 1"
                        class="w-40 h-40 rounded-full mx-auto mb-4 shadow-lg">
                    <h3 class="text-lg font-semibold">Team Member 1</h3>
                    <!-- Social icons -->
                    <div class="flex justify-center space-x-4 mt-2">
                        <a href="https://github.com/username" target="_blank">
                            <Github class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                        <a href="https://linkedin.com/in/username" target="_blank">
                            <Linkedin class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                    </div>
                </div>

                <div class="text-center">
                    <img src="https://via.placeholder.com/150" alt="Member 2"
                        class="w-40 h-40 rounded-full mx-auto mb-4 shadow-lg">
                    <h3 class="text-lg font-semibold">Team Member 2</h3>
                    <!-- Social icons -->
                    <div class="flex justify-center space-x-4 mt-2">
                        <a href="https://github.com/username2" target="_blank">
                            <Github class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                        <a href="https://linkedin.com/in/username2" target="_blank">
                            <Linkedin class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                    </div>
                </div>

                <div class="text-center">
                    <img src="https://via.placeholder.com/150" alt="Member 3"
                        class="w-40 h-40 rounded-full mx-auto mb-4 shadow-lg">
                    <h3 class="text-lg font-semibold">Team Member 3</h3>
                    <!-- Social icons -->
                    <div class="flex justify-center space-x-4 mt-2">
                        <a href="https://github.com/username3" target="_blank">
                            <Github class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                        <a href="https://linkedin.com/in/username3" target="_blank">
                            <Linkedin class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                    </div>
                </div>
            </div>

            <!-- Second row of two members -->
            <div class="grid grid-cols-2 gap-8 mt-12">
                <div class="text-center">
                    <img src="https://via.placeholder.com/150" alt="Member 4"
                        class="w-40 h-40 rounded-full mx-auto mb-4 shadow-lg">
                    <h3 class="text-lg font-semibold">Team Member 4</h3>
                    <!-- Social icons -->
                    <div class="flex justify-center space-x-4 mt-2">
                        <a href="https://github.com/username4" target="_blank">
                            <Github class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                        <a href="https://linkedin.com/in/username4" target="_blank">
                            <Linkedin class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                    </div>
                </div>

                <div class="text-center">
                    <img src="https://via.placeholder.com/150" alt="Member 5"
                        class="w-40 h-40 rounded-full mx-auto mb-4 shadow-lg">
                    <h3 class="text-lg font-semibold">Team Member 5</h3>
                    <!-- Social icons -->
                    <div class="flex justify-center space-x-4 mt-2">
                        <a href="https://github.com/username5" target="_blank">
                            <Github class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                        <a href="https://linkedin.com/in/username5" target="_blank">
                            <Linkedin class="text-red-600 w-6 h-6 hover:text-red-700" />
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
