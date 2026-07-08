from scipy.stats import ks_2samp

class DriftMonitoringService:
    def __init__(self, rec_service):
        self.rec_service = rec_service
        
    def get_detect_status(self):
        # In a real system, traffic is continuous. For the demo, if we don't have enough recent scores,
        # we auto-generate some traffic to evaluate the current model state.
        if len(self.rec_service.recent_scores) < 20:
            import random
            for _ in range(5):
                self.rec_service.get_recommendations(str(random.randint(1, 10000)), top_k=10)
                
        recent_scores = self.rec_service.recent_scores
        
        # We need at least some recent scores to compare
        if len(recent_scores) < 20:
            return {"is_drift": False, "p_value": 1.0, "drift_score": 0.0}
            
        # Baseline scores: A typical ideal distribution of recommendations (centered around 4.0)
        import numpy as np
        baseline_scores_raw = np.random.normal(loc=4.0, scale=0.5, size=200)
        baseline_scores = [min(5.0, max(1.0, float(s))) for s in baseline_scores_raw]
            
        # Perform Kolmogorov-Smirnov Test for goodness of fit
        # It compares the distribution of recent_scores with baseline_scores
        stat, p_value = ks_2samp(recent_scores, baseline_scores)
        
        # Typically, p-value < 0.05 indicates the distributions are significantly different (Drift!)
        is_drift = bool(p_value < 0.05)
        
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
        # We proxy CTR by the mean predicted score. If the model is predicting lower scores,
        # users are theoretically less likely to click.
        mean_baseline = float(np.mean(baseline_scores)) if baseline_scores else 0
        mean_current = float(np.mean(recent_scores)) if recent_scores else 0
        
        if mean_baseline > 0:
            ctr_fluctuation = ((mean_current - mean_baseline) / mean_baseline) * 100
        else:
            ctr_fluctuation = 0.0
            
        return {
            "is_drift": is_drift,
            "p_value": round(p_value, 4),
            "drift_score": round(stat, 4),
            "ctr_fluctuation": round(ctr_fluctuation, 2),
            "chart_data": chart_data
        }
