import axios from "axios";
import router from "@/router";
import { useAuthStore } from "@/stores/authStore";
import { storeToRefs } from "pinia";

// Create an Axios instance
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add a request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const authStore = useAuthStore();
    const { refreshToken } = storeToRefs(authStore);

    if (error.response && error.response.status === 401 && refreshToken.value) {
      const originalRequest = error.config;

      try {
        // Attempt to refresh the token
        const response = await apiClient.post("/auth/token/refresh/", {
          refresh: refreshToken.value,
        });

        const newAccessToken = response.data.access;

        // Update token through authStore method
        authStore.updateToken(newAccessToken);

        // Retry the original request with the new token
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // If refresh fails, log out and redirect to login
        authStore.logout();
        router.push("/login");
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
