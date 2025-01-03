<script setup>
</script>

<template>
    <div class="bg-gray-100 py-16 px-4 sm:px-8 md:px-16 lg:px-24">
        <div class="max-w-4xl mx-auto">
            <h2 class="text-4xl font-bold text-center text-gray-900 mb-10">Frequently Asked Questions</h2>

            <div class="space-y-6">
                <!-- FAQ 1 -->
                <details
                    class="group border-l-4 border-red-600 bg-white p-6 shadow-sm rounded-lg [&_summary::-webkit-details-marker]:hidden">
                    <summary class="flex cursor-pointer items-center justify-between gap-1.5">
                        <h3 class="text-lg font-semibold text-gray-900">How can I request a campus tour?</h3>
                        <span
                            class="shrink-0 rounded-full bg-white p-1.5 text-gray-900 transition duration-300 group-open:rotate-45">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                            </svg>
                        </span>
                    </summary>

                    <p class="mt-4 leading-relaxed text-gray-700">
                        You can request a campus tour by navigating to the 'Request a Tour' section. Select your
                        preferred date and time,
                        and submit your request. Our team will confirm the tour details with you shortly after.
                    </p>
                </details>

                <!-- FAQ 2 -->
                <details
                    class="group border-l-4 border-red-600 bg-white p-6 shadow-sm rounded-lg [&_summary::-webkit-details-marker]:hidden">
                    <summary class="flex cursor-pointer items-center justify-between gap-1.5">
                        <h3 class="text-lg font-semibold text-gray-900">Can I schedule an online tour instead?</h3>
                        <span
                            class="shrink-0 rounded-full bg-white p-1.5 text-gray-900 transition duration-300 group-open:rotate-45">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                            </svg>
                        </span>
                    </summary>

                    <p class="mt-4 leading-relaxed text-gray-700">
                        Yes, you can opt for an online tour. Choose the 'Online Tour' option when filling out the
                        request form. You'll
                        have the option to connect via Zoom or Google Meet at a time of your choosing.
                    </p>
                </details>

                <!-- FAQ 3 -->
                <details
                    class="group border-l-4 border-red-600 bg-white p-6 shadow-sm rounded-lg [&_summary::-webkit-details-marker]:hidden">
                    <summary class="flex cursor-pointer items-center justify-between gap-1.5">
                        <h3 class="text-lg font-semibold text-gray-900">Who will guide my tour?</h3>
                        <span
                            class="shrink-0 rounded-full bg-white p-1.5 text-gray-900 transition duration-300 group-open:rotate-45">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor" stroke-width="2">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
                            </svg>
                        </span>
                    </summary>

                    <p class="mt-4 leading-relaxed text-gray-700">
                        Your tour will be guided by a current Bilkent University student who is knowledgeable about the
                        campus and can
                        answer any questions you have. Each tour is designed to give you a personalized experience.
                    </p>
                </details>
            </div>
        </div>
    </div>
</template>