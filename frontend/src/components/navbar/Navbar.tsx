import { Bell, User } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

function Navbar() {
  const { logout } = useAuth();

  return (
    <nav className="h-16 bg-white shadow flex items-center justify-between px-6">
      
      <h1 className="text-xl font-bold text-blue-600">
        Weather Alert System
      </h1>

      <div className="flex items-center gap-5">

        {/* Notifications */}
        <button className="relative">
          <Bell size={22} />

          <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full px-1">
            3
          </span>
        </button>

        {/* User */}
        <div className="flex items-center gap-2">
          <User size={22} />

          <span>Admin</span>
        </div>

        {/* Logout */}
        <button
          onClick={logout}
          className="bg-red-500 text-white px-3 py-2 rounded"
        >
          Logout
        </button>

      </div>
    </nav>
  );
}

export default Navbar;