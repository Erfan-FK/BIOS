import apiClient from "@/services/APIClient";

const messagingController = {
  fetchChatsForUser: (userId) => apiClient.get(`api/chats/${userId}/`),
  fetchChatDetails: (chatId) => apiClient.get(`api/chats/${chatId}/details/`),
  sendMessage: (data) => apiClient.post("api/messages/send/", data),
  createChat: (contactId) => apiClient.post("api/chats/", { contact_id: contactId }),
  editMessage: (messageId, content) =>
    apiClient.put(`api/messages/${messageId}/edit/`, { content }),
  deleteMessage: (messageId) => apiClient.delete(`api/messages/${messageId}/delete/`),
  fetchContacts: () => apiClient.get("api/users/list/"),
  fetchMessages: () => apiClient.get("api/messages/"),
  markMessagesAsRead: (chatId) => apiClient.post(`api/chats/${chatId}/mark-read/`), // New method
};

export default messagingController;
