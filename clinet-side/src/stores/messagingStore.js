import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { toast } from "vue-sonner";
import messagingController from "@/controllers/messagingController";

export const useMessagingStore = defineStore("messaging", () => {
  const authStore = useAuthStore();

  const chats = ref([]);
  const websocket = ref(null);
  const contactsList = ref([]);
  const activeChatId = ref(null);
  const broadcastMessages = ref([]);
  const activeBroadcastId = ref(null);

  // Fetch chats for a specific contact
  const fetchChatsForUser = async (userId) => {
    try {
      const response = await messagingController.fetchChatsForUser(userId);
      chats.value = response.data;
    } catch (error) {
      console.error("Error fetching chats for user:", error);
    }
  };

  // Fetch broadcast messages
  const fetchBroadcastMessages = async () => {
    try {
      const response = await messagingController.fetchMessages();
      const { received_messages, sent_messages } = response?.data;
      const allMessages = [...received_messages, ...sent_messages];
      const broadcasts = allMessages.filter(
        (message) => message.message_type === "broadcast"
      );
      broadcasts.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
      broadcastMessages.value = broadcasts;
    } catch (error) {
      console.error("Error fetching broadcast messages:", error);
    }
  };

  // Fetch messages for a specific chat
  const fetchMessages = async (chatId) => {
    try {
      const response = await messagingController.fetchChatDetails(chatId);
      const chatIndex = chats.value.findIndex((chat) => chat.id === chatId);

      if (chatIndex !== -1) {
        // messages are in chronological order (oldest first)
        chats.value[chatIndex] = {
          ...chats.value[chatIndex],
          messages: response.data.messages.sort(
            (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
          ),
        };
      }
    } catch (error) {
      console.error("Error fetching messages for chat:", error);
    }
  };

  // Fetch contacts for creating new chats
  const fetchContacts = async () => {
    try {
      const response = await messagingController.fetchContacts();
      contactsList.value = response.data;
    } catch (error) {
      console.error("Error fetching contacts:", error);
    }
  };

  // Create a new chat
  const createChat = async (contactId) => {
    try {
      const response = await messagingController.createChat(contactId);
      const newChat = response.data;
      chats.value.push(newChat);
      setActiveChat(newChat.id);
      return newChat;
    } catch (error) {
      console.error("Error creating chat:", error);
      return null;
    }
  };

  const sendMessage = async (
    chatId,
    content,
    messageType = "direct",
    receivers = []
  ) => {
    try {
      const data = {
        chat_id: chatId,
        content,
        message_type: messageType,
        receivers,
      };

      const response = await messagingController.sendMessage(data);
      if (messageType === "direct") {
        // Refresh messages for the active chat
        await fetchMessages(chatId);
      } else {
        // Refresh broadcast messages
        await fetchBroadcastMessages();
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const setActiveChat = async (chatId) => {
    activeChatId.value = chatId;
    activeBroadcastId.value = null;
    await fetchMessages(chatId);
  };

  const setActiveBroadcast = async (broadcastId) => {
    activeBroadcastId.value = broadcastId;
    activeChatId.value = null;
    await fetchBroadcastMessages();
  };

  const handleIncomingMessage = (message) => {
    const messageTimestamp = new Date(message.timestamp).getTime();

    if (message.message_type === "broadcast") {
      // Handle Broadcast Messages
      const broadcastIndex = broadcastMessages.value.findIndex(
        (msg) => msg.id === message.id
      );
      if (broadcastIndex === -1) {
        broadcastMessages.value.unshift({
          id: `broadcast_${message.id}`, // Prefix to ensure uniqueness
          isBroadcast: true,
          name: "Broadcast",
          content: message.content,
          timestamp: messageTimestamp,
          message_type: message.message_type,
          is_seen: message.is_seen,
          sender: {
            id: message.sender.id,
            name: message.sender.name,
            profile_picture: message.sender.profile_picture,
            role: message.sender.role,
          },
        });
      } else {
        // Update existing broadcast message if needed
        broadcastMessages.value[broadcastIndex] = {
          ...broadcastMessages.value[broadcastIndex],
          content: message.content,
          timestamp: messageTimestamp,
          is_seen: message.is_seen,
        };
      }
    } else {
      // Handle Direct Messages
      const chatIndex = chats.value.findIndex((c) => c.id === message.chat);
      const newMessage = {
        id: message.id,
        sender: {
          id: message.sender.id,
          name: message.sender.name,
          profile_picture: message.sender.profile_picture,
          role: message.sender.role,
        },
        content: message.content,
        timestamp: messageTimestamp,
        message_type: message.message_type,
        is_seen: message.is_seen,
      };

      if (chatIndex !== -1) {
        // Append the new message to existing chat
        chats.value[chatIndex].messages.push(newMessage);
        // Update the last_message_timestamp
        chats.value[chatIndex].last_message_timestamp = messageTimestamp;
      } else {
        // Create a new chat with the incoming message
        chats.value.unshift({
          id: message.chat,
          participant1:
            message.sender.id === chats.value.participant1?.id
              ? message.sender
              : undefined,
          participant2:
            message.sender.id === chats.value.participant2?.id
              ? message.sender
              : undefined,
          messages: [newMessage],
          last_message_timestamp: messageTimestamp,
        });
      }

      if (message.sender.id !== authStore.user.id) {
        toast.info(`New message from ${message.sender.name}`);
      }
    }
  };

  // Connect WebSocket
  const connectWebSocket = () => {
    if (websocket.value) {
      if (websocket.value.readyState === WebSocket.OPEN) {
        console.log("WebSocket is already connected.");
        return;
      } else if (websocket.value.readyState === WebSocket.CONNECTING) {
        console.log("WebSocket is currently connecting.");
        return;
      } else if (
        websocket.value.readyState === WebSocket.CLOSING ||
        websocket.value.readyState === WebSocket.CLOSED
      ) {
        console.log("WebSocket is closed or closing. Reconnecting...");
        // Optionally, you can attempt to reconnect here
      }
    }

    if (!authStore.token) {
      console.error("Cannot connect WebSocket: no token available.");
      return;
    }

    const wsUrl = `ws://localhost:8001/ws/chat/?token=${authStore.token}`;

    websocket.value = new WebSocket(wsUrl);

    websocket.value.onopen = () => {
      console.log("WebSocket connected!");
    };

    websocket.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.message) {
          handleIncomingMessage(data.message);
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    websocket.value.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    websocket.value.onclose = (event) => {
      // Attempt to reconnect after a delay
      setTimeout(() => {
        console.log("Reconnecting WebSocket...");
        connectWebSocket();
      }, 5000); // Reconnect after 5 seconds
    };
  };

  const disconnectWebSocket = () => {
    if (websocket.value) {
      websocket.value.close();
      websocket.value = null;
      console.log("WebSocket disconnected!");
    }
  };

  return {
    chats,
    websocket,
    contactsList,
    activeChatId,
    broadcastMessages,
    activeBroadcastId,
    fetchChatsForUser,
    fetchMessages,
    fetchContacts,
    createChat,
    sendMessage,
    setActiveChat,
    handleIncomingMessage,
    connectWebSocket,
    disconnectWebSocket,
    fetchBroadcastMessages,
    setActiveBroadcast,
  };
});
