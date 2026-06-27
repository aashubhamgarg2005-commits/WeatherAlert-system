import {
  Home,
  AlertTriangle,
  Search,
  Cloud,
  History,
  BarChart3,
  Settings,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menu = [
  { name: "Dashboard", path: "/", icon: Home },
  { name: "Alerts", path: "/alerts", icon: AlertTriangle },
  { name: "Search", path: "/search", icon: Search },
  { name: "Forecast", path: "/forecast", icon: Cloud },
  { name: "History", path: "/history", icon: History },
  { name: "Analytics", path: "/analytics", icon: BarChart3 },
  { name: "Settings", path: "/settings", icon: Settings },
];

function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white p-5">

      <h2 className="text-2xl font-bold mb-8">
        Weather AI
      </h2>

      <nav className="space-y-3">

        {menu.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 p-3 rounded-lg transition
                ${isActive
                  ? "bg-blue-600 text-white"
                  : "hover:bg-slate-700 text-gray-300"}`
              }
              aria-current={({ isActive }) => (isActive ? "page" : undefined)}
            >
              <Icon size={20} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}

      </nav>
    </aside>
  );
}

export default Sidebar;