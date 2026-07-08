from src.interfaces.base import BaseMF, BaseClusterer, BaseRanker
from src.recommender.matrix_factorization.svd_model import SVDModel
from src.recommender.clustering.kmeans_clusterer import KMeansClusterer

class RecommenderFactory:
    """Factory to instantiate core recommendation algorithms."""
    
    @staticmethod
    def create_mf(config: dict) -> BaseMF:
        n_factors = config.get('n_factors', 100)
        lr = config.get('lr', 0.005)
        return SVDModel(n_factors=n_factors, lr=lr)
        
    @staticmethod
    def create_clusterer(config: dict) -> BaseClusterer:
        n_clusters = config.get('n_clusters', 10)
        return KMeansClusterer(n_clusters=n_clusters)
        
    @staticmethod
    def create_ranker(config: dict) -> BaseRanker:
        # To be implemented in Phase 4
        pass
