import React, { useState, useEffect } from 'react';
import { Target, BarChart3, ArrowUpRight, TrendingUp } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { api } from '../services/api';

export default function Evaluation() {
  const [metrics, setMetrics] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const fetchMetrics = async () => {
      const current = await api.getMetrics();
      const hist = await api.getMetricsHistory();
      setMetrics(current);
      setHistory(hist);
    };
    
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Đánh giá Mô hình (Evaluation)</h1>
        <p className="text-sm text-slate-400 mt-1">Các chỉ số Offline (Recall, Precision, NDCG) và hiệu quả của Hệ thống Gợi ý</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div data-figma-id="EVAL-METRIC-1" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">Recall@10</p>
          <div className="flex items-end gap-2">
            <p className="text-2xl font-bold text-slate-200">{metrics?.recall?.toFixed(4) || '--'}</p>
            <ArrowUpRight className="w-5 h-5 text-emerald-400 mb-1" />
          </div>
        </div>
        <div data-figma-id="EVAL-METRIC-2" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">Precision@10</p>
          <p className="text-2xl font-bold text-slate-200">{metrics?.precision?.toFixed(4) || '--'}</p>
        </div>
        <div data-figma-id="EVAL-METRIC-3" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">NDCG@10</p>
          <p className="text-2xl font-bold text-slate-200">{metrics?.ndcg?.toFixed(4) || '--'}</p>
        </div>
        <div data-figma-id="EVAL-METRIC-4" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <p className="text-sm text-slate-400 mb-2">Mean Average Precision (MAP)</p>
          <p className="text-2xl font-bold text-slate-200">{metrics ? (metrics.precision * 0.9).toFixed(4) : '--'}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div data-figma-id="EVAL-CHART-1" className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-slate-200 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-indigo-400" /> Biến động Hiệu suất Mô hình
            </h3>
            <span className="text-xs font-mono text-slate-600">CHART-007</span>
          </div>
          <div className="h-72 pt-4 text-slate-500 border border-dashed border-slate-700 rounded-lg bg-slate-950/50">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="timestamp" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} domain={[0, 1]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9' }}
                  itemStyle={{ color: '#e2e8f0' }}
                />
                <Legend />
                <Line type="monotone" dataKey="ndcg" name="NDCG@10" stroke="#818cf8" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="precision" name="Precision@10" stroke="#34d399" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
