export default function Dashboard({ onLogout }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold text-green-600">🎉 Welcome to the Dashboard!</h1>
      <button className="btn btn-error mt-6" onClick={onLogout}>Logout</button>
    </div>
  );
}
