<script setup>
import { ref, computed, watch, onMounted } from "vue";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { useManageAccountsStore } from "@/stores/manageAccounts";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { storeToRefs } from "pinia";
import authController from "@/controllers/authController";
import { toast } from "vue-sonner";
import  advisorController  from "@/controllers/advisorController";
import  usersController  from "@/controllers/userController";

const manageAccountsStore = useManageAccountsStore();

const searchQuery = ref("");
const isLoading = ref(false);
const selectedFilter = ref("All");
const selectedUser = ref(null);
const editedUser = ref({
  id: null,
  name: "",
  email: "",
  authorizedDay: [],
  advisor_id: null,
  guide_id: null,
});
const errorMessage = ref("");

const isEditModalOpen = ref(false);
const isDeleteModalOpen = ref(false);
const isNewUserModalOpen = ref(false);

const daysOfWeek = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];
const authorizedDays = ref([]);

const filteredUsers = computed(() => {
  const allUsers = manageAccountsStore.allUsers || [];

  return allUsers.filter((user) => {
    const matchesSearch =
      searchQuery.value === "" ||
      user.name.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesFilter =
      selectedFilter.value === "All" || user.role === selectedFilter.value;

    return matchesSearch && matchesFilter;
  });
});

watch(selectedFilter, () => {
  searchQuery.value = "";
});

onMounted(() => {
  manageAccountsStore.getAllUsers();
});

const validateUser = (user, isEdit = false) => {
  if (!user.name || !user.email) {
    errorMessage.value = "Name and Email fields are required.";
    return false;
  }
  if (!isEdit) {
    if (!user.role) {
      errorMessage.value = "Role field is required.";
      return false;
    }
  }
  if (user.role === "advisor" && user.authorizedDay.length === 0) {
    errorMessage.value =
      "At least one authorized day must be selected for advisors.";
    return false;
  }
  errorMessage.value = "";
  return true;
};

const createUser = async () => {
  const newUser = {
    name: editedUser.value.name,
    email: editedUser.value.email,
    role: editedUser.value.role.toLowerCase(),
    authorizedDay:
      editedUser.value.role === "advisor" ? authorizedDays.value : [],
  };
  if (validateUser(newUser)) {
    try {
      isLoading.value = true;
      await manageAccountsStore.createAccount(newUser);
      toast.success("User created successfully!");
      await manageAccountsStore.getAllUsers();
      closeModal();
    } catch (error) {
      toast.error("Failed to create user.");
    } finally {
      isLoading.value = false;
    }
  }
};

const updateUser = async () => {
  const id = editedUser.value.id;

  if (!id) {
    toast.error("User ID is missing.");
    return;
  }

  const user = manageAccountsStore.allUsers.find((u) => u.id === id);

  if (!user) {
    toast.error("User not found.");
    return;
  }

  const updatedUser = {
    name: editedUser.value.name,
    email: editedUser.value.email,
    authorizedDay: user.role === "advisor" ? authorizedDays.value : [],
  };

  if (validateUser({ ...updatedUser, role: user.role }, true)) {
    // Pass isEdit=true
    try {
      // Update user details
      await usersController.partialUpdateUser(id, {
        name: updatedUser.name,
        email: updatedUser.email,
      });

      // If the user is an advisor, update their authorizedDay using advisor_id
      if (user.role === "advisor" && editedUser.value.advisor_id) {
        await advisorController.partialUpdateAdvisor(
          editedUser.value.advisor_id,
          {
            authorizedDay: updatedUser.authorizedDay,
          }
        );
      }

      toast.success("User updated successfully!");
      await manageAccountsStore.getAllUsers();
      closeModal();
    } catch (error) {
      console.error("Failed to update user:", error);
      toast.error("Failed to update user.");
    }
  }
};

const openNewUserModal = () => {
  isNewUserModalOpen.value = true;
  // Reset authorizedDays when creating a new user
  authorizedDays.value = [];
  // Reset editedUser for creating
  editedUser.value = {
    id: null,
    name: "",
    email: "",
    authorizedDay: [],
    advisor_id: null,
    guide_id: null,
  };
};

