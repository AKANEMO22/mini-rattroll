import pandas as pd
from typing import Any
from src.interfaces.base import PipelineStep
from src.core.contexts import PipelineContext

class DataPreprocessor(PipelineStep):
    """Loads and cleans raw data (e.g. MovieLens)."""
    def __init__(self, config: dict):
        self.config = config

    def execute(self, context: PipelineContext) -> None:
        # If context.raw_data is None, load from config path
        if context.raw_data is None:
            # In a real environment, read from self.config['data_path']
            context.raw_data = {"interactions": [], "users": [], "items": []}
        
        # Clean data (mock logic for removing NaNs and low-interaction users)
        context.processed_data = context.raw_data
