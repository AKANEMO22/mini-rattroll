from typing import Any
from sklearn.cluster import KMeans

class KMeansClusterer:
    """K-Means Clustering for User Embeddings."""
    def __init__(self, n_clusters: int = 10):
        self.n_clusters = n_clusters
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.user_to_cluster = {}

    def fit(self, embeddings: Any) -> None:
        # Assuming embeddings is a matrix
        self.model.fit(embeddings)

    def assign(self, user_embedding: Any) -> int:
        # Assign cluster based on nearest centroid
        return int(self.model.predict([user_embedding])[0])