const openEditModal = (user) => {
  isEditModalOpen.value = true;
  selectedUser.value = user;
  editedUser.value = {
    id: user.id,
    name: user.name,
    email: user.email,
    authorizedDay: user.authorizedDay || [],
    advisor_id: user.advisor_id || null,
    guide_id: user.guide_id || null,
  };
  // If the user is an advisor, set authorizedDays
  authorizedDays.value = user.role === "advisor" ? user.authorizedDay : [];
};

const capitalizeFirstChar = (str) => {
  return str.charAt(0).toUpperCase() + str.slice(1);
};

const openDeleteModal = (user) => {
  isDeleteModalOpen.value = true;
  selectedUser.value = user;
};

const closeModal = () => {
  isEditModalOpen.value = false;
  isDeleteModalOpen.value = false;
  isNewUserModalOpen.value = false;
  selectedUser.value = null;
  editedUser.value = { name: "", email: "", authorizedDay: [] };
  errorMessage.value = "";
  authorizedDays.value = [];
};

const deleteUser = async (userID) => {
  try {
    await manageAccountsStore.deleteAccount(userID);
    toast.success("User deleted successfully!");
    await manageAccountsStore.getAllUsers();
    closeModal();
  } catch (error) {
    toast.error("Failed to delete user.");
  }
};

// Toggle authorized day selection
const toggleAuthorizedDay = (dayIndex) => {
  const index = authorizedDays.value.indexOf(dayIndex);
  if (index > -1) {
    authorizedDays.value.splice(index, 1);
  } else {
    authorizedDays.value.push(dayIndex);
  }
};
</script>

