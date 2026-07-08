import pytest
from src.domain.models import Movie, User, Rating
from datetime import datetime

def test_movie_model():
    m = Movie(movie_id="1", title="Toy Story", genres=["Animation"])
    assert m.title == "Toy Story"
    assert "Animation" in m.genres

def test_rating_model():
    r = Rating(user_id="u1", movie_id="m1", timestamp=datetime.now(), score=4.5)
    assert r.score == 4.5
    assert r.user_id == "u1"
