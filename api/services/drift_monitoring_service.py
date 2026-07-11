import numpy as np
import random
from src.adaptation.monitor.baseline_manager import BaselineManager
from src.adaptation.detector.drift_detector import StatisticalDriftDetector

class DriftMonitoringService:
    def __init__(self, rec_service):
        self.rec_service = rec_service
        self.baseline_manager = BaselineManager()
        self.drift_detector = StatisticalDriftDetector()
        
    def get_detect_status(self):
        if getattr(self.rec_service, 'recent_events', None) is not None:
            recent_events = self.rec_service.recent_events
        else:
            # Fallback for old attribute
            recent_events = [{"cluster_id": 0, "score": s} for s in getattr(self.rec_service, 'recent_scores', [])]
            
        recent_scores = [e['score'] for e in recent_events]
        
        # We need at least some recent scores to compare
        if len(recent_scores) < 20:
            return {"is_drift": False, "p_value": 1.0, "drift_score": 0.0, "ctr_fluctuation": 0.0, "chart_data": [], "heatmap_data": []}
            
        # Get baseline scores from standard pipeline module
        baseline_scores = self.baseline_manager.get_expected_distribution(size=max(200, len(recent_scores)))
            
        # Perform Drift Detection using standard pipeline module
        detect_result = self.drift_detector.detect(recent_scores, baseline_scores)
        
        is_drift = detect_result["is_drift"]
        p_value = detect_result["p_value"]
        stat = detect_result["drift_score"]
        
        # ---------------------------------------------------------
        # CALCULATE REAL DISTRIBUTION (For the Chart)
        # ---------------------------------------------------------
        import numpy as np
        bins = np.arange(1.0, 5.5, 0.5) # [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        
        baseline_hist, _ = np.histogram(baseline_scores, bins=bins)
        current_hist, _ = np.histogram(recent_scores, bins=bins)
        
        # Convert to percentages
        baseline_pct = (baseline_hist / len(baseline_scores) * 100) if len(baseline_scores) > 0 else np.zeros_like(baseline_hist)
        current_pct = (current_hist / len(recent_scores) * 100) if len(recent_scores) > 0 else np.zeros_like(current_hist)
        
        chart_data = []
        for i in range(len(bins) - 1):
            rating_label = f"{bins[i]:.1f}"
            chart_data.append({
                "rating": rating_label,
                "baseline": round(float(baseline_pct[i]), 1),
                "current": round(float(current_pct[i]), 1)
            })
            
        # ---------------------------------------------------------
        # CALCULATE REAL CTR FLUCTUATION
        # ---------------------------------------------------------
        mean_baseline = float(np.mean(baseline_scores)) if baseline_scores else 0
        mean_current = float(np.mean(recent_scores)) if recent_scores else 0
        
        if mean_baseline > 0:
            ctr_fluctuation = ((mean_current - mean_baseline) / mean_baseline) * 100
        else:
            ctr_fluctuation = 0.0
            
        # ---------------------------------------------------------
        # CALCULATE HEATMAP DATA (Cluster vs Rating Drift)
        # ---------------------------------------------------------
        heatmap_data = []
        for cluster_id in range(10):
            c_scores = [e['score'] for e in recent_events if e.get('cluster_id', 0) == cluster_id]
            if not c_scores:
                # If no traffic for this cluster yet, it's not drifting, it's just empty.
                # So the delta should be 0.
                c_delta = np.zeros_like(baseline_pct)
            else:
                c_hist, _ = np.histogram(c_scores, bins=bins)
                c_pct = (c_hist / len(c_scores)) * 100
                c_delta = c_pct - baseline_pct
            
            row = {"cluster": f"Cluster {cluster_id}"}
            for i in range(len(bins) - 1):
                rating_label = f"{bins[i]:.1f}"
                row[rating_label] = round(float(c_delta[i]), 1)
            heatmap_data.append(row)
            
        return {
            "is_drift": is_drift,
            "p_value": round(p_value, 4),
            "drift_score": round(stat, 4),
            "ctr_fluctuation": round(ctr_fluctuation, 2),
            "chart_data": chart_data,
            "heatmap_data": heatmap_data
        }
