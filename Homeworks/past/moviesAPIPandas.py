import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any

app = FastAPI(
    title="Movie API",
    description="An API to get information about movies.",
    version="1.0.0",
)

try:
    movies_df = pd.read_csv("movies.csv")
    movies_list = movies_df.to_dict(orient="records")
except FileNotFoundError:
    movies_df = pd.DataFrame()
    movies_list = []


@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API! Go to /docs to see the endpoints."}


@app.get("/movies", response_model=List[Dict[str, Any]])
def get_all_movies():
    if not movies_list:
        raise HTTPException(status_code=404, detail="No movie data available.")
    return movies_list


@app.get("/movies/{movie_id}", response_model=Dict[str, Any])
def get_movie_by_id(movie_id: int):
    movie = next((movie for movie in movies_list if movie['id'] == movie_id), None)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found.")
    return movie


@app.get("/movies/genre/{genre}", response_model=List[Dict[str, Any]])
def get_movies_by_genre(genre: str):
    genre_movies = [movie for movie in movies_list if movie['genre'].lower() == genre.lower()]
    return genre_movies


@app.get("/movies/top-rated/", response_model=List[Dict[str, Any]])
def get_top_rated_movies(limit: int = Query(5, ge=1, description="Number of top-rated movies to return.")):
    sorted_movies = sorted(movies_list, key=lambda x: x['rating'], reverse=True)
    return sorted_movies[:limit]


@app.get("/movies/stats/")
def get_movie_stats():
    if movies_df.empty:
        raise HTTPException(status_code=503, detail="Movie data is not available to generate stats.")

    total_movies = len(movies_df)
    average_rating = round(movies_df['rating'].mean(), 2)

    longest_movie_row = movies_df.loc[movies_df['duration_min'].idxmax()]
    longest_movie_title = longest_movie_row['title']

    shortest_movie_row = movies_df.loc[movies_df['duration_min'].idxmin()]
    shortest_movie_title = shortest_movie_row['title']

    return {
        "total_movies": total_movies,
        "average_rating": average_rating,
        "longest_movie": longest_movie_title,
        "shortest_movie": shortest_movie_title
    }


@app.get("/movies/average-rating-per-genre/")
def get_average_rating_per_genre():
    if movies_df.empty:
        raise HTTPException(status_code=503, detail="Movie data is not available to generate stats.")

    avg_ratings = movies_df.groupby('genre')['rating'].mean().round(2).to_dict()
    return avg_ratings