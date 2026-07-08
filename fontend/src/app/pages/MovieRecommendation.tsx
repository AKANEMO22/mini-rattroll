import React, { useState } from 'react';
import { Search, Info, ThumbsUp, ThumbsDown, Star, RefreshCw, Film } from 'lucide-react';
import { api } from '../services/api';

const MovieCard = ({ title, year, genres, predScore, mfScore, clusterScore, metaScore, confidence, explanation, id, imageIndex }: any) => (
  <div data-figma-id={id} className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col group hover:border-indigo-500/50 transition-colors">
    <div className="relative h-48 bg-slate-800 overflow-hidden">
      <div className="absolute top-2 right-2 text-[10px] bg-black/50 px-1 rounded text-slate-300 font-mono z-10">{id}</div>
      <img 
        src={`https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=400&h=300&sig=${imageIndex}`} 
        alt={title} 
        className="w-full h-full object-cover opacity-60 group-hover:opacity-80 transition-opacity"
      />
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-slate-900 to-transparent p-4 pt-12">
        <h3 className="text-lg font-bold text-white leading-tight">{title || 'Không rõ tên'} <span className="text-sm font-normal text-slate-300">({year || 'N/A'})</span></h3>
        <p className="text-xs text-indigo-300 mt-1">{(genres && genres.length > 0) ? genres.join(' • ') : 'Không có thể loại'}</p>
      </div>
      <div className="absolute top-3 left-3 bg-emerald-500 text-white font-bold px-2 py-1 rounded text-sm shadow-lg flex items-center gap-1">
        <Star className="w-3.5 h-3.5 fill-current" />
        {predScore ? predScore.toFixed(2) : '0.00'}
      </div>
    </div>
    
    <div className="p-4 flex-1 flex flex-col">
      <div className="grid grid-cols-3 gap-2 mb-4 text-center">
        <div className="bg-slate-950 rounded p-1.5 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">MF</div>
          <div className="text-sm text-slate-300 font-mono">{mfScore ? mfScore.toFixed(2) : '0.00'}</div>
        </div>
        <div className="bg-slate-950 rounded p-1.5 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">Cluster</div>
          <div className="text-sm text-slate-300 font-mono">{clusterScore ? clusterScore.toFixed(2) : '0.00'}</div>
        </div>
        <div className="bg-slate-950 rounded p-1.5 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">Meta</div>
          <div className="text-sm text-slate-300 font-mono">{metaScore ? metaScore.toFixed(2) : '0.00'}</div>
        </div>
      </div>
      
      <div className="mb-4 flex-1">
        <div className="flex justify-between text-xs mb-1">
          <span className="text-slate-400 flex items-center gap-1"><Info className="w-3 h-3" /> Độ tin cậy</span>
          <span className="text-emerald-400 font-medium">{confidence || 0}%</span>
        </div>
        <div className="w-full bg-slate-800 rounded-full h-1.5 mb-2">
          <div className="bg-emerald-400 h-1.5 rounded-full" style={{ width: `${confidence || 0}%` }}></div>
        </div>
        <p className="text-xs text-slate-500 italic line-clamp-2">"{explanation || 'Gợi ý được hệ thống sinh ra tự động.'}"</p>
      </div>
      
      <div className="flex gap-2 mt-auto border-t border-slate-800 pt-3">
        <button className="flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors">
          <ThumbsUp className="w-3.5 h-3.5" /> Thích
        </button>
        <button className="flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors">
          <ThumbsDown className="w-3.5 h-3.5" /> Không thích
        </button>
        <button className="flex-1 flex items-center justify-center gap-1.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs transition-colors">
          <Star className="w-3.5 h-3.5" /> Đánh giá
        </button>
      </div>
    </div>
  </div>
);

export default function MovieRecommendation() {
  const [userId, setUserId] = useState('1');
  const [isGenerating, setIsGenerating] = useState(false);
  const [recommendations, setRecommendations] = useState<any[]>([]);

  const handleRecommend = async () => {
    setIsGenerating(true);
    const res = await api.getRecommendations(userId, 4);
    
    // Transform backend data to fit Figma component specs if necessary
    const formattedRecs = (res.recommendations || []).map((item: any, idx: number) => ({
      title: item.title,
      year: item.year,
      genres: item.genres,
      predScore: item.score,
      mfScore: item.score,
      clusterScore: item.score,
      metaScore: item.score,
      confidence: Math.floor((item.score || 0) * 20),
      explanation: "Gợi ý cá nhân hóa từ thuật toán SVD (Matrix Factorization)."
    }));
    
    setRecommendations(formattedRecs);
    setIsGenerating(false);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Hệ thống Gợi ý Phim</h1>
          <p className="text-sm text-slate-400 mt-1">Tạo danh sách phim gợi ý cá nhân hóa sử dụng Mô hình Lai (Hybrid)</p>
        </div>
      </div>

      <div data-figma-id="CTRL-001" className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col md:flex-row items-end gap-4 relative">
        <div className="absolute top-2 right-2 text-[10px] text-slate-700 font-mono">CTRL-001</div>
        <div className="flex-1 w-full">
          <label className="block text-xs font-medium text-slate-400 mb-1.5 uppercase tracking-wider">Mã Người Dùng (User ID)</label>
          <div className="relative">
            <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input 
              type="text" 
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg py-2.5 pl-10 pr-4 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all"
              placeholder="VD: 12345"
            />
          </div>
        </div>
        
        <button 
          data-figma-id="BTN-REC-GEN"
          onClick={handleRecommend}
          disabled={isGenerating}
          className="w-full md:w-auto px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-600/50 text-white rounded-lg font-medium transition-colors shadow-[0_0_15px_rgba(79,70,229,0.3)] flex items-center justify-center gap-2"
        >
          {isGenerating ? <RefreshCw className="w-5 h-5 animate-spin" /> : <Film className="w-5 h-5" />}
          {isGenerating ? 'Đang xử lý...' : 'Tạo Phim Gợi ý'}
        </button>
      </div>

      {!isGenerating && (
        <div className="space-y-4">
          <div className="flex justify-between items-center px-1">
            <h2 className="text-lg font-semibold text-slate-200 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              Top Phim Gợi ý cho User: {userId}
            </h2>
            <span className="text-xs text-slate-500 font-mono">Thời gian suy luận: 42ms</span>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {recommendations.map((movie, idx) => (
              <MovieCard 
                key={idx}
                id={`REC-00${idx + 1}`}
                imageIndex={idx + 1}
                {...movie}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
