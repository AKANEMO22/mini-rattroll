import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, NavLink } from 'react-router';
import { 
  LayoutDashboard, 
  Film, 
  Search, 
  Users, 
  Database, 
  Box, 
  Settings2, 
  Activity, 
  PlayCircle, 
  BarChart2, 
  Beaker,
  FileText,
  Settings
} from 'lucide-react';

import Dashboard from './pages/Dashboard';
import MovieRecommendation from './pages/MovieRecommendation';
import UserProfile from './pages/UserProfile';
import DriftMonitoring from './pages/DriftMonitoring';
import Simulation from './pages/Simulation';
import Evaluation from './pages/Evaluation';

const Sidebar = () => {
  const navItems = [
    { name: 'Tổng quan', path: '/', icon: LayoutDashboard },
    { name: 'Gợi ý Phim', path: '/recommendations', icon: Film },
    { name: 'Người dùng', path: '/users', icon: Users },
    { name: 'Giám sát Trôi dạt', path: '/drift-monitoring', icon: Activity },
    { name: 'Mô phỏng', path: '/simulation', icon: PlayCircle },
    { name: 'Đánh giá', path: '/evaluation', icon: BarChart2 },
  ];

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-full overflow-y-auto">
      <div className="p-6">
        <h1 className="text-xl font-bold text-indigo-400 flex items-center gap-2">
          <Activity className="w-6 h-6" />
          Nexus AI
        </h1>
        <p className="text-xs text-slate-500 mt-1 uppercase tracking-wider font-semibold">Nền tảng Đề xuất</p>
      </div>
      
      <nav className="flex-1 px-4 pb-6 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2 rounded-lg transition-colors text-sm font-medium ${
                  isActive 
                    ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' 
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              {item.name}
            </NavLink>
          );
        })}
      </nav>
      
      <div className="p-4 border-t border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-medium text-slate-300">
            AI
          </div>
          <div className="text-sm">
            <p className="font-medium text-slate-300">Quản trị Hệ thống</p>
            <p className="text-xs text-slate-500">v2.4.1 Stable</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const Header = () => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/50 backdrop-blur flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <span className="px-2 py-1 rounded text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
          Hệ thống Ổn định
        </span>
        <span className="text-sm text-slate-400">Mô hình: <strong className="text-slate-200">Hybrid-MF-v4 (Đang chạy)</strong></span>
      </div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-400">Tập dữ liệu: MovieLens 25M</span>
        <button className="p-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors">
          <Activity className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
};

const Layout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans overflow-hidden selection:bg-indigo-500/30">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          {children}
        </main>
      </div>
    </div>
  );
};

const PlaceholderPage = ({ title }: { title: string }) => (
  <div className="flex flex-col items-center justify-center h-full text-slate-400 space-y-4">
    <Settings2 className="w-12 h-12 text-slate-600" />
    <h2 className="text-xl font-semibold text-slate-300">{title}</h2>
  </div>
);

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/recommendations" element={<MovieRecommendation />} />
          <Route path="/users" element={<UserProfile />} />
          <Route path="/drift-monitoring" element={<DriftMonitoring />} />
          <Route path="/simulation" element={<Simulation />} />
          <Route path="/evaluation" element={<Evaluation />} />
          
          {/* Catch-all for other pages */}
          <Route path="*" element={<PlaceholderPage title="Trang không tồn tại" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
