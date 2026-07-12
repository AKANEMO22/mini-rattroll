import pickle
from src.recommender.registry import ModelRegistry
import os

def find_clusters():
    registry = ModelRegistry("models")
    model_path = registry.get_active_model_path()
    if not model_path:
        model_path = "models/svd_model.pkl"

    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            data = pickle.load(f)
            model = data.get('model')
            cluster_model = data.get('cluster_model')
            
            if not model or not cluster_model:
                print("Model or cluster model not found.")
                return

            cluster_users = {}
            # We just need to check a few users
            for uid, user_idx in list(model.user_to_index.items())[:50000]: # Check first 50k users
                user_factor = model.user_factors[user_idx]
                cluster_id = cluster_model.assign(user_factor)
                if cluster_id not in cluster_users:
                    cluster_users[cluster_id] = []
                if len(cluster_users[cluster_id]) < 5:
                    cluster_users[cluster_id].append(uid)
                
                # if we have 5 users for at least 3 clusters, break
                if len(cluster_users) >= 3 and all(len(v) >= 5 for v in cluster_users.values()):
                    break

            for cid, users in cluster_users.items():
                print(f"Cluster {cid}: {users}")
    else:
        print("Model file not found")

if __name__ == "__main__":
    find_clusters()
