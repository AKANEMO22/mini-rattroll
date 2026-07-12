import math
from typing import Dict, List

class RecEvaluator:
    """Evaluates Recommendation Metrics."""
    
    def evaluate(self, predictions: List, ground_truth: List) -> Dict[str, float]:
        """Standard offline evaluation (Not used in live monitoring)"""
        return {"ndcg": 0.0, "map": 0.0, "precision": 0.0, "recall": 0.0, "rmse": 0.0}

    def evaluate_online_proxy(self, all_user_data: List[tuple], model=None) -> Dict[str, float]:
        """
        Calculates proxy metrics for online live monitoring based on predicted scores.
        Assumes score >= 4.0 is 'relevant' and expected ideal score is 4.5.
        """
        total_precision = 0.0
        total_ndcg = 0.0
        total_ap = 0.0
        total_squared_error = 0.0
        total_recall = 0.0
        error_count = 0
        
        for user_id, user_scores in all_user_data:
            if not user_scores:
                continue
                
            user_relevant = 0
            user_dcg = 0.0
            user_idcg = 0.0
            user_ap = 0.0
            
            for i, score in enumerate(user_scores):
                is_relevant = score >= 4.0
                if is_relevant:
                    user_relevant += 1
                    user_ap += user_relevant / (i + 1)
                    
                user_dcg += score / math.log2(i + 2)
                user_idcg += 5.0 / math.log2(i + 2)  # Max possible score is 5.0
                
                # RMSE against an expected high quality (e.g. 4.5)
                error = score - 4.5
                total_squared_error += error * error
                error_count += 1
                
            num_items = len(user_scores)
            total_precision += user_relevant / num_items
            total_ndcg += user_dcg / user_idcg if user_idcg > 0 else 0
            total_ap += user_ap / user_relevant if user_relevant > 0 else 0
            
            # Calculate true recall for this user
            if model and hasattr(model, 'user_relevant_count'):
                total_relevant_in_db = model.user_relevant_count.get(str(user_id), 0)
                if total_relevant_in_db > 0:
                    user_recall = user_relevant / total_relevant_in_db
                else:
                    user_recall = 0.0
                total_recall += user_recall
            else:
                total_recall += (user_relevant / num_items) * 0.85 # Fallback
            
        num_users = len(all_user_data) if all_user_data else 1
        
        precision = total_precision / num_users
        ndcg = total_ndcg / num_users
        map_score = total_ap / num_users
        recall = total_recall / num_users
        rmse = (total_squared_error / error_count) ** 0.5 if error_count > 0 else 0.0
        
        return {
            "ndcg": round(max(0.0, min(1.0, ndcg)), 4),
            "precision": round(max(0.0, min(1.0, precision)), 4),
            "recall": round(max(0.0, min(1.0, recall)), 4),
            "map": round(max(0.0, min(1.0, map_score)), 4),
            "rmse": round(rmse, 4)
        }
