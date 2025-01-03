import apiClient from "@/services/APIClient";
import advisorController from "@/controllers/advisorController";

const usersController = {
    getUsers: () => apiClient.get("/api/users/"),
    createUser: (data) => apiClient.post("/api/users/create-user/", data),
    getUserById: async (id) => {
        try {
            const userResponse = await apiClient.get(`/api/users/${id}/`);
            const user = userResponse.data;

            // If user is an advisor, fetch advisor details
            if (user.role === "advisor") {
                const advisorResponse = await advisorController.getAdvisorById(user.id);
                user.authorizedDay = advisorResponse.data.authorizedDay || [];
            }

            return user;
        } catch (error) {
            console.error("Failed to fetch user by ID:", error);
            throw error;
        }
    },
    updateUser: (id, data) => apiClient.put(`/api/users/${id}/`, data),
    partialUpdateUser: (id, data) => apiClient.patch(`/api/users/${id}/`, data),
    deleteUser: (id) => apiClient.delete(`/api/users/${id}/`),
    updateProfilePicture: (file) =>
        apiClient.patch("/api/user/update-profile-picture/", file, {
            headers: { "Content-Type": "multipart/form-data" },
        }),
};

export default usersController;
