export interface WeatherData {
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
  condition: string;
  pressure: number;
}

export interface AlertData {
  id: number;
  city: string;
  alertType: string;
  severity: "low" | "medium" | "high";
  message: string;
  createdAt: string; // ISO string
}