import { useEffect, useState } from "react";
import { getUserProfile, getForecastWeather } from "../../services/weatherService";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from "recharts";

function Forecast() {
  const [forecast, setForecast] = useState<any[]>([]);
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadForecast = async () => {
      try {
        const profile = await getUserProfile();
        const cityName = profile.city.charAt(0).toUpperCase() + profile.city.slice(1).toLowerCase();
        setCity(cityName);
        const data = await getForecastWeather(cityName);
        setForecast(data.forecast || []);
      } catch (err) {
        setError("Failed to load forecast data");
      } finally {
        setLoading(false);
      }
    };
    loadForecast();
  }, []);

  if (loading) return <div className="text-center mt-20 text-xl">Loading forecast...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Weather Forecast — {city}</h1>

      {error && <p className="text-red-500">{error}</p>}

      {/* Chart */}
      <div className="bg-white p-6 rounded-xl shadow">
        <p className="text-gray-600 mb-4 font-semibold">7 Days Temperature Trend</p>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={forecast}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="temperature" stroke="#f97316" strokeWidth={3} dot={{ r: 4 }} />
            <Line type="monotone" dataKey="max_temperature" stroke="#ef4444" strokeWidth={2} dot={{ r: 3 }} />
            <Line type="monotone" dataKey="min_temperature" stroke="#3b82f6" strokeWidth={2} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Forecast Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {forecast.map((item: any, index: number) => (
          <div key={index} className="bg-white rounded-xl shadow p-5">
            <p className="text-gray-500 text-sm mb-2">Day {index + 1}</p>
            <p className="text-2xl font-bold">{item.temperature}°C</p>
            <p className="text-sm text-red-500">Max: {item.max_temperature}°C</p>
            <p className="text-sm text-blue-500">Min: {item.min_temperature}°C</p>
            <p className="text-sm text-gray-600 mt-2">Humidity: {item.humidity}%</p>
            <p className="text-sm text-gray-600">Wind: {item.wind_kph} km/h</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Forecast;