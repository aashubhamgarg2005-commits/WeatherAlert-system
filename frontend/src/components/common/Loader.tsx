function Loader() {
  return (
    <div
      role="status"
      aria-label="Loading"
      className="flex justify-center items-center p-10"
    >
      <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600"></div>
    </div>
  );
}

export default Loader;