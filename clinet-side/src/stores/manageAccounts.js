// stores/manageAccounts.js
import { ref } from "vue";
import { defineStore } from "pinia";
import usersController from "@/controllers/userController";
import advisorController from "@/controllers/advisorController";
// Import guideController if you have one

export const useManageAccountsStore = defineStore("manageAccounts", () => {
    const allUsers = ref([]);

    // Fetch all users and merge advisor/guide data
    const getAllUsers = async () => {
        try {
            const usersResponse = await usersController.getUsers();
            const users = usersResponse.data;

            // Fetch all advisors to get their authorizedDay and advisor_id
            const advisorsResponse = await advisorController.getAdvisors();
            const advisors = advisorsResponse.data;

            // Similarly, fetch all guides if applicable
            // const guidesResponse = await guideController.getGuides();
            // const guides = guidesResponse.data;

            // Create a map of advisor user IDs to their authorizedDay and advisor_id
            const advisorMap = {};
            advisors.forEach(advisor => {
                advisorMap[advisor.user] = {
                    authorizedDay: advisor.authorizedDay,
                    advisor_id: advisor.id,
                };
            });

            // Similarly, create a guideMap if applicable
            // const guideMap = {};
            // guides.forEach(guide => {
            //     guideMap[guide.user] = {
            //         // guide-specific fields
            //     };
            // });

            // Merge advisor data into user objects
            const mergedUsers = users.map(user => {
                if (user.role === "advisor" && advisorMap[user.id]) {
                    return {
                        ...user,
                        authorizedDay: advisorMap[user.id].authorizedDay || [],
                        advisor_id: advisorMap[user.id].advisor_id,
                    };
                }
                // Similarly handle guides if applicable
                return user;
            });

            allUsers.value = mergedUsers;
        } catch (error) {
            console.error("Failed to fetch users:", error);
            throw error;
        }
    };

    // Create a new user and set authorizedDay if advisor
    const createAccount = async (data) => {
        try {
            console.log(data);
            // Create the user
            const userResponse = await usersController.createUser({
                name: data.name,
                email: data.email,
                role: data.role,
            });
            const user = userResponse.data;

            // If the user is an advisor, update authorizedDay
            if (data.role === "advisor" && user.advisor_id) {
                await advisorController.partialUpdateAdvisor(user.advisor_id, {
                    authorizedDay: data.authorizedDay,
                });
            }
        } catch (error) {
            console.error("Failed to create account:", error);
            throw error;
        }
    };

    // Delete a user and, if advisor, delete advisor profile
    const deleteAccount = async (userID) => {
        try {
            const user = allUsers.value.find(u => u.id === userID);
            if (user && user.role === "advisor" && user.advisor_id) {
                await advisorController.deleteAdvisor(user.advisor_id);
            }
            await usersController.deleteUser(userID);
        } catch (error) {
            console.error("Failed to delete account:", error);
            throw error;
        }
    };

    // Update a user and, if advisor, update their authorizedDay
    const partialUpdateAccount = async (userID, data) => {
        console.log(userID, data);
        try {
            // Update user details
            await usersController.partialUpdateUser(userID, {
                name: data.name,
                email: data.email,
                // role is not editable
            });

            // If the user is an advisor, update their authorizedDay
            const user = allUsers.value.find(u => u.id === userID);
            if (user && user.role === "advisor" && user.advisor_id) {
                await advisorController.partialUpdateAdvisor(user.advisor_id, {
                    authorizedDay: data.authorizedDay,
                });
            }
        } catch (error) {
            console.error("Failed to update account:", error);
            throw error;
        }
    };

    return {
        allUsers,
        getAllUsers,
        createAccount,
        deleteAccount,
        partialUpdateAccount,
    };
});
