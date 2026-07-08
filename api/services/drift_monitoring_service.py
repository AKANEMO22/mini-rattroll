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
            
        # Baseline scores: The top 50 movies which our model normally picks from
        # Note: top_movies is sorted by mean_rating
        baseline_pool = self.rec_service.top_movies[:50]
        baseline_scores = [m['mean_rating'] for m in baseline_pool]
        
        if not baseline_scores:
            return {"is_drift": False, "p_value": 1.0, "drift_score": 0.0}
            
        # Perform Kolmogorov-Smirnov Test for goodness of fit
        # It compares the distribution of recent_scores with baseline_scores
        stat, p_value = ks_2samp(recent_scores, baseline_scores)
        
        # Typically, p-value < 0.05 indicates the distributions are significantly different (Drift!)
        is_drift = bool(p_value < 0.05)
        
        return {
            "is_drift": is_drift,
            "p_value": round(p_value, 4),
            "drift_score": round(stat, 4)
        }
