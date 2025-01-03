import { defineStore } from "pinia";
import { ref } from "vue";
import router from "@/router";
import authController from "@/controllers/authController";
import { useMessagingStore } from "@/stores/messagingStore";
import apiClient from "@/services/APIClient";

export const useAuthStore = defineStore("auth", () => {
  const isLoggedIn = ref(false);
  const token = ref("");
  const user = ref({});
  const userRole = ref("");
  const refreshToken = ref("");
  const authInitialized = ref(false);
  const refreshTimeout = ref(null);

  const messagingStore = useMessagingStore();

  const login = async (email, password) => {
    try {
      const response = await authController.login({ email, password });
      setTokens(response.data.access, response.data.refresh);

      const userResponse = await authController.getProfile();
      user.value = userResponse.data;
      userRole.value = userResponse.data.role;
      isLoggedIn.value = true;

      messagingStore.connectWebSocket();

      redirectUser(userRole.value);
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  };
  

  const setTokens = (accessToken, refresh) => {
    token.value = accessToken;
    refreshToken.value = refresh;

    localStorage.setItem("token", token.value);
    localStorage.setItem("refreshToken", refreshToken.value);

    apiClient.defaults.headers.common["Authorization"] = `Bearer ${token.value}`;

    scheduleTokenRefresh();
  };

  const redirectUser = (role) => {
    router.push("/" + role ? role : "");
  };

  const logout = () => {
    isLoggedIn.value = false;
    token.value = "";
    refreshToken.value = "";

    messagingStore.disconnectWebSocket();

    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");

    delete apiClient.defaults.headers.common["Authorization"];

    if (refreshTimeout.value) {
      clearTimeout(refreshTimeout.value);
    }

    router.push("/login");
  };

  const refreshAccessToken = async () => {
    try {
      const response = await authController.refreshToken(refreshToken.value);
      setTokens(response.data.access, refreshToken.value);
    } catch (error) {
      console.error("Failed to refresh access token:", error);
      logout();
    }
  };

  const scheduleTokenRefresh = () => {
    const tokenPayload = JSON.parse(atob(token.value.split(".")[1]));
    const expirationTime = tokenPayload.exp * 1000;
    const currentTime = Date.now();

    const timeout = expirationTime - currentTime - 60000;

    if (timeout > 0) {
      refreshTimeout.value = setTimeout(() => {
        refreshAccessToken();
      }, timeout);
    } else {
      refreshAccessToken();
    }
  };

  const initializeAuthState = async () => {
    const storedToken = localStorage.getItem("token");
    const storedRefreshToken = localStorage.getItem("refreshToken");

    if (storedToken && storedRefreshToken) {
      token.value = storedToken;
      refreshToken.value = storedRefreshToken;
      isLoggedIn.value = true;

      apiClient.defaults.headers.common["Authorization"] = `Bearer ${token.value}`;

      try {
        const userResponse = await authController.getProfile();
        user.value = userResponse.data;
        userRole.value = userResponse.data.role;

        // Connect WebSocket only if not already connected
        messagingStore.connectWebSocket();

        scheduleTokenRefresh();
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        logout();
      }
    }

    authInitialized.value = true;
  };

  initializeAuthState();

  return {
    isLoggedIn,
    token,
    refreshToken,
    user,
    userRole,
    authInitialized,
    initializeAuthState,
    login,
    logout,
  };
});
