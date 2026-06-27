import { CloudSun } from "lucide-react";

interface Props {
  title: string;
  value: string | number;
  unit?: string;
}

function WeatherCard({ title, value, unit }: Props) {
  return (
    <div className="bg-white rounded-xl shadow p-5 flex items-center justify-between">
      <div>
        <p className="text-gray-500 text-sm">{title}</p>

        <h2 className="text-2xl font-bold mt-2">
          {value} {unit && <span className="text-base font-medium">{unit}</span>}
        </h2>
      </div>

      <CloudSun className="text-blue-500" size={35} />
    </div>
  );
}

export default WeatherCard;

