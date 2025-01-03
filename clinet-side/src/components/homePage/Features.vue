<script setup>
import { MapPin, Video, Monitor, Clipboard } from 'lucide-vue-next';
</script>

<template>
    <section class="bg-gray-50 py-16">
        <div class="container mx-auto px-4 sm:px-8 md:px-16 lg:px-24">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-12">Our Features</h2>

            <!-- Campus Tours Feature -->
            <div class="flex flex-col md:flex-row items-center mb-12">
                <div class="w-full md:w-1/2">
                    <img src="@\assets\bilkent-spring.jpg" alt="Campus Tours" class="rounded-lg shadow-lg">
                </div>
                <div class="w-full md:w-1/2 md:pl-12 mt-6 md:mt-0">
                    <div class="flex items-center gap-4 mb-4">
                        <MapPin class="w-8 h-8 text-red-600" />
                        <h3 class="text-2xl font-semibold text-gray-900">Campus Tours</h3>
                    </div>
                    <p class="text-gray-700">
                        Explore Bilkent University’s stunning campus with a student guide. Get familiar with our
                        academic buildings, dormitories, and the vibrant campus life. Our guides will take you
                        through the most important landmarks, answering your questions along the way.
                    </p>
                </div>
            </div>

            <!-- Online Meetings Feature -->
            <div class="flex flex-col md:flex-row-reverse items-center mb-12">
                <div class="w-full md:w-1/2">
                    <img src="@\assets\bilkent-spring.jpg" alt="Online Meetings" class="rounded-lg shadow-lg">
                </div>
                <div class="w-full md:w-1/2 md:pr-12 mt-6 md:mt-0">
                    <div class="flex items-center gap-4 mb-4">
                        <Video class="w-8 h-8 text-red-600" />
                        <h3 class="text-2xl font-semibold text-gray-900">Online Meetings</h3>
                    </div>
                    <p class="text-gray-700">
                        Can’t visit the campus in person? No problem! Schedule an online meeting with one of our student
                        guides.
                        These 40-60 minute virtual sessions provide a personalized overview of the university and allow
                        you to
                        ask any questions about life at Bilkent, academic programs, or anything else.
                    </p>
                </div>
            </div>

            <!-- Virtual Tour Feature -->
            <div class="flex flex-col md:flex-row items-center mb-12">
                <div class="w-full md:w-1/2">
                    <img src="@\assets\bilkent-spring.jpg" alt="Virtual Tour" class="rounded-lg shadow-lg">
                </div>
                <div class="w-full md:w-1/2 md:pl-12 mt-6 md:mt-0">
                    <div class="flex items-center gap-4 mb-4">
                        <Monitor class="w-8 h-8 text-red-600" />
                        <h3 class="text-2xl font-semibold text-gray-900">Virtual Tour</h3>
                    </div>
                    <p class="text-gray-700">
                        Experience Bilkent University like never before with our immersive 360-degree virtual tour.
                        Explore our facilities and campus from the comfort of your home and gain an understanding
                        of what it’s like to study at Bilkent University.
                    </p>
                </div>
            </div>

            <!-- Office Tasks Management Feature -->
            <div class="flex flex-col md:flex-row-reverse items-center">
                <div class="w-full md:w-1/2">
                    <img src="@\assets\bilkent-spring.jpg" alt="Office Tasks Management"
                        class="rounded-lg shadow-lg">
                </div>
                <div class="w-full md:w-1/2 md:pr-12 mt-6 md:mt-0">
                    <div class="flex items-center gap-4 mb-4">
                        <Clipboard class="w-8 h-8 text-red-600" />
                        <h3 class="text-2xl font-semibold text-gray-900">Office Tasks Management</h3>
                    </div>
                    <p class="text-gray-700">
                        Our office tasks management feature allows advisors, coordinators, and guides to efficiently
                        manage tour requests and assignments. With this system, you can seamlessly organize tours,
                        track schedules, and ensure everything runs smoothly.
                    </p>
                </div>
            </div>
        </div>
    </section>
</template>
