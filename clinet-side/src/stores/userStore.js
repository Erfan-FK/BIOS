import { defineStore } from "pinia";
import { ref } from "vue";
import authController from "@/controllers/authController";
import userController from "@/controllers/userController";
import { toast } from "vue-sonner";
import { useAuthStore } from "./authStore";

export const useUserStore = defineStore("user", () => {
  const profile = ref(null);
  const selectedFile = ref(null);
  const currentPassword = ref("");
  const newPassword = ref("");
  const confirmPassword = ref("");

  const authStore = useAuthStore();

  // Handle file selection for profile picture
  const handleFileChange = (file) => {
    selectedFile.value = file;
  };

  // Fetch user profile data from the backend
  const fetchProfile = async () => {
    try {
      const response = await authController.getProfile();
      profile.value = response.data;
    } catch (error) {
      console.error("Failed to fetch profile:", error);
      throw error;
    }
  };

  // Handle password change
  const handlePasswordChange = async () => {
    if (newPassword.value !== confirmPassword.value) {
      throw new Error("Passwords do not match.");
    }
    try {
      const response = await authController.changePassword({
        current_password: currentPassword.value,
        new_password: newPassword.value,
      });
      toast.success("Password updated successfully.");
      currentPassword.value = "";
      newPassword.value = "";
      confirmPassword.value = "";
      return response;
    } catch (error) {
      console.error("Failed to update password:", error);
      throw error;
    }
  };

  // Save profile picture
  const saveProfilePicture = async () => {
    if (!selectedFile.value) {
      throw new Error("No file selected.");
    }
    try {
      const formData = new FormData();
      formData.append("profile_picture", selectedFile.value);

      const response = await userController.updateProfilePicture(formData);
      profile.value.profilePicture = response.data.profile_picture;

      // Synchronize with authStore
      authStore.user.profilePicture = response.data.profile_picture;

      toast.success("Profile picture updated successfully.");
      selectedFile.value = null;
    } catch (error) {
      console.error("Failed to upload profile picture:", error);
      throw error;
    }
  };

  return {
    profile,
    selectedFile,
    currentPassword,
    newPassword,
    confirmPassword,
    fetchProfile,
    saveProfilePicture,
    handlePasswordChange,
    handleFileChange,
  };
});
