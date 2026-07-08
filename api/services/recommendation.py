import json
import os
import re
import random
from typing import List, Dict, Any
from datetime import datetime
from src.domain.models import RecommendationHistory

class RecommendationCache:
    def __init__(self):
        self.cache = {}
        
    def get(self, key): return self.cache.get(key)
    def set(self, key, val): self.cache[key] = val

class RecommendationService:
    def __init__(self):
        self.cache = RecommendationCache()
        self.history_log: List[RecommendationHistory] = []
        self.recent_scores: List[float] = []
        self.top_movies = []
        self._load_baseline()

    def _load_baseline(self):
        baseline_path = "data/top_movies_baseline.json"
        if os.path.exists(baseline_path):
            with open(baseline_path, 'r', encoding='utf-8') as f:
                self.top_movies = json.load(f)

    def get_recommendations(self, user_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        cache_key = f"{user_id}_{top_k}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
            
        items = []
        if self.top_movies:
            # Read drift state
            from api.services.simulation_service import SimulationService
            sim_svc = SimulationService()
            drift_state = sim_svc.get_state()
            severity = float(drift_state.get("severity", 0.0))
            
            # Simple simulation of personalization: we shuffle the top 100 movies 
            # and pick top_k, but weight them by their actual score so it's a real baseline.
            # A real baseline would just return the exact top K every time,
            # but to give different users different movies, we pick randomly from the top 50.
            random.seed(int(user_id) if user_id.isdigit() else 42)
            
            if severity > 0:
                # Mix in bad movies based on severity
                num_bad = int(top_k * severity)
                num_good = top_k - num_bad
                
                good_pool = self.top_movies[:50]
                bad_pool = self.top_movies[-50:] # Bottom 50 of the top 200 (which are the lowest rated of the >500 count)
                
                selected = random.sample(good_pool, min(num_good, len(good_pool)))
                selected += random.sample(bad_pool, min(num_bad, len(bad_pool)))
                random.shuffle(selected)
            else:
                pool = self.top_movies[:50]
                selected = random.sample(pool, min(top_k, len(pool)))
            
            for m in selected:
                title = m['title']
                # Extract year using regex e.g. "Toy Story (1995)"
                year_match = re.search(r'\((\d{4})\)', title)
                year = year_match.group(1) if year_match else "N/A"
                clean_title = re.sub(r'\(\d{4}\)', '', title).strip()
                
                # Apply a mathematically visible penalty to simulate drift
                penalty = random.uniform(0.5, 2.0) * severity if severity > 0 else 0
                final_score = max(1.0, m['mean_rating'] - penalty)
                
                items.append({
                    "item_id": m['movieId'],
                    "title": clean_title,
                    "year": year,
                    "genres": m['genres'].split('|') if isinstance(m['genres'], str) else [],
                    "score": round(final_score, 2)
                })
        else:
            # Fallback if baseline doesn't exist
            items = []
            
        # Sort by score descending
        items = sorted(items, key=lambda x: x['score'], reverse=True)
        
        # Record scores for drift monitoring
        if items:
            self.recent_scores.extend([item['score'] for item in items])
            # Keep only last 200 items to represent recent distribution
            if len(self.recent_scores) > 200:
                self.recent_scores = self.recent_scores[-200:]
        
        self.cache.set(cache_key, items)
        
        # Log History matching Domain Model
        history_record = RecommendationHistory(
            req_id=f"req_{datetime.now().timestamp()}",
            user_id=user_id,
            latency_ms=15.4,
            timestamp=datetime.now(),
            model_version="v2.1"
        )
        self.history_log.append(history_record)
        
        return items
