import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
});

// ============ Plants API ============

export const getCatalog = async () => {
  const response = await api.get('/api/plants/catalog');
  return response.data;
};

export const searchPlants = async (query) => {
  const response = await api.get('/api/plants/search', { params: { q: query } });
  return response.data;
};

export const getPlantDetail = async (plantId) => {
  const response = await api.get(`/api/plants/${plantId}`);
  return response.data;
};

// ============ Chatbot API ============

export const sendChatMessage = async ({ message, image, sessionId }) => {
  const formData = new FormData();
  if (message) formData.append('message', message);
  if (image) formData.append('image', image);
  if (sessionId) formData.append('session_id', sessionId);

  const response = await api.post('/api/chatbot/chat', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export default api;
