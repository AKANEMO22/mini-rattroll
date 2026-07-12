import pandas as pd
from src.core.contexts import PipelineContext

class PreprocessingStep:
    """Cleans Raw Dataset and prepares it for feature extraction."""
    def __init__(self, config: dict = None):
        self.config = config or {}

    def execute(self, context: PipelineContext) -> None:
        if context.raw_data is None:
            raise ValueError("Raw data not loaded in PipelineContext")
            
        print("Starting Preprocessing: Removing users/movies with < 5 interactions...")
        
        # Mock logic
        context.processed_data = context.raw_data
        print("Preprocessing completed.")
