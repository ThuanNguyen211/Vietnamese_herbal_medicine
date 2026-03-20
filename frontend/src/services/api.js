import axios from 'axios';

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
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

// ============ Map API ============

export const sendMapMessage = async ({ message, image, sessionId }) => {
  const formData = new FormData();
  if (message) formData.append('message', message);
  if (image) formData.append('image', image);
  if (sessionId) formData.append('session_id', sessionId);

  try {
    const response = await api.post('/api/map/chat', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error) {
    // Backward-compatible fallback for old backend deployments.
    if (error?.response?.status === 404) {
      const fallbackResponse = await api.post('/api/chatbot/chat', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return fallbackResponse.data;
    }
    throw error;
  }
};

export default api;
