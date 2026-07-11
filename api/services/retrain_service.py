import subprocess
import json
import os
import threading

class RetrainService:
    def __init__(self, rec_service):
        self.rec_service = rec_service
        self.status_file = "data/retrain_status.json"
        
    def start_retraining(self):
        # Reset the status file
        os.makedirs("data", exist_ok=True)
        with open(self.status_file, "w") as f:
            json.dump({"status": "starting", "progress": 0, "message": "Starting background process..."}, f)
            
        # Run in a background thread to avoid blocking API
        thread = threading.Thread(target=self._run_pipeline)
        thread.daemon = True
        thread.start()
        
        return {"status": "success", "message": "Retraining triggered"}
        
    def _run_pipeline(self):
        try:
            # Call the train_pipeline.py as a separate process
            # We use subprocess so it uses a fresh memory space and doesn't crash the server
            result = subprocess.run(["python", "train_pipeline.py"], capture_output=True, text=True)
            if result.returncode == 0:
                # Reload model into RecommendationService
                self.rec_service._load_model()
                # Clear recent scores so Drift turns green again
                self.rec_service.recent_scores.clear()
                # Clear cache so new recommendations use the newly trained model
                self.rec_service.cache.cache.clear()
            else:
                with open(self.status_file, "w") as f:
                    json.dump({"status": "error", "progress": 0, "message": f"Error: {result.stderr}"}, f)
        except Exception as e:
            with open(self.status_file, "w") as f:
                json.dump({"status": "error", "progress": 0, "message": f"Exception: {str(e)}"}, f)

    def get_status(self):
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return {"status": "idle", "progress": 0, "message": "No training in progress"}
