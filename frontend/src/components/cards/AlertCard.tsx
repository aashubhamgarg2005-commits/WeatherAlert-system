interface Props {
  type: string;
  message: string;
  severity: "low" | "medium" | "high";
}

function AlertCard({ type, message, severity }: Props) {
  const severityColor =
    severity === "high"
      ? "text-red-600"
      : severity === "medium"
      ? "text-yellow-600"
      : "text-green-600";

  const borderColor =
    severity === "high"
      ? "border-red-500"
      : severity === "medium"
      ? "border-yellow-500"
      : "border-green-500";

  return (
    <div className={`bg-white shadow rounded-xl p-5 border-l-4 ${borderColor}`}>
      <div className="flex justify-between">
        <h3 className="font-bold">{type}</h3>

        <span className={`font-semibold ${severityColor}`}>
          {severity}
        </span>
      </div>

      <p className="mt-3 text-gray-600">{message}</p>
    </div>
  );
}

export default AlertCard;