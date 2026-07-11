import json
import os
import random
import time
from datetime import datetime
from src.evaluation.recommendation import RecEvaluator

class EvaluationService:
    def __init__(self, rec_service):
        self.rec_service = rec_service
        self.history_file = "data/metrics_history.json"
        self.evaluator = RecEvaluator()
        
    def evaluate(self):
        # 1. Check if model is available, else return zeros
        if not self.rec_service.model or not hasattr(self.rec_service.model, 'user_to_index'):
            metrics = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "ndcg": 0.0, "precision": 0.0, "recall": 0.0, "map": 0.0, "rmse": 0.0, "latency": 0.0
            }
            return metrics

        # 2. Sample 20 REAL users from the model
        start_time = time.time()
        
        all_users = list(self.rec_service.model.user_to_index.keys())
        if len(all_users) >= 20:
            users = random.sample(all_users, 20)
        else:
            users = all_users

        all_user_scores = []
        for u in users:
            items, _ = self.rec_service.get_recommendations(str(u), top_k=10)
            if not items:
                continue
            scores = [item.get("score", 0) for item in items]
            all_user_scores.append(scores)
            
        # 3. Call standard pipeline evaluator
        metrics = self.evaluator.evaluate_online_proxy(all_user_scores)
        
        latency = (time.time() - start_time) * 1000 # in ms
        metrics["timestamp"] = datetime.now().strftime("%H:%M:%S")
        metrics["latency"] = round(latency, 2)
        
        self.save_metrics(metrics)
        return metrics
        
    def save_metrics(self, metrics):
        history = self.get_history()
        history.append(metrics)
        # Keep only last 20
        history = history[-20:]
        with open(self.history_file, 'w') as f:
            json.dump(history, f)
            
    def get_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
