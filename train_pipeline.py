import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import pickle
import os

from src.core.contexts import PipelineContext
from src.pipeline.core import Pipeline
from src.pipeline.steps import TrainMFStep
from src.recommender.matrix_factorization.svd_model import SVDModel

def run_training_pipeline():
    import json
    
    def update_status(status_str, progress, message):
        print(message)
        status_data = {
            "status": status_str,
            "progress": progress,
            "message": message
        }
        os.makedirs('data', exist_ok=True)
        with open('data/retrain_status.json', 'w') as f:
            json.dump(status_data, f)
            
    update_status("running", 5, "Initializing Pipeline...")
    pipeline = Pipeline()
    
    # We create a step with our SVDModel
    mf_model = SVDModel(n_factors=50)
    pipeline.add_step(TrainMFStep(mf_model))
    
    update_status("running", 10, "Loading ML-25M movies metadata...")
    movies_df = pd.read_csv('data/ml-25m/movies.csv')
    
    update_status("running", 15, "Loading ML-25M ratings (25 million rows)...")
    
    # Read in chunks to update UI progress dynamically
    chunk_size = 5000000
    chunks = []
    total_rows = 25000095  # Approximate total rows
    processed_rows = 0
    
    import time
    for chunk in pd.read_csv('data/ml-25m/ratings.csv', usecols=['userId', 'movieId', 'rating'], chunksize=chunk_size):
        chunks.append(chunk)
        processed_rows += len(chunk)
        progress = 15 + int((processed_rows / total_rows) * 15) # Scales from 15% to 30%
        update_status("running", min(30, progress), f"Loading ratings dataset: {processed_rows:,} rows read...")
        
    ratings_df = pd.concat(chunks, ignore_index=True)
    
    update_status("running", 32, f"Mapping {len(ratings_df):,} ratings to internal IDs...")
    users = ratings_df['userId'].unique()
    items = ratings_df['movieId'].unique()
    
    user_to_index = {uid: idx for idx, uid in enumerate(users)}
    item_to_index = {iid: idx for idx, iid in enumerate(items)}
    
    update_status("running", 36, "Extracting array vectors for Sparse Matrix...")
    row = ratings_df['userId'].map(user_to_index).values
    col = ratings_df['movieId'].map(item_to_index).values
    data = ratings_df['rating'].values
    
    update_status("running", 42, f"Constructing {len(users):,} x {len(items):,} Sparse Matrix...")
    sparse_matrix = csr_matrix((data, (row, col)), shape=(len(users), len(items)))
    
    context = PipelineContext()
    context.processed_data = {
        'sparse_matrix': sparse_matrix,
        'user_to_index': user_to_index,
        'item_to_index': item_to_index
    }
    
    update_status("running", 50, "Running Phase 1: Matrix Factorization (SVD) Training...")
    pipeline.run(context)
    
    update_status("running", 60, "Running Phase 2: KMeans Clustering on User Embeddings...")
    from src.recommender.clustering.kmeans_clusterer import KMeansClusterer
    kmeans_model = KMeansClusterer(n_clusters=10)
    kmeans_model.fit(mf_model.user_factors)
    
    update_status("running", 65, "Sampling data for Multi-stage Models (50,000 interactions)...")
    from src.recommender.ranking.cluster_lr import ClusterLRModel
    from src.recommender.meta.stacking import StackingMetaLearner
    from src.recommender.registry import ModelRegistry
    import datetime

    # Sample data for fast training (50,000 interactions)
    sampled_df = ratings_df.sample(n=min(50000, len(ratings_df)), random_state=42)
    
    cluster_data = {}
    mf_scores = []
    lr_scores = []
    labels = []
    
    update_status("running", 70, "Pre-computing cluster assignments and features...")
    # Pre-compute cluster assignments for sampled users to group data
    for _, row in sampled_df.iterrows():
        uid = row['userId']
        iid = row['movieId']
        rating = row['rating']
        
        if uid in user_to_index and iid in item_to_index:
            u_idx = user_to_index[uid]
            i_idx = item_to_index[iid]
            
            u_factor = mf_model.user_factors[u_idx]
            i_factor = mf_model.item_factors[i_idx]
            
            cluster_id = kmeans_model.assign(u_factor)
            label = 1 if rating >= 4.0 else 0
            
            if cluster_id not in cluster_data:
                cluster_data[cluster_id] = {'X': [], 'y': []}
                
            cluster_data[cluster_id]['X'].append(i_factor)
            cluster_data[cluster_id]['y'].append(label)

    # Convert to numpy arrays
    for cid in cluster_data:
        cluster_data[cid]['X'] = np.array(cluster_data[cid]['X'])
        cluster_data[cid]['y'] = np.array(cluster_data[cid]['y'])

    update_status("running", 80, "Running Phase 3: Training Cluster-Specific Re-Rankers (Logistic Regression)...")
    cluster_lr = ClusterLRModel()
    cluster_lr.fit(cluster_data)

    update_status("running", 85, "Running Phase 4: Training Stacking Meta-Learner (Blending Weights)...")
    # Now train Meta Learner
    for _, row in sampled_df.iterrows():
        uid = row['userId']
        iid = row['movieId']
        rating = row['rating']
        
        if uid in user_to_index and iid in item_to_index:
            u_idx = user_to_index[uid]
            i_idx = item_to_index[iid]
            
            u_factor = mf_model.user_factors[u_idx]
            i_factor = mf_model.item_factors[i_idx]
            
            cluster_id = kmeans_model.assign(u_factor)
            label = 1 if rating >= 4.0 else 0
            
            mf_score = float(u_factor.dot(i_factor))
            lr_score = cluster_lr.predict(cluster_id, i_factor)
            
            mf_scores.append(mf_score)
            lr_scores.append(lr_score)
            labels.append(label)

    meta_learner = StackingMetaLearner()
    meta_learner.fit(mf_scores, lr_scores, labels)

    update_status("running", 90, "Packaging Multi-stage Models...")
    registry = ModelRegistry("models")
    
    # We save the models and the movies dataframe
    model_data = {
        'model': mf_model,
        'cluster_model': kmeans_model,
        'ranker_model': cluster_lr,
        'meta_model': meta_learner,
        'movies_df': movies_df
    }
    
    update_status("running", 95, "Saving artifacts to Model Registry...")
    version = "v" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    registry.register(version, model_data)
    registry.activate(version)
        
    update_status("completed", 100, f"Pipeline Execution Completed Successfully! Activated {version}")

if __name__ == '__main__':
    run_training_pipeline()
