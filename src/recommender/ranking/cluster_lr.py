from typing import Any, Dict
from src.interfaces.base import BaseRanker
from sklearn.linear_model import LogisticRegression
import numpy as np

class ClusterLRModel(BaseRanker):
    """Logistic Regression trained specifically for a given user cluster."""
    def __init__(self):
        self.models: Dict[int, LogisticRegression] = {}
        # default model if cluster is missing or un-trainable
        self.default_model = LogisticRegression(random_state=42)
        self.is_fitted = False

    def fit(self, data: Dict[int, Dict[str, Any]]) -> None:
        """
        data is a dict mapping cluster_id to a dict of {'X': np.array, 'y': np.array}
        """
        all_X = []
        all_y = []
        
        for cluster_id, cluster_data in data.items():
            X = cluster_data['X']
            y = cluster_data['y']
            
            if len(X) == 0:
                continue
                
            model = LogisticRegression(random_state=42)
            if len(np.unique(y)) > 1:
                model.fit(X, y)
                self.models[cluster_id] = model
                
            all_X.append(X)
            all_y.append(y)
            
        if all_X:
            X_concat = np.vstack(all_X)
            y_concat = np.hstack(all_y)
            if len(np.unique(y_concat)) > 1:
                self.default_model.fit(X_concat, y_concat)
                self.is_fitted = True

    def predict(self, cluster_id: int, item_factor: Any) -> float:
        if not self.is_fitted:
            return 0.5
            
        model = self.models.get(cluster_id)
        if model is None:
            model = self.default_model
            
        try:
            proba = model.predict_proba([item_factor])[0]
            if 1 in model.classes_:
                idx = np.where(model.classes_ == 1)[0][0]
                return float(proba[idx])
            return 0.0
        except Exception:
            return 0.5
