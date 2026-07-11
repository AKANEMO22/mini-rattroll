import React, { useState } from 'react';
import { PlayCircle, Zap, AlertTriangle, CheckCircle, RefreshCw, Terminal } from 'lucide-react';
import { api } from '../services/api';

export default function Simulation() {
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);

  const fetchLogs = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/simulate/logs');
      const data = await res.json();
      setLogs(data);
    } catch (e) {
      console.error("Failed to fetch logs", e);
    }
  };

  React.useEffect(() => {
    fetchLogs();
  }, []);

  const handleSimulate = async (type: string) => {
    setIsSimulating(true);
    setSimulationResult(null);
    setLogs([]);
    const severity = type === 'None' ? 0.0 : 0.8;
    const res = await api.simulateDrift(type, severity);
    setSimulationResult({ type, ...res });
    await fetchLogs();
    setIsSimulating(false);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Mô phỏng (Simulation Engine)</h1>
        <p className="text-sm text-slate-400 mt-1">Công cụ bơm nhiễu nhân tạo (Synthetic Drift Injection) để kiểm thử Hệ thống Thích ứng</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { id: 'Preference Drift', name: 'Preference Drift', desc: 'Bơm 200 đánh giá rác (điểm 1.0 - 2.0) vào luồng thời gian thực.' },
          { id: 'Interaction Drift', name: 'Interaction Drift', desc: 'Bơm 200 đánh giá phân cực (chỉ 1.0 hoặc 5.0) làm rối hệ thống.' },
          { id: 'Context Drift', name: 'Context Drift', desc: 'Bơm 200 tương tác ngẫu nhiên (điểm 1.0 - 3.0) từ nền tảng khác.' },
          { id: 'Structural Drift', name: 'Structural Drift', desc: 'Phá hủy ma trận bằng cách bơm 200 điểm số hoàn toàn ngẫu nhiên.' }
        ].map((drift) => (
          <div key={drift.id} data-figma-id={`SIM-BTN-${drift.id}`} className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col">
            <h3 className="font-semibold text-slate-200 mb-1">{drift.name}</h3>
            <p className="text-xs text-slate-400 mb-4 flex-1">{drift.desc}</p>
            <button 
              onClick={() => handleSimulate(drift.id)}
              disabled={isSimulating}
              className="w-full py-2 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 border border-slate-700 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
            >
              <Zap className="w-4 h-4 text-amber-400" /> Bơm Nhiễu
            </button>
          </div>
        ))}
      </div>

      <div className="flex justify-end mt-2">
        <button 
          onClick={() => handleSimulate('None')}
          className="px-6 py-2 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-400 border border-emerald-500/30 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" /> Khôi phục Trạng thái Gốc (Reset)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        <div data-figma-id="SIM-PROGRESS" className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="font-semibold text-slate-200 mb-6 flex items-center gap-2">
            <Terminal className="w-5 h-5 text-indigo-400" /> Bảng Dữ liệu Đã Bơm
          </h3>
          
          <div className="h-64 bg-slate-950 border border-slate-800 rounded-lg overflow-y-auto">
            {isSimulating ? (
              <div className="flex flex-col items-center justify-center h-full text-indigo-400">
                <RefreshCw className="w-6 h-6 animate-spin mb-2" />
                <span className="text-sm">Đang bơm dữ liệu vào RAM...</span>
              </div>
            ) : logs.length > 0 ? (
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-slate-400 uppercase bg-slate-900 sticky top-0 border-b border-slate-800">
                  <tr>
                    <th className="px-4 py-3">Thời gian</th>
                    <th className="px-4 py-3">User ID</th>
                    <th className="px-4 py-3">Movie ID</th>
                    <th className="px-4 py-3 text-right">Rating</th>
                    <th className="px-4 py-3">Loại</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log, i) => (
                    <tr key={i} className="border-b border-slate-800/50 hover:bg-slate-900/50">
                      <td className="px-4 py-3 text-slate-300 font-mono text-xs">{log.timestamp}</td>
                      <td className="px-4 py-3 text-slate-200 font-medium">#{log.user_id}</td>
                      <td className="px-4 py-3 text-slate-400">#{log.movie_id}</td>
                      <td className="px-4 py-3 text-right">
                        <span className={`px-2 py-1 rounded text-xs font-bold ${log.score >= 4.0 ? 'bg-emerald-500/20 text-emerald-400' : log.score <= 2.0 ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'}`}>
                          {log.score.toFixed(1)} ★
                        </span>
                      </td>
                      <td className="px-4 py-3 text-indigo-400 text-xs">{log.type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="flex items-center justify-center h-full text-slate-600 text-sm">
                Chưa có luồng dữ liệu nào được bơm.
              </div>
            )}
          </div>
        </div>

        <div data-figma-id="SIM-ACTION" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" /> Tác động hệ thống
          </h3>
          <div className="space-y-4 text-sm text-slate-300">
            {simulationResult && simulationResult.type !== 'None' ? (
              <div className="p-3 bg-rose-500/10 rounded border border-rose-500/30 text-rose-300">
                <p className="font-mono text-rose-400 mb-2 font-bold">» SYSTEM ALERT</p>
                200 điểm số rác đã được bơm thẳng vào mảng <code className="bg-rose-500/20 px-1 rounded">recent_scores</code>. <br/><br/>
                Hành động tiếp theo: <br/>
                Hãy qua tab <b>Giám sát Trôi dạt</b> để xem biểu đồ KS-Test sụp đổ ngay lập tức!
              </div>
            ) : simulationResult?.type === 'None' ? (
              <div className="p-3 bg-emerald-500/10 rounded border border-emerald-500/30 text-emerald-300">
                <p className="font-mono text-emerald-400 mb-2 font-bold">» SYSTEM CLEARED</p>
                Đã xóa sạch bộ nhớ tạm. Hệ thống đã trở về trạng thái ổn định.
              </div>
            ) : (
              <p className="text-slate-500 text-center py-8">Bấm Bơm Nhiễu để kiểm thử.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
