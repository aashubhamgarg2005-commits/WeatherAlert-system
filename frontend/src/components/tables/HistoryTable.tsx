import { useEffect, useState } from "react";
import { getUserProfile } from "../../services/weatherService";
import api from "../../services/api";

function HistoryTable() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const profile = await getUserProfile();
        const cityName = profile.city.charAt(0).toUpperCase() + profile.city.slice(1).toLowerCase();

        // Last 7 days dates
        const dates = [];
        for (let i = 6; i >= 0; i--) {
          const d = new Date();
          d.setDate(d.getDate() - i);
          dates.push(d.toISOString().split("T")[0]);
        }

        // Fetch each date
        const results = await Promise.allSettled(
          dates.map((date) => api.get(`/alert/weather_by_date/${date}`))
        );

        const history = results
          .filter((r) => r.status === "fulfilled")
          .map((r: any, i) => ({
            date: dates[i],
            city: cityName,
            temp: r.value?.data?.weather?.temperature_in_celsius ?? "--",
            condition: r.value?.data?.weather?.condition ?? "--",
            humidity: r.value?.data?.weather?.humidity ?? "--",
          }));

        setData(history);
      } catch (err) {
        setError("Failed to load history");
      } finally {
        setLoading(false);
      }
    };
    loadHistory();
  }, []);

  if (loading) return <div className="text-center mt-10">Loading history...</div>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="bg-white shadow rounded-xl p-5 overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b bg-gray-50">
            <th className="p-3 font-semibold">Date</th>
            <th className="p-3 font-semibold">City</th>
            <th className="p-3 font-semibold">Temperature</th>
            <th className="p-3 font-semibold">Humidity</th>
            <th className="p-3 font-semibold">Condition</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.date} className="border-b hover:bg-gray-50 transition">
              <td className="p-3">{item.date}</td>
              <td className="p-3">{item.city}</td>
              <td className="p-3">{item.temp}°C</td>
              <td className="p-3">{item.humidity}%</td>
              <td className="p-3">{item.condition}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;