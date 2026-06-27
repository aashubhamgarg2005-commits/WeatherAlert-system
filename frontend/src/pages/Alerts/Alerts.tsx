import { useEffect, useState } from "react";
import AlertCard from "../../components/cards/AlertCard";
import { getUserProfile, getTodayAlert } from "../../services/weatherService";

function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const profile = await getUserProfile();
        const cityName = profile.city.charAt(0).toUpperCase() + profile.city.slice(1).toLowerCase();
        setCity(cityName);
        const data = await getTodayAlert(cityName);
        setAlerts(data.alerts || []);
      } catch (err) {
        setError("Failed to load alerts");
      } finally {
        setLoading(false);
      }
    };
    loadAlerts();
  }, []);

  if (loading) return <div className="text-center mt-20 text-xl">Loading alerts...</div>;

  return (
    <div className="space-y-5">
      <h1 className="text-3xl font-bold">Weather Alerts — {city}</h1>

      {error && <p className="text-red-500">{error}</p>}

      {alerts.length === 0 ? (
        <p className="text-gray-500">No active alerts for {city} today.</p>
      ) : (
        alerts.map((alert: any, index: number) => (
          <AlertCard
            key={index}
            type={alert.type || "Weather Alert"}
            severity={alert.severity?.toLowerCase() || "low"}
            message={alert.message || ""}
          />
        ))
      )}
    </div>
  );
}

export default Alerts;