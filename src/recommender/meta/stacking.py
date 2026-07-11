from typing import Any, List
from sklearn.linear_model import LogisticRegression
import numpy as np

class StackingMetaLearner:
    """Combines predictions from MF and Cluster-LR models."""
    def __init__(self):
        self.blender = LogisticRegression(random_state=42)
        self.is_fitted = False

    def fit(self, mf_scores: List[float], lr_scores: List[float], labels: List[int]) -> None:
        X = np.column_stack((mf_scores, lr_scores))
        y = np.array(labels)
        
        if len(np.unique(y)) > 1:
            self.blender.fit(X, y)
            self.is_fitted = True

    def blend_scores(self, mf_score: float, lr_score: float) -> float:
        if not self.is_fitted:
            # Fallback to simple average if not trained properly
            return (mf_score + lr_score) / 2.0
            
        try:
            X = np.array([[mf_score, lr_score]])
            proba = self.blender.predict_proba(X)[0]
            if 1 in self.blender.classes_:
                idx = np.where(self.blender.classes_ == 1)[0][0]
                return float(proba[idx])
            return 0.0
        except Exception:
            return (mf_score + lr_score) / 2.0
