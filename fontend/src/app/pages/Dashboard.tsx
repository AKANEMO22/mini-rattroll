import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, AreaChart, Area,
  BarChart, Bar
} from 'recharts';
import { Activity, AlertTriangle, CheckCircle, Clock, Zap, TrendingUp, Users, Film } from 'lucide-react';
import { api } from '../services/api';

const StatCard = ({ title, value, icon: Icon, trend, status, id }: any) => (
  <div data-figma-id={id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 relative overflow-hidden group hover:border-slate-700 transition-colors">
    <div className="absolute top-2 right-2 text-[10px] text-slate-700 font-mono opacity-0 group-hover:opacity-100 transition-opacity">{id}</div>
    <div className="flex justify-between items-start mb-4">
      <div className="p-2 bg-slate-800 rounded-lg">
        <Icon className={`w-5 h-5 ${status === 'good' ? 'text-emerald-400' : status === 'warning' ? 'text-amber-400' : status === 'error' ? 'text-rose-400' : 'text-indigo-400'}`} />
      </div>
      {trend && (
        <span className={`flex items-center text-xs font-medium ${trend > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
          {trend > 0 ? '+' : ''}{trend}%
        </span>
      )}
    </div>
    <h3 className="text-slate-400 text-sm font-medium mb-1">{title}</h3>
    <p className="text-2xl font-bold text-slate-100">{value}</p>
  </div>
);

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [detectStatus, setDetectStatus] = useState<any>(null);
  const [metricsHistory, setMetricsHistory] = useState<any[]>([]);
  const [retrainStatus, setRetrainStatus] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      const st = await api.getSystemStatus();
      const m = await api.getMetrics();
      const d = await api.getDetectStatus();
      const history = await api.getMetricsHistory();
      setStatus(st);
      setMetrics(m);
      setDetectStatus(d);
      setMetricsHistory(history);
      
      try {
        const res = await fetch('http://127.0.0.1:8000/retrain/status');
        const data = await res.json();
        setRetrainStatus(data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 2000); // Tăng tốc độ poll lên một chút để xem tiến độ mượt hơn
    return () => clearInterval(interval);
  }, []);

  const handleStartRetrain = async () => {
    try {
      await fetch('http://127.0.0.1:8000/retrain/start', { method: 'POST' });
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500 relative">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Tổng quan Hệ thống</h1>
          <p className="text-sm text-slate-400 mt-1">Chỉ số thời gian thực của Hệ thống Khuyến nghị Thích ứng</p>
        </div>
        <div className="flex gap-2">
          <button data-figma-id="BTN-001" className="px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg text-sm font-medium transition-colors">
            Xuất Báo cáo
          </button>
          <button 
            data-figma-id="BTN-002" 
            onClick={handleStartRetrain}
            disabled={retrainStatus?.status === 'starting' || retrainStatus?.status === 'running'}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-600/50 text-white rounded-lg text-sm font-medium transition-colors shadow-[0_0_15px_rgba(79,70,229,0.3)]"
          >
            {retrainStatus?.status === 'starting' || retrainStatus?.status === 'running' ? 'Đang Huấn luyện...' : 'Huấn luyện lại Thủ công'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard id="STAT-001" title="Trạng thái" value={status?.state || 'Đang tải...'} icon={CheckCircle} status={status?.status === 'OK' ? 'good' : 'warning'} />
        <StatCard id="STAT-002" title="Chỉ số NDCG" value={metrics?.ndcg || '0.0'} icon={Activity} status="neutral" />
        <StatCard id="STAT-003" title="Trạng thái Trôi dạt" value={detectStatus?.is_drift ? 'PHÁT HIỆN LỖI' : 'Ổn định'} icon={AlertTriangle} status={detectStatus?.is_drift ? 'error' : 'good'} />
        <StatCard id="STAT-004" title="Điểm Trôi dạt" value={detectStatus?.drift_score || '0.0'} icon={Zap} status="neutral" />
      </div>

      <div className="grid grid-cols-1 gap-6">
        <div data-figma-id="CHART-001" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-slate-200">Độ chính xác Khuyến nghị (RMSE)</h3>
            <span className="text-xs font-mono text-slate-600">CHART-001</span>
          </div>
          <div className="h-64">
            {metricsHistory.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={metricsHistory} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="timestamp" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} domain={['auto', 'auto']} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }}
                    itemStyle={{ color: '#818cf8' }}
                  />
                  <Line type="monotone" dataKey="rmse" name="RMSE" stroke="#818cf8" strokeWidth={3} dot={{ r: 4, fill: '#818cf8', strokeWidth: 0 }} activeDot={{ r: 6, fill: '#fff' }} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-500">
                <p>Đang tải dữ liệu lịch sử...</p>
              </div>
            )}
          </div>
        </div>


      </div>

      <div className="grid grid-cols-1 gap-6">

        <div data-figma-id="PANEL-001" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="font-semibold text-slate-200 mb-4">Trạng thái Huấn luyện lại</h3>
          <div className="h-48 flex flex-col items-center justify-center text-slate-500 border border-dashed border-slate-700 rounded-lg bg-slate-950/50 p-4 text-center">
            {retrainStatus?.status === 'running' || retrainStatus?.status === 'starting' ? (
              <div className="w-full">
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-indigo-400">{retrainStatus.message}</span>
                  <span className="text-slate-300">{retrainStatus.progress}%</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2">
                  <div className="bg-indigo-500 h-2 rounded-full transition-all duration-500" style={{ width: `${retrainStatus.progress}%` }}></div>
                </div>
              </div>
            ) : retrainStatus?.status === 'completed' ? (
              <div className="text-emerald-400 text-sm">
                <CheckCircle className="w-8 h-8 mx-auto mb-2 text-emerald-500" />
                Mô hình đã được cập nhật thành công!
              </div>
            ) : (
              <p className="text-sm">Chưa có tiến trình học nào đang chạy.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
