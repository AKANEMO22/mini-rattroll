import os
import json
import pickle
from typing import Dict, Any, Optional
from datetime import datetime

class ModelRegistry:
    """Manages ML Model lifecycle (Versioning, Activation, Rollback)."""
    def __init__(self, base_path: str = "models"):
        self.base_path = base_path
        self.manifest_path = os.path.join(self.base_path, "manifest.json")
        self._init_manifest()

    def _init_manifest(self):
        if not os.path.exists(self.manifest_path):
            os.makedirs(self.base_path, exist_ok=True)
            with open(self.manifest_path, 'w') as f:
                json.dump({"active_version": None, "versions": []}, f)

    def _load_manifest(self) -> dict:
        with open(self.manifest_path, 'r') as f:
            return json.load(f)

    def _save_manifest(self, manifest: dict):
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)

    def register(self, version: str, artifacts: Dict[str, Any]) -> None:
        manifest = self._load_manifest()
        
        # Save artifacts to versioned folder
        version_dir = os.path.join(self.base_path, version)
        os.makedirs(version_dir, exist_ok=True)
        
        model_path = os.path.join(version_dir, "svd_model.pkl")
        with open(model_path, 'wb') as f:
            pickle.dump(artifacts, f)
            
        # Update manifest
        version_entry = {
            "version": version,
            "created_at": datetime.now().isoformat(),
            "status": "Archived"
        }
        
        # Remove old entry if same version
        manifest["versions"] = [v for v in manifest["versions"] if v["version"] != version]
        manifest["versions"].append(version_entry)
        
        self._save_manifest(manifest)

    def activate(self, version: str) -> None:
        manifest = self._load_manifest()
        # Mark all as Archived
        for v in manifest["versions"]:
            v["status"] = "Archived"
            
        # Mark target as Active
        for v in manifest["versions"]:
            if v["version"] == version:
                v["status"] = "Active"
                manifest["active_version"] = version
                break
                
        self._save_manifest(manifest)

    def get_active_model_path(self) -> Optional[str]:
        manifest = self._load_manifest()
        active = manifest.get("active_version")
        if active:
            return os.path.join(self.base_path, active, "svd_model.pkl")
        return None
