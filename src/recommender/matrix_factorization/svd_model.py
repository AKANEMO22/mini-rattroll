from typing import Any, Dict
from sklearn.decomposition import TruncatedSVD
import numpy as np

class SVDModel:
    """Matrix Factorization implementation using SVD."""
    def __init__(self, n_factors: int = 100, lr: float = 0.005):
        self.n_factors = n_factors
        self.lr = lr
        self.user_factors = None
        self.item_factors = None
        self.user_to_index = {}
        self.item_to_index = {}
        self.index_to_user = {}
        self.index_to_item = {}
        self.user_relevant_count = {}

    def fit(self, data: Any) -> None:
        """
        data expected to be a dict with:
        - 'sparse_matrix': scipy.sparse.csr_matrix
        - 'user_to_index': dict
        - 'item_to_index': dict
        """
        sparse_matrix = data['sparse_matrix']
        self.user_to_index = data['user_to_index']
        self.item_to_index = data['item_to_index']
        self.index_to_user = {idx: uid for uid, idx in self.user_to_index.items()}
        self.index_to_item = {idx: iid for iid, idx in self.item_to_index.items()}
        
        # Calculate true relevant items per user for exact Recall evaluation
        self.user_relevant_count = {}
        for u_idx in range(sparse_matrix.shape[0]):
            row = sparse_matrix.getrow(u_idx)
            relevant_count = np.sum(row.data >= 4.0)
            uid = self.index_to_user.get(u_idx)
            if uid is not None:
                self.user_relevant_count[str(uid)] = int(relevant_count)
        
        n_components = min(self.n_factors, sparse_matrix.shape[1] - 1)
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        
        # Fit and extract latent factors
        self.user_factors = svd.fit_transform(sparse_matrix)
        self.item_factors = svd.components_.T

    def predict(self, user_id: int, item_id: int) -> float:
        """Dot product of user and item latent factors."""
        if self.user_factors is None or self.item_factors is None:
            return 0.0
            
        u_idx = self.user_to_index.get(user_id)
        i_idx = self.item_to_index.get(item_id)
        
        if u_idx is None or i_idx is None:
            return 0.0
            
        return float(np.dot(self.user_factors[u_idx], self.item_factors[i_idx]))

    def get_user_embeddings(self) -> dict:
        if self.user_factors is None:
            return {}
        return {self.index_to_user[i]: self.user_factors[i] for i in range(len(self.user_factors))}
