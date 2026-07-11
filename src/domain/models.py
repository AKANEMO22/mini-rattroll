from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class Movie(BaseModel):
    movie_id: str
    title: str
    genres: List[str]
    year: Optional[int] = None

class User(BaseModel):
    user_id: str
    demographics: Dict[str, Any] = Field(default_factory=dict)

class Interaction(BaseModel):
    user_id: str
    movie_id: str
    timestamp: datetime
    context: Dict[str, Any] = Field(default_factory=dict)

class Rating(Interaction):
    score: float

class ImplicitFeedback(Interaction):
    action_type: str # "click", "view", "skip"
    dwell_time: Optional[float] = None

class Recommendation(BaseModel):
    req_id: str
    user_id: str
    items: List[str]
    scores: List[float]
    model_version: str

class RecommendationHistory(BaseModel):
    req_id: str
    user_id: str
    latency_ms: float
    timestamp: datetime
    model_version: str
    cluster_id: Optional[int] = None

class DriftEvent(BaseModel):
    metric_name: str
    p_value: float
    drift_score: float
    is_drift: bool
    timestamp: datetime

class RetrainingEvent(BaseModel):
    strategy: str # "retrain_all", "retrain_ranking_only"
    target_component: Optional[str] = None
    timestamp: datetime
