import { BrowserRouter, Link, NavLink, Route, Routes } from "react-router-dom";
import { GalleryPage } from "./pages/GalleryPage";
import { LivePage } from "./pages/LivePage";
import { TechPage } from "./pages/TechPage";

function Nav() {
  const base = "px-4 py-2 text-sm font-medium rounded-lg transition-colors";
  const active = "bg-indigo-600 text-white";
  const inactive = "text-gray-400 hover:text-white hover:bg-gray-800";

  return (
    <nav className="bg-gray-950 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link to="/" className="text-white font-bold text-lg">
          LLManim <span className="text-indigo-400">Exhibition</span>
        </Link>
        <div className="flex items-center gap-1">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
          >
            Gallery
          </NavLink>
          <NavLink
            to="/tech"
            className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
          >
            Tech
          </NavLink>
          <NavLink
            to="/live"
            className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
          >
            Live
          </NavLink>
        </div>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="bg-gray-950 min-h-screen">
        <Nav />
        <Routes>
          <Route path="/" element={<GalleryPage />} />
          <Route path="/tech" element={<TechPage />} />
          <Route path="/live" element={<LivePage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
