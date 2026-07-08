from src.interfaces.base import PipelineStep
from src.core.contexts import PipelineContext
from src.recommender.matrix_factorization.svd_model import SVDModel
from src.recommender.clustering.kmeans_clusterer import KMeansClusterer
from src.recommender.ranking.cluster_lr import ClusterLRModel
from src.recommender.meta.stacking import StackingMetaLearner

class TrainMFStep(PipelineStep):
    def execute(self, context: PipelineContext) -> None:
        print("Training Matrix Factorization (SVD)...")
        model = SVDModel()
        context.models['svd'] = model

class TrainKMeansStep(PipelineStep):
    def execute(self, context: PipelineContext) -> None:
        print("Training KMeans Clustering on User Embeddings...")
        model = KMeansClusterer(n_clusters=5)
        context.models['kmeans'] = model

class TrainRankingStep(PipelineStep):
    def execute(self, context: PipelineContext) -> None:
        print("Training Cluster Logistic Regression...")
        model = ClusterLRModel()
        context.models['cluster_lr'] = model

class TrainMetaLearnerStep(PipelineStep):
    def execute(self, context: PipelineContext) -> None:
        print("Training Stacking Meta Learner...")
        model = StackingMetaLearner()
        context.models['meta_learner'] = model
