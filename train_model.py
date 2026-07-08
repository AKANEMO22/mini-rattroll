import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
import pickle
import os

def train():
    print("Loading data...")
    # Load movies
    movies_df = pd.read_csv('data/ml-25m/movies.csv')
    
    # Load a sample of ratings (100k) to prevent OOM
    # We'll read the first 100k ratings for training
    ratings_df = pd.read_csv('data/ml-25m/ratings.csv', nrows=100000)
    
    print(f"Loaded {len(ratings_df)} ratings.")
    
    # Map user and item IDs to matrix indices
    users = ratings_df['userId'].unique()
    items = ratings_df['movieId'].unique()
    
    user_to_index = {uid: idx for idx, uid in enumerate(users)}
    item_to_index = {iid: idx for idx, iid in enumerate(items)}
    
    index_to_user = {idx: uid for uid, idx in user_to_index.items()}
    index_to_item = {idx: iid for iid, idx in item_to_index.items()}
    
    # Create sparse matrix
    row = ratings_df['userId'].map(user_to_index).values
    col = ratings_df['movieId'].map(item_to_index).values
    data = ratings_df['rating'].values
    
    sparse_matrix = csr_matrix((data, (row, col)), shape=(len(users), len(items)))
    
    print("Training TruncatedSVD...")
    # Train SVD
    n_components = min(50, len(items) - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    user_factors = svd.fit_transform(sparse_matrix)
    item_factors = svd.components_.T
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    model_data = {
        'user_factors': user_factors,
        'item_factors': item_factors,
        'user_to_index': user_to_index,
        'item_to_index': item_to_index,
        'index_to_user': index_to_user,
        'index_to_item': index_to_item,
        'movies_df': movies_df
    }
    
    with open('models/svd_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
        
    print("Model trained and saved to models/svd_model.pkl")

if __name__ == '__main__':
    train()
