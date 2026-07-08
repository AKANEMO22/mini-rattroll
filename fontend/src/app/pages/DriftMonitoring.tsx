import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, TrendingDown, Thermometer, BarChart2 } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../services/api';

export default function DriftMonitoring() {
  const [detectStatus, setDetectStatus] = useState<any>(null);
  
  // Generate distribution data for the chart based on drift state
  const getChartData = () => {
    const isDrift = detectStatus?.is_drift;
    const data = [];
    for (let i = 1; i <= 5; i += 0.5) {
      // Baseline is centered around 4.0
      const baseline = Math.exp(-Math.pow(i - 4.0, 2) / 0.5) * 100;
      // Current shifts to 2.5 if drifted, otherwise stays near baseline
      const center = isDrift ? 2.5 : 3.9;
      const current = Math.exp(-Math.pow(i - center, 2) / 0.5) * 100;
      
      data.push({
        rating: i.toFixed(1),
        baseline: Math.round(baseline),
        current: Math.round(current)
      });
    }
    return data;
  };

  const chartData = getChartData();

  useEffect(() => {
    // Poll the detect status every 2 seconds to make it real-time
    const fetchStatus = async () => {
      const status = await api.getDetectStatus();
      setDetectStatus(status);
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Giám sát Trôi dạt (Drift Monitoring)</h1>
          <p className="text-sm text-slate-400 mt-1">Phân tích chuyên sâu về sự phân kỳ dữ liệu và thay đổi hành vi người dùng</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div data-figma-id="DRIFT-STAT-1" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">Biến động CTR</p>
          <div className="flex items-end gap-2">
            <p className="text-2xl font-bold text-slate-200">-1.2%</p>
            <TrendingDown className="w-5 h-5 text-rose-400 mb-1" />
          </div>
        </div>
        <div data-figma-id="DRIFT-STAT-2" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">KS-Test (Rating Dist P-Value)</p>
          <p className={`text-2xl font-bold ${detectStatus?.is_drift ? 'text-rose-400' : 'text-emerald-400'}`}>
            {detectStatus ? detectStatus.p_value : '--'}
          </p>
        </div>
        <div data-figma-id="DRIFT-STAT-3" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">Drift Score (KS Statistic)</p>
          <p className="text-2xl font-bold text-slate-200">
            {detectStatus ? detectStatus.drift_score : '--'}
          </p>
        </div>
        <div data-figma-id="DRIFT-STAT-4" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">Trạng thái (Status)</p>
          <p className={`text-2xl font-bold ${detectStatus?.is_drift ? 'text-rose-400' : 'text-emerald-400'}`}>
            {detectStatus ? (detectStatus.is_drift ? 'DRIFT DETECTED' : 'NORMAL') : '--'}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div data-figma-id="DRIFT-CHART-1" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-slate-200 flex items-center gap-2">
              <BarChart2 className="w-5 h-5 text-indigo-400" /> Phân phối Rating (Baseline vs Current)
            </h3>
            <span className="text-xs font-mono text-slate-600">CHART-005</span>
          </div>
          <div className="h-64 pt-4 text-slate-500 border border-dashed border-slate-700 rounded-lg bg-slate-950/50">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorBaseline" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#818cf8" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#818cf8" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorCurrent" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#fb7185" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#fb7185" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="rating" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Area type="monotone" dataKey="baseline" name="Baseline (Ideal)" stroke="#818cf8" strokeWidth={2} fillOpacity={1} fill="url(#colorBaseline)" />
                <Area type="monotone" dataKey="current" name="Current" stroke="#fb7185" strokeWidth={2} fillOpacity={1} fill="url(#colorCurrent)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div data-figma-id="DRIFT-HEATMAP" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-slate-200">Heatmap Cảnh báo</h3>
            <span className="text-xs font-mono text-slate-600">CHART-005</span>
          </div>
          <div className="h-64 flex flex-col items-center justify-center text-slate-500 bg-slate-950 rounded-lg border border-slate-800">
            {/* Empty UI */}
          </div>
        </div>
      </div>

      <div data-figma-id="DRIFT-TABLE" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="font-semibold text-slate-200 mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-rose-400" /> Lịch sử Cảnh báo
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-500 uppercase bg-slate-800/50">
              <tr>
                <th className="px-4 py-3 rounded-l-lg">Thời gian</th>
                <th className="px-4 py-3">Loại Trôi dạt</th>
                <th className="px-4 py-3">P-Value</th>
                <th className="px-4 py-3">Thành phần bị Ảnh hưởng</th>
                <th className="px-4 py-3 rounded-r-lg">Quyết định</th>
              </tr>
            </thead>
            <tbody>
              {detectStatus?.is_drift ? (
                <tr className="bg-rose-500/10 border-b border-slate-800/50">
                  <td className="px-4 py-3 text-slate-300">{new Date().toLocaleTimeString()}</td>
                  <td className="px-4 py-3 text-rose-400 font-medium">Concept Drift</td>
                  <td className="px-4 py-3 text-slate-300 font-mono">{detectStatus.p_value}</td>
                  <td className="px-4 py-3 text-slate-300">Distribution of Recommendation Scores</td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-1 rounded bg-rose-500/20 text-rose-400 text-xs border border-rose-500/30">
                      Trigger Retraining
                    </span>
                  </td>
                </tr>
              ) : (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-slate-500">
                    Chưa có cảnh báo nào trong hệ thống. (Hệ thống Ổn định)
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
