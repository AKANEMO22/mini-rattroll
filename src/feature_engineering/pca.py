from typing import Any
from sklearn.decomposition import PCA
from src.interfaces.base import PipelineStep
from src.core.contexts import PipelineContext

class PCAFeatureExtractor(PipelineStep):
    """Applies PCA to reduce dimensionality of sparse feature matrices."""
    def __init__(self, n_components: int = 50):
        self.pca = PCA(n_components=n_components, random_state=42)

    def execute(self, context: PipelineContext) -> None:
        # Assume context.processed_data contains feature matrices
        # In reality, we call fit_transform
        context.features['pca_transformed'] = []
        context.models['pca_transformer'] = self.pca
