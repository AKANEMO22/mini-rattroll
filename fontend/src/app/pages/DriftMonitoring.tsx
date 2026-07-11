import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, TrendingDown, Thermometer, BarChart2, ShieldCheck, ChevronRight, Zap, PlayCircle, RefreshCw } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { api } from '../services/api';

export default function DriftMonitoring() {
  const [detectStatus, setDetectStatus] = useState<any>(null);
  const [retrainStatus, setRetrainStatus] = useState<any>(null);

  const renderHeatmap = () => {
    if (!detectStatus?.heatmap_data || detectStatus.heatmap_data.length === 0) {
      return (
        <div className="h-64 flex flex-col items-center justify-center text-slate-500 bg-slate-950 rounded-lg border border-slate-800">
          Chưa đủ dữ liệu Cụm...
        </div>
      );
    }

    const bins = ["1.0", "1.5", "2.0", "2.5", "3.0", "3.5", "4.0", "4.5"];
    
    return (
      <div className="overflow-auto bg-slate-950 rounded-lg p-4 border border-slate-800 h-64">
        <div className="flex text-xs text-slate-400 mb-2">
          <div className="w-20 flex-shrink-0"></div>
          {bins.map(b => (
            <div key={b} className="flex-1 text-center font-mono">{b}</div>
          ))}
        </div>
        
        {detectStatus.heatmap_data.map((row: any, i: number) => (
          <div key={i} className="flex items-center mb-1">
            <div className="w-20 flex-shrink-0 text-xs text-slate-300 font-medium">
              {row.cluster}
            </div>
            {bins.map(b => {
              const val = row[b] || 0;
              let bgColor = "bg-slate-800";
              if (val < -10) bgColor = "bg-rose-600";
              else if (val < -5) bgColor = "bg-rose-500/80";
              else if (val < -1) bgColor = "bg-rose-500/40";
              else if (val > 10) bgColor = "bg-emerald-500";
              else if (val > 5) bgColor = "bg-emerald-500/80";
              else if (val > 1) bgColor = "bg-emerald-500/40";
              
              return (
                <div 
                  key={b} 
                  className={`flex-1 h-4 mx-0.5 rounded-sm ${bgColor} transition-colors cursor-pointer group relative`}
                >
                  <div className="absolute hidden group-hover:block bottom-full mb-1 left-1/2 -translate-x-1/2 bg-slate-800 text-slate-200 text-[10px] px-1.5 py-0.5 rounded shadow-lg z-10 whitespace-nowrap">
                    {val > 0 ? '+' : ''}{val}%
                  </div>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    );
  };
  
  // Use real distribution data from the API if available
  const getChartData = () => {
    if (detectStatus?.chart_data && detectStatus.chart_data.length > 0) {
      return detectStatus.chart_data;
    }
    return [];
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
            <p className={`text-2xl font-bold ${detectStatus?.ctr_fluctuation >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {detectStatus?.ctr_fluctuation > 0 ? '+' : ''}{detectStatus?.ctr_fluctuation ?? '--'}%
            </p>
            {detectStatus?.ctr_fluctuation < 0 && <TrendingDown className="w-5 h-5 text-rose-400 mb-1" />}
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
          {renderHeatmap()}
        </div>
      </div>


    </div>
  );
}
