interface Props {
  message: string;
}

function ErrorMessage({ message }: Props) {
  return (
    <div
      role="alert"
      className="bg-red-100 border border-red-300 text-red-700 p-4 rounded-lg flex items-center gap-2"
    >
      <span className="font-semibold">⚠️ Error:</span>
      <span>{message}</span>
    </div>
  );
}

export default ErrorMessage;