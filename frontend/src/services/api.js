import axios from "axios";

const ROOT_URL = "http://127.0.0.1:5000";

const api = axios.create({
  baseURL: `${ROOT_URL}/api`,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export { ROOT_URL };
export default api;

