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
  const [isRetrainModalOpen, setIsRetrainModalOpen] = useState(false);
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
    };
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let interval: any;
    if (isRetrainModalOpen) {
      const fetchRetrainStatus = async () => {
        try {
          const res = await fetch('http://127.0.0.1:8000/retrain/status');
          const data = await res.json();
          setRetrainStatus(data);
          // Auto close modal after successful completion and wait a bit
          if (data.status === 'completed') {
            setTimeout(() => setIsRetrainModalOpen(false), 3000);
          }
        } catch (e) {
          console.error(e);
        }
      };
      fetchRetrainStatus();
      interval = setInterval(fetchRetrainStatus, 1000);
    }
    return () => clearInterval(interval);
  }, [isRetrainModalOpen]);

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
            onClick={() => setIsRetrainModalOpen(true)}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-sm font-medium transition-colors shadow-[0_0_15px_rgba(79,70,229,0.3)]"
          >
            Huấn luyện lại Thủ công
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard id="STAT-001" title="Trạng thái" value={status?.state || 'Đang tải...'} icon={CheckCircle} status={status?.status === 'OK' ? 'good' : 'warning'} />
        <StatCard id="STAT-002" title="Chỉ số NDCG" value={metrics?.ndcg || '0.0'} icon={Activity} status="neutral" />
        <StatCard id="STAT-003" title="Trạng thái Trôi dạt" value={detectStatus?.is_drift ? 'PHÁT HIỆN LỖI' : 'Ổn định'} icon={AlertTriangle} status={detectStatus?.is_drift ? 'error' : 'good'} />
        <StatCard id="STAT-004" title="Điểm Trôi dạt" value={detectStatus?.drift_score || '0.0'} icon={Zap} status="neutral" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

        <div data-figma-id="CHART-002" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-slate-200">Độ trễ Hệ thống (Latency - ms)</h3>
            <span className="text-xs font-mono text-slate-600">CHART-002</span>
          </div>
          <div className="h-64">
            {metricsHistory.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={metricsHistory} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
                  <defs>
                    <linearGradient id="colorLatency" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#34d399" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#34d399" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                  <XAxis dataKey="timestamp" stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#64748b" fontSize={12} tickLine={false} axisLine={false} domain={[0, 'auto']} />
                  <RechartsTooltip 
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }}
                    itemStyle={{ color: '#34d399' }}
                  />
                  <Area type="monotone" dataKey="latency" name="Latency (ms)" stroke="#34d399" strokeWidth={2} fillOpacity={1} fill="url(#colorLatency)" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-full flex items-center justify-center text-slate-500">
                <p>Đang tải dữ liệu lịch sử...</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div data-figma-id="LIST-001" className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-slate-200">Sự kiện Trôi dạt Gần đây</h3>
            <button className="text-sm text-indigo-400 hover:text-indigo-300">Xem tất cả</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 uppercase bg-slate-800/50">
                <tr>
                  <th className="px-4 py-3 rounded-l-lg">Thời gian</th>
                  <th className="px-4 py-3">Loại</th>
                  <th className="px-4 py-3">Mức độ</th>
                  <th className="px-4 py-3 rounded-r-lg">Hành động</th>
                </tr>
              </thead>
              <tbody>
                {detectStatus?.is_drift ? (
                  <tr className="border-b border-slate-800/50">
                    <td className="px-4 py-3 text-slate-300">Vừa xong</td>
                    <td className="px-4 py-3 text-slate-300">Phát hiện Trôi dạt</td>
                    <td className="px-4 py-3"><span className="px-2 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded text-xs">Cao (Score: {detectStatus.drift_score})</span></td>
                    <td className="px-4 py-3 text-slate-400">Kích hoạt Phân tích</td>
                  </tr>
                ) : (
                  <tr>
                    <td colSpan={4} className="px-4 py-6 text-center text-slate-500 text-sm">
                      Không phát hiện sự kiện trôi dạt nào gần đây.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

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

      {isRetrainModalOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 w-full max-w-lg shadow-2xl animate-in zoom-in-95 duration-200">
            <h2 className="text-xl font-bold text-slate-100 mb-2 flex items-center gap-2">
              <Zap className="w-5 h-5 text-indigo-400" /> Huấn luyện Thích ứng (Adaptive Learning)
            </h2>
            
            <div className="bg-slate-800/50 p-4 rounded-lg border border-slate-700 mb-6 text-sm text-slate-300 space-y-3">
              <p>
                <strong className="text-rose-400">Tại sao phải Huấn luyện lại?</strong><br/>
                Hệ thống phát hiện luồng dữ liệu tương tác thực tế (Live Traffic) đang chệch hướng nghiêm trọng so với kiến thức cũ của AI (Concept Drift). Nếu không can thiệp, AI sẽ tiếp tục gợi ý sai.
              </p>
              <p>
                <strong className="text-emerald-400">Quá trình này làm gì?</strong><br/>
                Nó sẽ gom toàn bộ dữ liệu mới nhất (bao gồm cả dữ liệu nhiễu), đẩy vào Pipeline và ép mô hình SVD cập nhật lại trọng số ma trận. Khi học xong, nó sẽ Hot-swap (thay nóng) vào bộ nhớ để hệ thống hoạt động chính xác trở lại.
              </p>
            </div>

            <div className="mb-6">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-400">Tiến độ:</span>
                <span className="font-mono text-indigo-400">{retrainStatus?.progress || 0}%</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-3">
                <div 
                  className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-500" 
                  style={{ width: `${retrainStatus?.progress || 0}%` }}
                ></div>
              </div>
              <p className="text-xs text-slate-500 mt-2 text-center h-4">
                {retrainStatus?.message || "Đang chờ khởi chạy..."}
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <button 
                onClick={() => setIsRetrainModalOpen(false)}
                className="px-4 py-2 bg-transparent hover:bg-slate-800 text-slate-300 rounded-lg text-sm font-medium transition-colors"
                disabled={retrainStatus?.status === 'running' || retrainStatus?.status === 'starting'}
              >
                Đóng
              </button>
              <button 
                onClick={handleStartRetrain}
                disabled={retrainStatus?.status === 'running' || retrainStatus?.status === 'starting'}
                className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg text-sm font-medium transition-colors shadow-lg"
              >
                {retrainStatus?.status === 'running' || retrainStatus?.status === 'starting' ? 'Đang Huấn luyện...' : 'Bắt đầu Huấn luyện'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
