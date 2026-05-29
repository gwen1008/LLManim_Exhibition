import { BrowserRouter, Link, NavLink, Route, Routes } from "react-router-dom";
import { Sparkles } from "lucide-react";
import { GalleryPage } from "./pages/GalleryPage";
import { LivePage } from "./pages/LivePage";
import { TechPage } from "./pages/TechPage";

function Nav() {
  const base =
    "px-4 py-2 text-sm font-medium rounded-lg transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400";
  const active = "bg-emerald-500 text-slate-950";
  const inactive = "text-gray-300 hover:text-white hover:bg-gray-800";

  return (
    <nav
      aria-label="主導覽"
      className="bg-gray-950/80 backdrop-blur border-b border-gray-800 sticky top-0 z-40 supports-[backdrop-filter]:bg-gray-950/60"
    >
      <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link
          to="/"
          className="text-white font-bold text-lg flex items-center gap-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 rounded-md px-1"
        >
          <Sparkles className="size-5 text-emerald-400" aria-hidden="true" />
          <span>
            LLManim <span className="text-emerald-400">Exhibition</span>
          </span>
        </Link>
        <div className="flex items-center gap-1">
          <NavLink to="/" end className={({ isActive }) => `${base} ${isActive ? active : inactive}`}>
            Gallery
          </NavLink>
          <NavLink to="/tech" className={({ isActive }) => `${base} ${isActive ? active : inactive}`}>
            Tech
          </NavLink>
          <NavLink to="/live" className={({ isActive }) => `${base} ${isActive ? active : inactive}`}>
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
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 focus:bg-emerald-500 focus:text-slate-950 focus:px-3 focus:py-2 focus:rounded-md"
      >
        跳至主內容
      </a>
      <div className="bg-gray-950 min-h-dvh">
        <Nav />
        <main id="main-content" tabIndex={-1} className="scroll-mt-16 focus:outline-none">
          <Routes>
            <Route path="/" element={<GalleryPage />} />
            <Route path="/tech" element={<TechPage />} />
            <Route path="/live" element={<LivePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