<template>
  <div class="flex flex-col h-full bg-white rounded-lg shadow-lg">
    <!-- Header -->
    <div class="flex justify-between items-center p-6 border-b border-gray-300">
      <div>
        <h2 class="text-xl font-bold">Manage Staff Accounts</h2>
        <p class="text-md text-gray-600 mt-2">Change or add staff accounts.</p>
      </div>
      <div class="flex items-center gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by Staff Name"
          class="w-[250px] p-2 border border-gray-300 rounded-lg"
        />
        <Select v-model="selectedFilter">
          <SelectTrigger class="w-[180px]">
            <SelectValue placeholder="Filter" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Filter Options</SelectLabel>
              <SelectItem value="All">All Users</SelectItem>
              <SelectItem value="coordinator">Coordinator(s)</SelectItem>
              <SelectItem value="advisor">Advisor(s)</SelectItem>
              <SelectItem value="secretary">Secretary(s)</SelectItem>
              <SelectItem value="guide">Guide(s)</SelectItem>
              <SelectItem value="director">Director(s)</SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Users Table -->
    <div class="flex-grow overflow-y-auto p-6 pt-2">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead class="font-bold text-red-700">#</TableHead>
            <TableHead class="font-bold text-red-700">Name</TableHead>
            <TableHead class="font-bold text-red-700">Email</TableHead>
            <TableHead class="font-bold text-red-700">Role</TableHead>
            <TableHead class="font-bold text-red-700">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow v-for="(user, index) in filteredUsers" :key="user.id">
            <TableCell>{{ index + 1 }}</TableCell>
            <TableCell>{{ user.name }}</TableCell>
            <TableCell>{{ user.email }}</TableCell>
            <TableCell>{{ capitalizeFirstChar(user.role) }}</TableCell>
            <TableCell>
              <div class="flex gap-3">
                <Button
                  class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded"
                  @click="openEditModal(user)"
                >
                  Edit
                </Button>
                <Button
                  class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                  @click="openDeleteModal(user)"
                >
                  Delete
                </Button>
              </div>
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </div>

    <!-- Add New User Button -->
    <div class="flex justify-center mb-4">
      <Button
        class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        @click="openNewUserModal()"
      >
        Add New User
      </Button>
    </div>
  </div>

  <!-- Create User Modal -->
  <div
    v-if="isNewUserModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
      <!-- Increased max-w -->
      <h2 class="text-2xl font-bold mb-6">Add New User</h2>
      <form @submit.prevent="createUser" class="space-y-4">
        <div>
          <Label for="name" class="block text-lg font-semibold">Name</Label>
          <Input
            id="name"
            v-model="editedUser.name"
            type="text"
            class="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <Label for="email" class="block text-lg font-semibold">Email</Label>
          <Input
            id="email"
            v-model="editedUser.email"
            type="email"
            class="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <Label for="role" class="block text-lg font-semibold">Role</Label>
          <Select id="role" v-model="editedUser.role" class="w-full" required>
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select Role" />
            </SelectTrigger>
            <SelectContent>
              <SelectGroup>
                <SelectLabel>Roles</SelectLabel>
                <SelectItem value="director">Director</SelectItem>
                <SelectItem value="coordinator">Coordinator</SelectItem>
                <SelectItem value="advisor">Advisor</SelectItem>
                <SelectItem value="guide">Guide</SelectItem>
                <SelectItem value="secretary">Secretary</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>
        </div>

        <!-- Authorized Days (Visible Only for Advisors) -->
        <div v-if="editedUser.role === 'advisor'">
          <Label class="block text-lg font-semibold">Authorized Days</Label>
          <div class="flex flex-wrap gap-2">
            <!-- Changed to flex-wrap -->
            <button
              type="button"
              v-for="(day, index) in daysOfWeek"
              :key="index"
              @click="toggleAuthorizedDay(index)"
              :class="[
                'px-4 py-2 rounded focus:outline-none focus:ring',
                authorizedDays.includes(index)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700',
              ]"
            >
              {{ day }}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-4 mt-6">
          <Button
            type="submit"
            :disabled="isLoading"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          >
            <span v-if="isLoading" class="mr-2">Adding...</span>
            <span v-else>Add User</span>
          </Button>
          <Button
            type="button"
            @click="closeModal"
            class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
          >
            Close
          </Button>
        </div>
      </form>
    </div>
  </div>

  <!-- Edit Modal -->
  <div
    v-if="isEditModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
      <!-- Increased max-w -->
      <h2 class="text-2xl font-bold mb-6">
        Edit User: {{ selectedUser?.name }}
      </h2>
      <form @submit.prevent="updateUser" class="space-y-4">
        <div>
          <Label for="name" class="block text-lg font-semibold">Name</Label>
          <Input
            id="name"
            v-model="editedUser.name"
            type="text"
            class="w-full p-2 border rounded"
            required
          />
        </div>
        <div>
          <Label for="email" class="block text-lg font-semibold">Email</Label>
          <Input
            id="email"
            v-model="editedUser.email"
            type="email"
            class="w-full p-2 border rounded"
            required
          />
        </div>
        <!-- Removed Role Field -->

        <!-- Authorized Days (Visible Only for Advisors) -->
        <div v-if="selectedUser?.role === 'advisor'">
          <!-- Use selectedUser to ensure correct role -->
          <Label class="block text-lg font-semibold">Authorized Days</Label>
          <div class="flex flex-wrap gap-2">
            <!-- Changed to flex-wrap -->
            <button
              type="button"
              v-for="(day, index) in daysOfWeek"
              :key="index"
              @click="toggleAuthorizedDay(index)"
              :class="[
                'px-4 py-2 rounded focus:outline-none focus:ring',
                authorizedDays.includes(index)
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700',
              ]"
            >
              {{ day }}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

        <!-- Action Buttons -->
        <div class="flex justify-end space-x-4 mt-6">
          <Button
            type="submit"
            class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
          >
            Update User
          </Button>
          <Button
            type="button"
            @click="closeModal"
            class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
          >
            Close
          </Button>
        </div>
      </form>
    </div>
  </div>

  <!-- Delete Modal -->
  <div
    v-if="isDeleteModalOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white p-6 rounded-lg shadow-lg w-full max-w-md">
      <h2 class="text-2xl font-bold mb-4">Delete User</h2>
      <p class="text-gray-600 mb-6">
        Are you sure you want to delete
        <span class="font-semibold">{{ selectedUser?.name }}</span
        >?
      </p>
      <div class="flex justify-end space-x-4">
        <Button
          class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
          @click="deleteUser(selectedUser.id)"
        >
          Delete
        </Button>
        <Button
          @click="closeModal"
          class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
        >
          Cancel
        </Button>
      </div>
    </div>
  </div>
</template>
