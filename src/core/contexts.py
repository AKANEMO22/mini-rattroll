from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PipelineContext:
    """Manages state for offline/retraining pipelines."""
    raw_data: Optional[Any] = None
    processed_data: Optional[Any] = None
    features: Dict[str, Any] = field(default_factory=dict)
    embeddings: Dict[str, Any] = field(default_factory=dict)
    clusters: Optional[Any] = None
    models: Dict[str, Any] = field(default_factory=dict)
    baselines: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)
    configuration: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RecommendationContext:
    """Manages state for a single online recommendation request."""
    user_id: str
    request_timestamp: datetime = field(default_factory=datetime.utcnow)
    user_features: Optional[Any] = None
    assigned_cluster: Optional[int] = None
    candidate_items: List[Any] = field(default_factory=list)
    mf_scores: Dict[str, float] = field(default_factory=dict)
    lr_scores: Dict[str, float] = field(default_factory=dict)
    final_ranking: List[Any] = field(default_factory=list)
    ab_test_group: str = "A"
