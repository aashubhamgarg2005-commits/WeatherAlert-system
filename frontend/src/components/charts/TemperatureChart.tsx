import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

const data = [
  { time: "9AM", temp: 28 },
  { time: "12PM", temp: 34 },
  { time: "3PM", temp: 36 },
  { time: "6PM", temp: 30 },
];

function TemperatureChart() {
  return (
    <div className="bg-white shadow rounded-xl p-5">
      <h2 className="font-bold mb-5">Temperature Trend</h2>

      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="time" />
            <YAxis />

            <Tooltip />

            <Line
              type="monotone"
              dataKey="temp"
              stroke="#f97316"
              strokeWidth={3}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default TemperatureChart;