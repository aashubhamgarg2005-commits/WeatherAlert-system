import { useState } from "react";
import { getTodayWeather } from "../services/weatherService";

interface WeatherData {
  city: string;
  temperature: number;
  humidity: number;
  windSpeed: number;
  condition: string;
}

export default function useWeather() {
  const [data, setData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const fetchWeather = async (city: string) => {
    try {
      setLoading(true);
      setError("");
      const result = await getTodayWeather(city);
      setData({
        city: result.city,
        temperature: result.tempreture_in_celsius,
        humidity: result.humidity,
        windSpeed: result.wind_kph,
        condition: result.condition,
      });
    } catch (err: any) {
      setError(err?.response?.data?.detail || "City not found or server error");
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, fetchWeather };
}