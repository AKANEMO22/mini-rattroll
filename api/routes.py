from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from api.services.recommendation import RecommendationService
from api.services.simulation_service import SimulationService
from api.services.evaluation_service import EvaluationService
from api.services.drift_monitoring_service import DriftMonitoringService

from api.services.retrain_service import RetrainService

router = APIRouter()
rec_service = RecommendationService()
sim_service = SimulationService(rec_service)
eval_service = EvaluationService(rec_service)
drift_service = DriftMonitoringService(rec_service)
retrain_service = RetrainService(rec_service)

class RecRequest(BaseModel):
    user_id: str
    top_k: int = 10

@router.post("/recommend")
def recommend(request: RecRequest):
    items, cluster_id = rec_service.get_recommendations(request.user_id, request.top_k)
    return {"user_id": request.user_id, "cluster_id": cluster_id, "recommendations": items}

@router.get("/status")
def get_status():
    retrain_state = retrain_service.get_status()
    if retrain_state.get("status") in ["starting", "running"]:
        return {"status": "OK", "state": "Retraining"}
    return {"status": "OK", "state": "Monitoring"}

@router.get("/detect_status")
def get_detect_status():
    return drift_service.get_detect_status()

@router.get("/models")
def get_models():
    return {
        "active_version": "v2.1",
        "versions": [
            {"version": "v2.1", "status": "Active", "metrics": {"ndcg": 0.85}},
            {"version": "v2.0", "status": "Archived", "metrics": {"ndcg": 0.82}}
        ]
    }

class RollbackRequest(BaseModel):
    version: str

@router.post("/models/rollback")
def rollback_model(request: RollbackRequest):
    return {"status": "success", "message": f"Rolled back to {request.version}"}

@router.post("/simulate")
def simulate_drift(payload: Dict[str, Any]):
    # Clear recommendation cache so the new state takes effect immediately
    rec_service.cache.cache.clear()
    return sim_service.inject_drift(payload.get("type", "Unknown"), payload.get("severity", 0.0))

@router.get("/simulate/logs")
def get_simulation_logs():
    return sim_service.get_logs()

@router.get("/metrics")
def get_metrics():
    return eval_service.evaluate()

@router.post("/retrain/start")
def start_retraining():
    return retrain_service.start_retraining()

@router.get("/retrain/status")
def get_retrain_status():
    return retrain_service.get_status()

import json
import os

@router.get("/metrics/history")
def get_metrics_history():
    return eval_service.get_history()

from api.services.dataset_service import DatasetService
data_service = DatasetService()

@router.get("/dataset/info")
def get_dataset_info():
    return data_service.get_dataset_info()

@router.get("/movies/search")
def search_movies(q: str = ""):
    return data_service.search_movies(q)

@router.get("/users/{user_id}")
def get_user_profile(user_id: int):
    profile = data_service.get_user_profile(user_id)
    try:
        if rec_service.model and user_id in rec_service.model.user_to_index:
            user_idx = rec_service.model.user_to_index[user_id]
            user_factor = rec_service.model.user_factors[user_idx]
            if rec_service.cluster_model:
                cluster_id = rec_service.cluster_model.assign(user_factor)
                profile["cluster_id"] = int(cluster_id)
            else:
                profile["cluster_id"] = None
        else:
            profile["cluster_id"] = None
    except Exception:
        profile["cluster_id"] = None
    return profile

@router.get("/history")
def get_global_history():
    return data_service.get_global_history()
