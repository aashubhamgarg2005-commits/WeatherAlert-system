import { useEffect, useState } from "react";
import { getPreferences, updatePreferences } from "../../services/weatherService";

function Settings() {
  const [notifyViaPush, setNotifyViaPush] = useState(true);
  const [alertLevel, setAlertLevel] = useState("severe");
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const pref = await getPreferences();
        setNotifyViaPush(pref.notify_via_push);
        setAlertLevel(pref.alert_level);
      } catch (err) {
        console.error("Failed to load preferences");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleSave = async () => {
    try {
      await updatePreferences({ notify_via_push: notifyViaPush, alert_level: alertLevel });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error("Failed to save preferences");
    }
  };

  if (loading) return <div className="text-center mt-20 text-xl">Loading settings...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      <div className="bg-white rounded-xl shadow p-6 space-y-5">
        <h2 className="font-bold text-lg">Alert Preferences</h2>

        <label className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={notifyViaPush}
            onChange={() => setNotifyViaPush(!notifyViaPush)}
            className="w-4 h-4"
          />
          <span>Enable Push Notifications</span>
        </label>

        <div>
          <label className="block font-medium mb-2">Alert Level</label>
          <select
            value={alertLevel}
            onChange={(e) => setAlertLevel(e.target.value)}
            className="border p-2 rounded-lg w-48"
          >
            <option value="low">Low</option>
            <option value="moderate">Moderate</option>
            <option value="severe">Severe</option>
          </select>
        </div>

        <button
          onClick={handleSave}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          Save Settings
        </button>

        {saved && <p className="text-green-500 font-medium">✓ Settings saved!</p>}
      </div>
    </div>
  );
}

export default Settings;