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
    print("Initializing Pipeline...")
    pipeline = Pipeline()
    
    # We create a step with our SVDModel
    mf_model = SVDModel(n_factors=50)
    pipeline.add_step(TrainMFStep(mf_model))
    
    print("Loading ML-25M dataset (This might take a moment)...")
    movies_df = pd.read_csv('data/ml-25m/movies.csv')
    
    # For full 25M dataset, we read directly. 
    # Pandas handles 25M rows of 4 columns comfortably on modern machines (~1GB RAM).
    ratings_df = pd.read_csv('data/ml-25m/ratings.csv', usecols=['userId', 'movieId', 'rating'])
    
    print(f"Loaded {len(ratings_df)} ratings.")
    
    # Building User/Item mappings
    print("Building Mappings and Sparse Matrix...")
    users = ratings_df['userId'].unique()
    items = ratings_df['movieId'].unique()
    
    user_to_index = {uid: idx for idx, uid in enumerate(users)}
    item_to_index = {iid: idx for idx, iid in enumerate(items)}
    
    row = ratings_df['userId'].map(user_to_index).values
    col = ratings_df['movieId'].map(item_to_index).values
    data = ratings_df['rating'].values
    
    sparse_matrix = csr_matrix((data, (row, col)), shape=(len(users), len(items)))
    
    # Create the PipelineContext
    context = PipelineContext()
    context.processed_data = {
        'sparse_matrix': sparse_matrix,
        'user_to_index': user_to_index,
        'item_to_index': item_to_index
    }
    
    print("Running Pipeline Execution (Training SVD on 25M ratings)...")
    # This executes mf_model.fit inside the step
    pipeline.run(context)
    
    print("Saving trained model to models/svd_model.pkl...")
    os.makedirs('models', exist_ok=True)
    
    # We save the model and the movies dataframe
    model_data = {
        'model': mf_model,
        'movies_df': movies_df
    }
    
    with open('models/svd_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
        
    print("Pipeline Execution Completed Successfully!")

if __name__ == '__main__':
    run_training_pipeline()
