<script setup>
import { onMounted } from "vue";
import { useReviewStore } from "@/stores/reviewStore";
import { Star } from "lucide-vue-next";

const reviewStore = useReviewStore();
const placeholderImage = "https://via.placeholder.com/150";

// Fetch reviews when the component is mounted
onMounted(() => {
  reviewStore.fetchReviews();
});
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <!-- Header -->
    <div class="p-6 border-b border-gray-300">
      <h2 class="text-xl font-bold">Tour Reviews</h2>
      <p class="text-md text-gray-600 mt-2">View reviews from participants.</p>
    </div>

    <!-- Grid List -->
    <div class="flex-grow overflow-y-auto p-6 bg-gray-50">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Review Card -->
        <div
          v-for="review in reviewStore.reviews"
          :key="review.id"
          class="bg-white rounded-lg shadow p-4 flex flex-col space-y-4"
        >
          <!-- Profile Image and Name -->
          <div class="flex items-center space-x-4">
            <img
              :src="review.reviewer?.user?.profile_picture || placeholderImage"
              alt="Reviewer"
              class="w-16 h-16 rounded-full object-cover"
            />
            <div>
              <p class="font-bold text-gray-900">{{ review.reviewer?.user?.name }}</p>
              <p class="text-sm text-gray-500 underline">
                {{ new Date(review.timestamp).toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                  year: "numeric",
                }) }}
              </p>
            </div>
          </div>

          <!-- Separator Line -->
          <hr class="border-gray-300" />

          <!-- Rating -->
          <div class="flex items-center space-x-1">
            <span class="font-semibold text-gray-900">{{ review.reviewRating.toFixed(1) }}</span>
            <Star class="w-5 h-5 text-yellow-500 fill-yellow-500" />
          </div>

          <!-- Review Comment -->
          <p class="text-sm text-gray-700">{{ review.review }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
