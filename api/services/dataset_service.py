import pandas as pd
import os

class DatasetService:
    def __init__(self, data_dir="data/ml-25m"):
        self.data_dir = data_dir
        self.movies_df = None
        self.ratings_sample = None
        
    def _load_movies(self):
        if self.movies_df is None:
            movies_path = os.path.join(self.data_dir, "movies.csv")
            if os.path.exists(movies_path):
                self.movies_df = pd.read_csv(movies_path)
            else:
                self.movies_df = pd.DataFrame(columns=["movieId", "title", "genres"])

    def get_dataset_info(self):
        self._load_movies()
        ratings_path = os.path.join(self.data_dir, "ratings.csv")
        ratings_size = 0
        if os.path.exists(ratings_path):
            ratings_size = os.path.getsize(ratings_path) // (1024 * 1024) # MB
        return {
            "version": "MovieLens 25M",
            "movies_count": len(self.movies_df),
            "ratings_size_mb": ratings_size,
            "status": "Ready" if len(self.movies_df) > 0 else "Missing"
        }
        
    def search_movies(self, query: str):
        self._load_movies()
        if len(self.movies_df) == 0 or not query:
            return []
        
        # Simple case-insensitive search
        results = self.movies_df[self.movies_df['title'].str.contains(query, case=False, na=False)].head(10)
        return results.to_dict('records')

    def get_user_profile(self, user_id: int):
        # Scan a chunk of ratings to find user data without loading 25M rows
        ratings_path = os.path.join(self.data_dir, "ratings.csv")
        if not os.path.exists(ratings_path):
            return {"user_id": user_id, "history": []}
            
        chunk_iter = pd.read_csv(ratings_path, chunksize=100000)
        user_ratings = []
        found = False
        for chunk in chunk_iter:
            u_data = chunk[chunk['userId'] == user_id]
            if not u_data.empty:
                user_ratings.append(u_data)
                found = True
            elif found:
                break
            
            if chunk['userId'].max() > user_id:
                break
        
        if not user_ratings:
            return {"user_id": user_id, "history": []}
            
        res_df = pd.concat(user_ratings)
        
        # Load movies to join titles
        self._load_movies()
        if len(self.movies_df) > 0:
            res_df = res_df.merge(self.movies_df[['movieId', 'title', 'genres']], on='movieId', how='left')
            res_df['title'] = res_df['title'].fillna(res_df['movieId'].astype(str))
        else:
            res_df['title'] = res_df['movieId'].astype(str)
            res_df['genres'] = ""
            
        # Format timestamp
        if 'timestamp' in res_df.columns:
            res_df['date'] = pd.to_datetime(res_df['timestamp'], unit='s').dt.strftime('%d/%m/%Y %H:%M')
        else:
            res_df['date'] = "N/A"
            
        history_records = res_df.head(15).to_dict('records')
        
        # Calculate genre distribution
        genre_dist = []
        if 'genres' in res_df.columns:
            all_genres = res_df['genres'].dropna().str.split('|').explode()
            # Filter out empty or '(no genres listed)'
            all_genres = all_genres[~all_genres.isin(['', '(no genres listed)'])]
            if not all_genres.empty:
                counts = all_genres.value_counts().head(6)
                genre_dist = [{"name": k, "value": int(v)} for k, v in counts.items()]
        
        return {
            "user_id": user_id,
            "interaction_count": len(res_df),
            "avg_rating": round(res_df['rating'].mean(), 2),
            "history": history_records,
            "genre_distribution": genre_dist
        }

    def get_global_history(self):
        ratings_path = os.path.join(self.data_dir, "ratings.csv")
        if not os.path.exists(ratings_path):
            return []
            
        df = pd.read_csv(ratings_path, nrows=100)
        
        self._load_movies()
        if len(self.movies_df) > 0:
            df = df.merge(self.movies_df[['movieId', 'title', 'genres']], on='movieId', how='left')
            df['title'] = df['title'].fillna(df['movieId'].astype(str))
        else:
            df['title'] = df['movieId'].astype(str)
            df['genres'] = ""
            
        if 'timestamp' in df.columns:
            df['date'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime('%d/%m/%Y %H:%M')
        else:
            df['date'] = "N/A"
            
        return df.to_dict('records')
