import pandas as pd
from sklearn.decomposition import PCA
from src.interfaces.base import PipelineStep
from src.core.contexts import PipelineContext

class FeatureEngineeringStep(PipelineStep):
    """Applies TF-IDF, Encoding, and PCA on Processed Dataset."""
    def __init__(self, n_components: int = 50):
        self.pca = PCA(n_components=n_components, random_state=42)

    def execute(self, context: PipelineContext) -> None:
        if context.processed_data is None:
            raise ValueError("Processed data not available.")
            
        print("Starting Feature Engineering & PCA...")
        
        # Extract features and fit PCA
        # Mock logic
        context.features['pca_transformed'] = "pca_matrix_mock"
        context.models['pca_transformer'] = self.pca
        
        print("Feature Engineering completed.")
