      <!-- src/components/FilterModal.vue -->
      <template>
          <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
            <div class="bg-white w-11/12 md:w-1/2 lg:w-1/3 p-6 rounded shadow-lg">
              <!-- Modal Header -->
              <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold">Filter Options</h2>
                <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700 text-2xl leading-none">
                  &times;
                </button>
              </div>
              <!-- Modal Body -->
              <div>
                <!-- Future Filter Content Goes Here -->
                <p class="text-gray-500">Filter content will be here.</p>
              </div>
              <!-- Modal Footer (Optional) -->
              <div class="mt-4 flex justify-end">
                <button @click="$emit('close')" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                  Close
                </button>
              </div>
            </div>
          </div>
        </template>
  
  <script>
  export default {
      name: 'FilterModal',
    };
  </script>
  
  <style scoped>
  /* Optional: Add any scoped styles if needed */
  </style>