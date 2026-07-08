from src.interfaces.base import PipelineStep
from src.core.contexts import PipelineContext
from src.interfaces.base import BaseMF, BaseClusterer, BaseRanker
from src.recommender.meta.stacking import StackingMetaLearner

class TrainMFStep(PipelineStep):
    """Pipeline step to train Matrix Factorization."""
    def __init__(self, mf_model: BaseMF):
        self.mf_model = mf_model

    def execute(self, context: PipelineContext) -> None:
        self.mf_model.fit(context.processed_data)
        context.embeddings['user'] = getattr(self.mf_model, 'get_user_embeddings', lambda: {})()
        context.models['mf'] = self.mf_model

class TrainKMeansStep(PipelineStep):
    """Pipeline step to train KMeans Clustering."""
    def __init__(self, clusterer: BaseClusterer):
        self.clusterer = clusterer

    def execute(self, context: PipelineContext) -> None:
        if 'user' in context.embeddings:
            embeddings_matrix = list(context.embeddings['user'].values())
            if embeddings_matrix:
                self.clusterer.fit(embeddings_matrix)
        context.models['kmeans'] = self.clusterer

class TrainRankingStep(PipelineStep):
    """Pipeline step to train Cluster-Specific Logistic Regression."""
    def __init__(self, ranker: BaseRanker):
        self.ranker = ranker

    def execute(self, context: PipelineContext) -> None:
        self.ranker.fit(context.processed_data)
        context.models['cluster_lr'] = self.ranker

class TrainMetaStep(PipelineStep):
    """Pipeline step to train Stacking Meta Learner."""
    def __init__(self, meta_learner: StackingMetaLearner):
        self.meta_learner = meta_learner

    def execute(self, context: PipelineContext) -> None:
        # Extract features and labels from context
        mf_scores = []
        lr_scores = []
        labels = []
        self.meta_learner.fit(mf_scores, lr_scores, labels)
        context.models['meta_learner'] = self.meta_learner
