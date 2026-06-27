import { useEffect, useState } from "react";
import WeatherCard from "../../components/cards/WeatherCard";
import TemperatureChart from "../../components/charts/TemperatureChart";
import AlertCard from "../../components/cards/AlertCard";
import { getUserProfile, getTodayWeather, getTodayAlert } from "../../services/weatherService";

function Dashboard() {
  const [weather, setWeather] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [city, setCity] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const profile = await getUserProfile();
        const cityName = profile.city.charAt(0).toUpperCase() + profile.city.slice(1).toLowerCase();
        setCity(cityName);

        const weatherData = await getTodayWeather(cityName);
        setWeather(weatherData);

        const alertData = await getTodayAlert(cityName);
        setAlerts(alertData.alerts || []);
      } catch (err) {
        console.error("Dashboard load error:", err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div className="text-center mt-20 text-xl">Loading...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        Dashboard — {city}
      </h1>

      {/* Weather Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <WeatherCard title="Temperature" value={`${weather?.tempreture_in_celsius ?? "--"}°C`} />
        <WeatherCard title="Humidity" value={`${weather?.humidity ?? "--"}%`} />
        <WeatherCard title="Wind Speed" value={`${weather?.wind_kph ?? "--"} km/h`} />
        <WeatherCard title="Precipitation" value={`${weather?.precip_mm ?? "--"} mm`} />
      </div>

      {/* Charts + Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <TemperatureChart />
        {alerts.length > 0 ? (
          alerts.map((alert: any, index: number) => (
            <AlertCard
              key={index}
              type={alert.type || "Weather Alert"}
              severity={alert.severity?.toLowerCase() || "low"}
              message={alert.message || ""}
            />
          ))
        ) : (
          <AlertCard
            type="No Alerts"
            severity="low"
            message="No weather alerts for your city today."
          />
        )}
      </div>
    </div>
  );
}

export default Dashboard;