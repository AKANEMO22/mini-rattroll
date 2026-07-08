import React, { useState } from 'react';
import { User, History, PieChart, Tag, Search, Info, Film, Star, RefreshCw } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { api } from '../services/api';

export default function UserProfile() {
  const [userId, setUserId] = useState('');
  const [profileData, setProfileData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    if (!userId) return;
    setIsLoading(true);
    const res = await api.getUserProfile(parseInt(userId));
    setProfileData(res);
    setIsLoading(false);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Hồ sơ Người dùng</h1>
        <p className="text-sm text-slate-400 mt-1">Phân tích hành vi, lịch sử tương tác và cụm sở thích (Cluster)</p>
      </div>

      <div data-figma-id="USR-SEARCH" className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex gap-4">
        <div className="flex-1 relative">
          <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input 
            type="text" 
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="w-full bg-slate-950 border border-slate-700 rounded-lg py-2.5 pl-10 pr-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            placeholder="Nhập Mã Người Dùng (VD: 55)..."
          />
        </div>
        <button 
          onClick={handleSearch}
          disabled={isLoading}
          className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-600/50 text-white rounded-lg text-sm font-medium transition-colors shadow-[0_0_15px_rgba(79,70,229,0.3)] flex items-center gap-2">
          {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : null}
          {isLoading ? 'Đang xử lý...' : 'Tra cứu'}
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div data-figma-id="USR-INFO" className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex flex-col items-center pb-6 border-b border-slate-800 mb-6">
            <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mb-4 border-2 border-indigo-500/50">
              <User className="w-10 h-10 text-indigo-400" />
            </div>
            <h2 className="text-xl font-bold text-slate-200">{profileData ? `Người dùng ${profileData.user_id}` : 'Chưa chọn'}</h2>
            <p className="text-sm text-slate-400 mt-1">Trạng thái: Hoạt động</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <span className="text-xs text-slate-500 uppercase">Cụm sở thích (Cluster)</span>
              <p className="text-sm font-medium text-slate-300 mt-1 flex items-center gap-2">
                <Tag className="w-4 h-4 text-emerald-400" />
                {profileData ? 'Cluster-A' : '---'}
              </p>
            </div>
            <div>
              <span className="text-xs text-slate-500 uppercase">Tổng số tương tác</span>
              <p className="text-sm font-medium text-slate-300 mt-1 flex items-center gap-2">
                <History className="w-4 h-4 text-indigo-400" />
                {profileData ? `${profileData.interaction_count} đánh giá (AVG: ${profileData.avg_rating}⭐)` : '0 đánh giá'}
              </p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-6">
          <div data-figma-id="USR-CHART" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="font-semibold text-slate-200 mb-4">Phân bổ Sở thích (Genres)</h3>
            <div className="h-48 flex flex-col items-center justify-center text-slate-500 rounded-lg bg-slate-950/50">
              {profileData?.genre_distribution?.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={profileData.genre_distribution} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <XAxis type="number" hide />
                    <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} width={100} />
                    <Tooltip 
                      cursor={{fill: '#334155', opacity: 0.4}}
                      contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '0.5rem', color: '#f1f5f9'}}
                      itemStyle={{color: '#818cf8'}}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                      {profileData.genre_distribution.map((entry: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={index === 0 ? '#6366f1' : '#4f46e5'} opacity={1 - index * 0.1} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full w-full border border-dashed border-slate-700 rounded-lg flex items-center justify-center">
                  <PieChart className="w-8 h-8 mb-2 opacity-50" />
                </div>
              )}
            </div>
          </div>

          <div data-figma-id="USR-HISTORY" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold text-slate-200">Lịch sử Đánh giá (Ratings)</h3>
              <span className="text-xs font-mono text-slate-600">TABLE-001</span>
            </div>
            <div className="overflow-x-auto text-slate-500 border border-slate-700 rounded-lg bg-slate-950/50">
              {profileData?.history?.length > 0 ? (
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-slate-500 uppercase bg-slate-900/80">
                    <tr>
                      <th className="px-4 py-3">Thời gian</th>
                      <th className="px-4 py-3">Tên Phim</th>
                      <th className="px-4 py-3 text-right">Đánh giá</th>
                    </tr>
                  </thead>
                  <tbody>
                    {profileData.history.map((h: any, idx: number) => (
                      <tr key={idx} className="border-b border-slate-800/50 hover:bg-slate-900/50 transition-colors">
                        <td className="px-4 py-3 text-slate-400 whitespace-nowrap">{h.date}</td>
                        <td className="px-4 py-3 text-slate-200 font-medium">
                          {h.title}
                          {h.genres && <div className="text-xs text-slate-500 font-normal truncate max-w-[200px]">{h.genres}</div>}
                        </td>
                        <td className="px-4 py-3 text-right">
                          <span className="inline-flex items-center gap-1 text-amber-400 font-bold bg-amber-400/10 px-2 py-0.5 rounded">
                            {h.rating} <Star className="w-3 h-3 fill-current" />
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <div className="h-48 flex items-center justify-center">
                  <Info className="w-8 h-8 mb-2 opacity-50" />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
