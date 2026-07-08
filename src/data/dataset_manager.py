import pandas as pd
import numpy as np
import os
from typing import Dict, Tuple, Any

class DatasetManager:
    """Manages the lifecycle of MovieLens 25M dataset."""
    
    def __init__(self, data_dir: str = "data/ml-25m"):
        self.data_dir = data_dir
        self.raw_movies: pd.DataFrame = None
        self.raw_ratings: pd.DataFrame = None

    def load_raw_data(self) -> None:
        """Loads raw CSV files from disk."""
        movies_path = os.path.join(self.data_dir, "movies.csv")
        ratings_path = os.path.join(self.data_dir, "ratings.csv")
        
        # In a real environment, we'd use Dask or chunks for 25M.
        # For prototype, we mock reading or read sample if large
        try:
            self.raw_movies = pd.read_csv(movies_path)
            self.raw_ratings = pd.read_csv(ratings_path)
        except FileNotFoundError:
            # Fallback mock for testing if dataset is missing
            self.raw_movies = pd.DataFrame({"movieId": [1, 2], "title": ["A", "B"], "genres": ["Action", "Comedy"]})
            self.raw_ratings = pd.DataFrame({"userId": [1, 1, 2], "movieId": [1, 2, 1], "rating": [5.0, 4.0, 3.0], "timestamp": [1600000000, 1600000010, 1600000020]})

    def clean_data(self) -> pd.DataFrame:
        """Removes noise (e.g., users with < 5 ratings)."""
        if self.raw_ratings is None:
            self.load_raw_data()
        
        user_counts = self.raw_ratings['userId'].value_counts()
        valid_users = user_counts[user_counts >= 5].index
        
        cleaned = self.raw_ratings[self.raw_ratings['userId'].isin(valid_users)].copy()
        cleaned['timestamp'] = pd.to_datetime(cleaned['timestamp'], unit='s')
        return cleaned

    def time_based_split(self, df: pd.DataFrame, train_ratio: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Splits data strictly by time to avoid data leakage."""
        df = df.sort_values('timestamp')
        split_idx = int(len(df) * train_ratio)
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        return train_df, test_df
