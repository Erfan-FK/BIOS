<script setup>
import { useUserStore } from "@/stores/userStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Star } from "lucide-vue-next";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "vue-sonner";
import { ref, onMounted } from "vue";
import {storeToRefs} from "pinia";

const userStore = useUserStore();
const showDialog = ref(false); // Control dialog visibility
const fileInputRef = ref(null); // Reference for the file input element

const { selectedFile } = storeToRefs(userStore);
// Fetch profile on mount
onMounted(async () => {
  try {
    await userStore.fetchProfile();
  } catch (error) {
    console.error("Failed to load profile data.", error);
  }
});

const confirmPasswordChange = async () => {
  try {
    await userStore.handlePasswordChange();
    toast.success("Password updated successfully!", {
      description: "Your password has been changed.",
    });
    showDialog.value = false; // Close dialog
  } catch (error) {
    toast.error(error.message || "Failed to update password. Please try again.");
  }
};

const saveProfilePicture = async () => {
  try {
    await userStore.saveProfilePicture();
    if (fileInputRef.value) {
      fileInputRef.value.value = ""; // Reset file input field
    }
  } catch (error) {
    toast.error("Failed to update profile picture. Please try again.");
  }
};
</script>

<template>
  <div class="flex flex-col h-full bg-gray-100">
    <!-- Header Section -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300 bg-white rounded-t-lg shadow">
      <div>
        <h2 class="text-xl font-bold text-gray-800">Edit Profile</h2>
        <p class="text-md text-gray-600 mt-2">
          Update your personal details, change your password, or upload a profile picture.
        </p>
      </div>
    </div>

    <!-- Profile Content -->
    <div class="flex flex-col lg:flex-row bg-white rounded-b-lg shadow-lg p-8 space-y-6 lg:space-y-0 lg:space-x-10 flex-grow">
      <!-- Profile Information Display -->
      <div class="flex flex-col items-center lg:items-start space-y-4 lg:w-1/3 text-center lg:text-left">
        <img
          :src="userStore.profile?.profilePicture"
          alt="Profile"
          class="w-40 h-40 rounded-full shadow-md object-cover"
        />
        <div class="text-center lg:text-left space-y-2">
          <p class="text-2xl font-semibold">
            {{ userStore.profile?.firstName }} {{ userStore.profile?.lastName }}
          </p>
          <p class="text-gray-500">ID: {{ userStore.profile?.id }}</p>
          <p class="text-gray-500">{{ userStore.profile?.email }}</p>

          <!-- Display rating only if the user is a guide -->
          <div v-if="userStore.profile?.role === 'guide'" class="flex items-center justify-center lg:justify-start space-x-1">
            <Star class="text-yellow-500 fill-yellow-500 w-5 h-5" />
            <span class="text-lg font-semibold">
              {{ userStore.profile?.rating || "0" }}
            </span>
          </div>
        </div>
      </div>

      <!-- Profile Update Form -->
      <div class="flex flex-col flex-grow space-y-6">
        <!-- Profile Picture Change -->
        <div>
          <Label for="profilePicture" class="font-medium text-gray-700">
            Change Profile Picture
          </Label>
          <Input
            id="profilePicture"
            type="file"
            ref="fileInputRef"
            @change="(e) => userStore.handleFileChange(e.target.files[0])"
            class="mt-2"
          />
          <div class="mt-4">
            <Button
              @click="saveProfilePicture"
              variant="primary"
              class="bg-red-500 hover:bg-red-600 text-white"
              v-show="selectedFile"
            >
              Upload Picture
            </Button>
          </div>
        </div>

        <!-- Change Password Section -->
        <div>
          <Label for="currentPassword" class="font-medium text-gray-700">
            Current Password
          </Label>
          <Input
            id="currentPassword"
            v-model="userStore.currentPassword"
            type="password"
            placeholder="Current Password"
            class="mt-2"
          />

          <Label for="newPassword" class="font-medium text-gray-700 mt-4 block">
            New Password
          </Label>
          <Input
            id="newPassword"
            v-model="userStore.newPassword"
            type="password"
            placeholder="New Password"
            class="mt-2"
          />

          <Label for="confirmPassword" class="font-medium text-gray-700 mt-4 block">
            Confirm New Password
          </Label>
          <Input
            id="confirmPassword"
            v-model="userStore.confirmPassword"
            type="password"
            placeholder="Confirm New Password"
            class="mt-2"
          />

          <!-- Confirmation Dialog -->
          <Dialog v-model:open="showDialog">
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Confirm Password Change</DialogTitle>
              </DialogHeader>
              <p class="text-sm text-gray-600">
                Are you sure you want to change your password? This action cannot be undone.
              </p>
              <DialogFooter class="space-x-4">
                <Button
                  variant="secondary"
                  class="bg-gray-500 hover:bg-gray-600 text-white"
                  @click="showDialog = false"
                >
                  Cancel
                </Button>
                <Button
                  variant="primary"
                  class="bg-red-500 hover:bg-red-600 text-white"
                  @click="confirmPasswordChange"
                >
                  Confirm
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          <!-- Trigger Dialog -->
          <Button
            variant="primary"
            class="mt-4 bg-red-500 hover:bg-red-600 text-white ml-auto"
            @click="showDialog = true"
          >
            Change Password
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
