const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = {
  getSystemStatus: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/status`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { status: "Error", state: "Disconnected" };
    }
  },
  
  getMetrics: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/metrics`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { ndcg: 0, precision: 0, recall: 0 };
    }
  },

  getMetricsHistory: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/metrics/history`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getDetectStatus: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/detect_status`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { is_drift: false, p_value: 1.0, drift_score: 0.0 };
    }
  },

  getRecommendations: async (userId: string, topK: number = 10) => {
    try {
      const res = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, top_k: topK })
      });
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { user_id: userId, recommendations: [] };
    }
  },
  
  simulateDrift: async (type: string, severity: number) => {
    try {
      const res = await fetch(`${API_BASE_URL}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, severity })
      });
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { status: "error", message: "Failed to connect" };
    }
  },
  
  getModels: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/models`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { active_version: "Unknown", versions: [] };
    }
  },
  
  rollbackModel: async (version: string) => {
    try {
      const res = await fetch(`${API_BASE_URL}/models/rollback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ version })
      });
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return { status: "error", message: "Failed to rollback" };
    }
  },

  getDatasetInfo: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/dataset/info`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  },

  searchMovies: async (query: string) => {
    try {
      const res = await fetch(`${API_BASE_URL}/movies/search?q=${encodeURIComponent(query)}`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  getUserProfile: async (userId: number) => {
    try {
      const res = await fetch(`${API_BASE_URL}/users/${userId}`);
      if (!res.ok) throw new Error('Network response was not ok');
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  },

};
