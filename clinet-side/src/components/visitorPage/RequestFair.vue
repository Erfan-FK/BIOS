<template>
  <section class="flex justify-center items-center mt-12">
    <div class="bg-white px-8 py-6 rounded-lg shadow-xl border border-gray-200 w-full max-w-lg">
      <div class="text-center mb-6">
        <h2 class="text-3xl font-bold">
          Request a <span class="text-red-600">Fair Invitation</span>
        </h2>
        <p class="text-gray-600 mt-2 text-sm">
          Fill out this form to request a Bilkent visit to your fair.
        </p>
      </div>

      <form class="space-y-4">
        <!-- Date Selection -->
        <div>
          <Label for="date" class="font-medium text-gray-700 text-sm">
            Select Date
          </Label>
          <Popover>
            <PopoverTrigger as-child>
              <Button
                variant="outline"
                class="w-full h-10 text-left"
                @click="popoverVisible = !popoverVisible"
              >
                <CalendarIcon class="mr-2" />
                {{ form.date ? format(new Date(form.date), "dd/MM/yyyy") : "Select a date" }}
              </Button>
            </PopoverTrigger>
            <PopoverContent class="w-auto p-0">
              <Calendar
                v-model="form.date"
                class="rounded-md border"
                mode="single"
                @change="popoverVisible = false"
              />
            </PopoverContent>
          </Popover>
        </div>

        <!-- Explanation -->
        <div>
          <Label for="explanation" class="font-medium text-gray-700 text-sm">
            Explanation
          </Label>
          <textarea
            id="explanation"
            v-model="form.explanation"
            placeholder="Provide details about the fair"
            class="w-full h-20 px-4 py-2 border rounded-lg"
          ></textarea>
        </div>

        <div class="flex justify-end">
          <Button
            type="submit"
            class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
            @click.prevent="submit"
          >
            Submit Request
          </Button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { format } from "date-fns";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { CalendarIcon } from "lucide-vue-next";
import { toast } from "vue-sonner";
import { useAuthStore } from "@/stores/authStore.js";
import { useFairStore } from "@/stores/fairStore.js";

const authStore = useAuthStore();
const fairStore = useFairStore();

const popoverVisible = ref(false);

const form = ref({
  date: null,
  explanation: "",
});

const resetForm = () => {
  form.value = {
    date: null,
    explanation: "",
  };
};

const submit = async () => {
  if (!form.value.date) {
    toast.error("Date is required.", {
      description: "Please select a date for the fair.",
    });
    return;
  }

  // Ensure the selected date is converted to a valid date
  const selectedDate = new Date(form.value.date);

  if (isNaN(selectedDate)) {
    toast.error("Invalid date.", {
      description: "Please select a valid date for the fair.",
    });
    return;
  }

  const payload = {
    date: selectedDate.toISOString().split("T")[0], // Format date as YYYY-MM-DD
    explanation: form.value.explanation || "",
  };

  console.log("Payload to send:", payload);

  try {
    // Call the store method to create a fair request
    await fairStore.createFairRequest(payload);

    toast.success("Fair request submitted successfully!");
    resetForm();
  } catch (err) {
    console.error("Failed to create fair invitation:", err);
    toast.error("Failed to create fair invitation", {
      description: "Please try again later.",
    });
  }
};
</script>
