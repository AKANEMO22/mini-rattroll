import os
import pickle
from typing import Dict, Any, Optional

class ModelRegistry:
    """Manages ML Model lifecycle (Single version overwrite)."""
    def __init__(self, base_path: str = "models"):
        self.base_path = base_path
        self.model_path = os.path.join(self.base_path, "svd_model.pkl")
        os.makedirs(self.base_path, exist_ok=True)

    def register(self, version: str, artifacts: Dict[str, Any]) -> None:
        """Saves the model artifacts, overwriting any previous model."""
        with open(self.model_path, 'wb') as f:
            pickle.dump(artifacts, f)

    def activate(self, version: str) -> None:
        """No-op. Since we only keep one model, it is always active."""
        pass

    def get_active_model_path(self) -> Optional[str]:
        """Returns the path to the single model if it exists."""
        if os.path.exists(self.model_path):
            return self.model_path
        return None
