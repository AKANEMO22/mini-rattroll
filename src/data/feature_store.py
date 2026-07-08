import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from typing import Dict, Any

class FeatureStore:
    """Maintains pre-computed features and sparse matrices for fast ML access."""
    
    def __init__(self):
        self.user_item_matrix: csr_matrix = None
        self.user_mapping: Dict[int, int] = {}
        self.item_mapping: Dict[int, int] = {}
        
        self.reverse_user_mapping: Dict[int, int] = {}
        self.reverse_item_mapping: Dict[int, int] = {}

    def build_user_item_matrix(self, ratings_df: pd.DataFrame) -> csr_matrix:
        """Converts interaction dataframe into sparse CSR matrix."""
        unique_users = ratings_df['userId'].unique()
        unique_items = ratings_df['movieId'].unique()
        
        self.user_mapping = {u: i for i, u in enumerate(unique_users)}
        self.item_mapping = {item: i for i, item in enumerate(unique_items)}
        
        self.reverse_user_mapping = {i: u for u, i in self.user_mapping.items()}
        self.reverse_item_mapping = {i: item for item, i in self.item_mapping.items()}
        
        row_idx = ratings_df['userId'].map(self.user_mapping).values
        col_idx = ratings_df['movieId'].map(self.item_mapping).values
        data = ratings_df['rating'].values
        
        self.user_item_matrix = csr_matrix((data, (row_idx, col_idx)), shape=(len(unique_users), len(unique_items)))
        return self.user_item_matrix

    def get_user_interactions(self, internal_user_id: int) -> np.ndarray:
        if self.user_item_matrix is None:
            raise ValueError("FeatureStore not initialized.")
        return self.user_item_matrix[internal_user_id].toarray().flatten()
