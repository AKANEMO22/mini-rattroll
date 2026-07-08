import React, { useState } from 'react';
import { PlayCircle, Zap, AlertTriangle, CheckCircle, RefreshCw } from 'lucide-react';
import { api } from '../services/api';

export default function Simulation() {
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState<any>(null);

  const handleSimulate = async (type: string) => {
    setIsSimulating(true);
    setSimulationResult(null);
    const severity = type === 'None' ? 0.0 : 0.8;
    const res = await api.simulateDrift(type, severity);
    setSimulationResult({ type, ...res });
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
          { id: 'preference', name: 'Preference Drift', desc: 'Người dùng thay đổi sở thích đột ngột' },
          { id: 'interaction', name: 'Interaction Drift', desc: 'Lượng tương tác giảm mạnh' },
          { id: 'context', name: 'Context Drift', desc: 'Thay đổi hành vi theo thời gian/thiết bị' },
          { id: 'structural', name: 'Structural Drift', desc: 'Cấu trúc ma trận thay đổi' }
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
            <PlayCircle className="w-5 h-5 text-indigo-400" /> Quá trình Mô phỏng
          </h3>
          
          {isSimulating ? (
            <div className="h-48 flex flex-col items-center justify-center text-slate-400">
              <RefreshCw className="w-8 h-8 animate-spin mb-4 text-indigo-500" />
              <p>Đang tiến hành bơm nhiễu và chạy chẩn đoán...</p>
            </div>
          ) : simulationResult ? (
            <div className="space-y-4">
              <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-lg flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-emerald-400 mt-0.5" />
                <div>
                  <h4 className="font-medium text-emerald-400">Hoàn thành Mô phỏng</h4>
                  <p className="text-sm text-slate-300 mt-1">Đã tiêm nhiễu "{simulationResult.type}". {simulationResult.message}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-500 uppercase">Độ trễ phát hiện (Delay)</p>
                  <p className="text-lg font-bold text-slate-200 mt-1">2.4s</p>
                </div>
                <div className="bg-slate-950 p-4 rounded-lg border border-slate-800">
                  <p className="text-xs text-slate-500 uppercase">Độ chính xác (Diagnosis Accuracy)</p>
                  <p className="text-lg font-bold text-slate-200 mt-1">100%</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-48 flex flex-col items-center justify-center text-slate-500 border border-dashed border-slate-700 rounded-lg bg-slate-950/50">
              <p className="text-sm">Chưa có phiên mô phỏng nào được chạy.</p>
              <p className="text-xs mt-1">Vui lòng chọn một loại Drift ở trên.</p>
            </div>
          )}
        </div>

        <div data-figma-id="SIM-ACTION" className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="font-semibold text-slate-200 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" /> Quyết định Huấn luyện
          </h3>
          <div className="space-y-4 text-sm text-slate-300">
            {simulationResult ? (
              <div className="p-3 bg-slate-800 rounded border border-slate-700">
                <p className="font-mono text-emerald-400 mb-2">» EXPECTED ACTION</p>
                Hệ thống xác nhận cần chạy lại Component <b>Cluster Logistic</b> dựa trên nhiễu được tiêm.
              </div>
            ) : (
              <p className="text-slate-500 text-center py-8">Chưa có kết quả.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
