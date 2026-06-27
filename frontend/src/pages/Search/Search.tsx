import { useState } from "react";
import useWeather from "../../hooks/useWeather";
import WeatherCard from "../../components/cards/WeatherCard";

function Search() {
  const [city, setCity] = useState("");

  const { data, loading, error, fetchWeather } = useWeather();

  const handleSearch = () => {
    if (city.trim()) {
      const formatted = city.trim().charAt(0).toUpperCase() + city.trim().slice(1).toLowerCase();
fetchWeather(formatted);
    }
  };

  return (
    <div className="space-y-6">

      <h1 className="text-3xl font-bold">
        Search Weather
      </h1>

      {/* Search Box */}
      <div className="flex gap-3">

        <input
          type="text"
          placeholder="Enter city name"
          className="border p-3 rounded-lg w-80"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()}
        />

        <button
          onClick={handleSearch}
          className="bg-blue-600 text-white px-6 rounded-lg"
        >
          Search
        </button>

      </div>

      {/* Loading */}
      {loading && (
        <p className="text-gray-500">
          Loading weather data...
        </p>
      )}

      {/* Error */}
      {error && (
        <p className="text-red-500">
          {error}
        </p>
      )}

      {/* Empty state */}
      {!loading && !data && !error && (
        <p className="text-gray-400">
          Search a city to get weather information
        </p>
      )}

      {/* Result */}
      {data && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">

          <WeatherCard title="City" value={data.city} />

          <WeatherCard
            title="Temperature"
            value={`${data.temperature}°C`}
          />

          <WeatherCard
            title="Humidity"
            value={`${data.humidity}%`}
          />

          <WeatherCard
            title="Wind Speed"
            value={`${data.windSpeed} km/h`}
          />

        </div>
      )}

    </div>
  );
}

export default Search;