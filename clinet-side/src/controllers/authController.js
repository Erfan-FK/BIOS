import apiClient from "@/services/axios";

const authController = {
  login: (credentials) => apiClient.post("auth/login/", credentials),
  getProfile: () => apiClient.get("auth/me/"),
  refreshToken: (refresh) => apiClient.post("auth/refresh/", { refresh }),
  changePassword: (data) => apiClient.post("/auth/change-password/", data),
};

export default authController;
