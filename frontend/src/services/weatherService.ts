import api from "./api";

// ===== AUTH =====
export const loginUser = async (email: string, password: string) => {
  const response = await api.post("/auth/login", { email, password });
  return response.data;
};

export const registerUser = async (data: {
  email: string;
  password: string;
  user_name: string;
  phone: string;
  city_name: string;
  state: string;
}) => {
  const response = await api.post("/auth/register", data);
  return response.data;
};

// ===== WEATHER =====
export const getTodayWeather = async (city: string) => {
  const response = await api.get(`/alert/today_weather/${city}`);
  return response.data;
};

export const getForecastWeather = async (city: string) => {
  const response = await api.get(`/alert/forecast_weather/${city}`);
  return response.data;
};

// ===== ALERTS =====
export const getTodayAlert = async (city: string) => {
  const response = await api.get(`/alert/today_alert/${city}`);
  return response.data;
};

export const getForecastAlert = async (city: string) => {
  const response = await api.get(`/alert/forecast_alert/${city}`);
  return response.data;
};

// ===== WIND & RAIN =====
export const getWindData = async (city: string) => {
  const response = await api.get(`/alert/wind_by_city/${city}`);
  return response.data;
};

export const getRainData = async (city: string) => {
  const response = await api.get(`/alert/rain_city/${city}`);
  return response.data;
};

export const getUserProfile = async () => {
  const response = await api.get("/auth/profile");
  return response.data;
};


export const getPreferences = async () => {
  const response = await api.get("/auth/preferences");
  return response.data;
};

export const updatePreferences = async (data: object) => {
  const response = await api.put("/auth/preferences", data);
  return response.data;
};