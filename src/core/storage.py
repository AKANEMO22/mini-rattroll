import os
import json
from typing import Any, Dict

class BaseStorage:
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

class DataStorage(BaseStorage):
    pass

class ModelStorage(BaseStorage):
    pass

class BaselineStorage(BaseStorage):
    def save_baseline(self, name: str, data: Dict[str, Any]):
        with open(os.path.join(self.base_path, f"{name}.json"), 'w') as f:
            json.dump(data, f)
            
    def load_baseline(self, name: str) -> Dict[str, Any]:
        with open(os.path.join(self.base_path, f"{name}.json"), 'r') as f:
            return json.load(f)

class LogStorage(BaseStorage):
    pass

class ArtifactManager:
    """Manages non-model artifacts like PCA weights, Scalers."""
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        
    def save_artifact(self, name: str, obj: Any):
        pass # To be implemented with pickle/joblib
        
    def load_artifact(self, name: str) -> Any:
        pass # To be implemented
