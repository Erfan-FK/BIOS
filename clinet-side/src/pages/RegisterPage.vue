<script setup>
import { ref, computed } from "vue";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectValue,
} from "@/components/ui/select";

// Import Dialog Components
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "vue-sonner";

import regRequestController from "@/controllers/regRequestController";

const form = ref({
  name: "",
  email: "",
  phone: "",
  userType: "individual",
  city: "",
  highSchool: "",
});

// Data for Select Inputs
const cities = ["Ankara", "Istanbul", "Izmir"];
const highSchools = {
  Ankara: ["Bilkent High School", "TED Ankara College", "Ankara Fen Lisesi"],
  Istanbul: ["Robert College", "Galatasaray High School", "Istanbul High School"],
  Izmir: ["Izmir American College", "Bornova Anadolu Lisesi", "Izmir Science High School"],
};

const filteredHighSchools = computed(() => {
  return form.value.city ? highSchools[form.value.city] || [] : [];
});

const isHighSchoolDisabled = computed(() => !form.value.city);

const resetForm = () => {
  form.value = {
    name: "",
    email: "",
    phone: "",
    userType: "individual",
    city: "",
    highSchool: "",
  };
};

const showConfirmDialog = ref(false);

const submitForm = () => {
  showConfirmDialog.value = true;
};

const confirmSubmit = async () => {
  try {
    const data = {
      name: form.value.name,
      email: form.value.email,
      phone_no: form.value.phone,
      user_type: form.value.userType,
      high_school_name: form.value.highSchool,
      city: form.value.city,
    };
    await regRequestController.createRegRequest(data);
    resetForm();
    showConfirmDialog.value = false;
    toast.success("Your registration request has been sent!");
  } catch (error) {
    console.error("Registration request failed:", error);
    toast.error("Failed to send registration request. Please try again.");
  }
};
</script>

<template>
  <section class="relative flex flex-wrap h-screen items-center bg-gray-200">
    <!-- Form Section -->
    <div class="w-full lg:w-1/2 px-8 py-24">
      <div class="mx-auto max-w-lg bg-white p-8 rounded-lg shadow-xl border border-gray-200">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold">
            Register with <span class="text-red-600">BIOS</span>
          </h1>
          <p class="mt-4 text-gray-600">
            This registration form is compulsory for all visitors.
          </p>
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="submitForm" class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label for="name">Name</Label>
              <Input
                id="name"
                v-model="form.name"
                type="text"
                placeholder="Name and Surname"
                class="w-full"
                required
              />
            </div>
            <div>
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="form.email"
                type="email"
                placeholder="Email Address"
                class="w-full"
                required
              />
            </div>
          </div>

          <div>
            <Label for="phone">Phone Number</Label>
            <Input
              id="phone"
              v-model="form.phone"
              type="text"
              placeholder="Phone Number"
              class="w-full"
              required
            />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label for="city">City</Label>
              <Select v-model="form.city" class="w-full" required>
                <SelectTrigger>
                  <SelectValue placeholder="Select city" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectItem
                      v-for="city in cities"
                      :key="city"
                      :value="city"
                    >
                      {{ city }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label for="highSchool">High School</Label>
              <Select
                v-model="form.highSchool"
                :disabled="isHighSchoolDisabled"
                class="w-full"
                required
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select high school" />
                </SelectTrigger>
                <SelectContent>
                  <SelectGroup>
                    <SelectItem
                      v-for="highSchool in filteredHighSchools"
                      :key="highSchool"
                      :value="highSchool"
                    >
                      {{ highSchool }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
              <p v-if="isHighSchoolDisabled" class="text-xs text-red-500 mt-1">
                Please select a city first.
              </p>
            </div>
          </div>

          <div>
            <p class="text-sm text-gray-600 mb-2">
              Select "High School Counsellor" if you are a high school official.
            </p>
            <div class="flex space-x-4">
              <label class="flex items-center">
                <input
                  type="radio"
                  v-model="form.userType"
                  value="individual"
                  class="mr-2"
                />
                Individual
              </label>
              <label class="flex items-center">
                <input
                  type="radio"
                  v-model="form.userType"
                  value="high_school_counsellor"
                  class="mr-2"
                />
                High School Counsellor
              </label>
            </div>
          </div>

          <div class="flex justify-between items-center space-x-4">
            <p class="text-sm text-gray-600 flex flex-col">
              Already have an account?
              <router-link to="/login" class="text-red-600 hover:underline">Sign in</router-link>
            </p>
            <div class="flex space-x-4">
              <!-- Removed Reset Form Button -->

              <Button
                type="submit"
                class="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700"
              >
                Sign Up
              </Button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Image Section -->
    <div class="hidden lg:block relative h-full w-1/2">
      <img
        alt="Bilkent Campus"
        src="@/assets/kayit.jpg"
        class="absolute inset-0 h-full w-full object-cover filter brightness-75 contrast-125 saturate-125 shadow-2xl"
      />
    </div>

    <!-- Confirmation Dialog -->
    <Dialog v-model:open="showConfirmDialog">
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm Registration</DialogTitle>
        </DialogHeader>
        <p class="text-sm text-gray-600">
          Are you sure you want to submit your registration? Please ensure all information is correct.
        </p>
        <DialogFooter class="space-x-4">
          <Button
            variant="secondary"
            class="bg-gray-500 hover:bg-gray-600 text-white"
            @click="showConfirmDialog = false"
          >
            Cancel
          </Button>
          <Button
            variant="primary"
            class="bg-red-600 hover:bg-red-700 text-white"
            @click="confirmSubmit"
          >
            Confirm
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  </section>
</template>