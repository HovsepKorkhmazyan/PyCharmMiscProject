from fastapi import FastAPI, HTTPException, Query, Body, Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from collections import Counter
import uvicorn

app = FastAPI()

db_movies = [
    {"id": 1, "title": "The Shawshank Redemption", "genre": "Drama", "year": 1994, "rating": 9.3},
    {"id": 2, "title": "The Godfather", "genre": "Crime", "year": 1972, "rating": 9.2},
    {"id": 3, "title": "The Dark Knight", "genre": "Action", "year": 2008, "rating": 9.0},
    {"id": 4, "title": "Pulp Fiction", "genre": "Crime", "year": 1994, "rating": 8.9},
    {"id": 5, "title": "Forrest Gump", "genre": "Drama", "year": 1994, "rating": 8.8},
    {"id": 6, "title": "Inception", "genre": "Sci-Fi", "year": 2010, "rating": 8.8},
    {"id": 7, "title": "The Matrix", "genre": "Sci-Fi", "year": 1999, "rating": 8.7},
]

current_id = len(db_movies) + 1


class MovieBase(BaseModel):
    title: str = Field(..., min_length=2, description="The title of the movie.")
    genre: str = Field("Unknown", description="The genre of the movie (defaults to 'Unknown').")
    year: int = Field(..., gt=1888, description="The release year (must be after 1888).")
    rating: float = Field(..., ge=0.0, le=10.0, description="The rating from 0.0 to 10.0.")


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    genre: Optional[str] = None
    year: Optional[int] = Field(None, gt=1888)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)


class BulkDeleteRequest(BaseModel):
    movie_ids: List[int]


def find_movie_by_id(movie_id: int) -> Optional[Dict]:
    for movie in db_movies:
        if movie["id"] == movie_id:
            return movie
    return None


@app.post("/movies/", response_model=Movie, status_code=201, tags=["CRUD Operations"])
def add_new_movie(movie: MovieCreate):
    global current_id
    new_movie_data = movie.model_dump()
    new_movie_data["id"] = current_id
    db_movies.append(new_movie_data)
    current_id += 1
    return new_movie_data


@app.get("/movies/", response_model=List[Movie], tags=["CRUD Operations", "Querying"])
def list_all_movies(
        genre: Optional[str] = Query(None, description="Filter by genre"),
        min_rating: Optional[float] = Query(None, ge=0.0, le=10.0, description="Filter by minimum rating"),
        from_year: Optional[int] = Query(None, gt=1888, description="Filter from a specific year"),
        to_year: Optional[int] = Query(None, gt=1888, description="Filter up to a specific year"),
        sort_by: Optional[str] = Query(None, enum=["title", "year", "rating"], description="Sort by field"),
        sort_order: Optional[str] = Query("asc", enum=["asc", "desc"], description="Sort order"),
        skip: int = Query(0, ge=0, description="Records to skip for pagination"),
        limit: int = Query(10, ge=1, description="Max records to return")
):
    movies_to_return = db_movies.copy()

    if genre:
        movies_to_return = [m for m in movies_to_return if m["genre"].lower() == genre.lower()]
    if min_rating is not None:
        movies_to_return = [m for m in movies_to_return if m["rating"] >= min_rating]
    if from_year:
        movies_to_return = [m for m in movies_to_return if m["year"] >= from_year]
    if to_year:
        movies_to_return = [m for m in movies_to_return if m["year"] <= to_year]

    if sort_by:
        movies_to_return.sort(key=lambda x: x[sort_by], reverse=(sort_order == "desc"))

    return movies_to_return[skip: skip + limit]


@app.get("/movies/{movie_id}", response_model=Movie, tags=["CRUD Operations"])
def get_movie_by_id(movie_id: int = Path(..., description="The ID of the movie to get.", gt=0)):
    movie = find_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found.")
    return movie


@app.put("/movies/{movie_id}", response_model=Movie, tags=["CRUD Operations"])
def update_a_movie(movie_id: int, movie_update: MovieUpdate):
    movie = find_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found.")

    update_data = movie_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        movie[key] = value

    return movie


@app.delete("/movies/{movie_id}", status_code=204, tags=["CRUD Operations"])
def delete_a_movie(movie_id: int):
    movie = find_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with ID {movie_id} not found.")
    db_movies.remove(movie)
    return


@app.post("/movies/bulk/", response_model=List[Movie], status_code=201, tags=["Bulk Operations"])
def add_multiple_movies(movies: List[MovieCreate]):
    global current_id
    newly_added = []
    for movie_data in movies:
        new_movie = movie_data.model_dump()
        new_movie["id"] = current_id
        db_movies.append(new_movie)
        newly_added.append(new_movie)
        current_id += 1
    return newly_added


@app.delete("/movies/bulk/", status_code=200, tags=["Bulk Operations"])
def delete_multiple_movies(delete_request: BulkDeleteRequest):
    global db_movies
    ids_to_delete = set(delete_request.movie_ids)
    original_count = len(db_movies)

    db_movies = [movie for movie in db_movies if movie["id"] not in ids_to_delete]

    deleted_count = original_count - len(db_movies)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="None of the provided movie IDs were found.")

    return {"status": "success", "deleted_count": deleted_count, "ids_deleted": sorted(list(ids_to_delete))}


@app.get("/movies/search/", response_model=List[Movie], tags=["Advanced Features"])
def search_movies(q: str = Query(..., min_length=1, description="Search keyword for title or genre")):
    search_term = q.lower()
    results = [
        movie for movie in db_movies
        if search_term in movie["title"].lower() or search_term in movie["genre"].lower()
    ]
    return results


@app.get("/movies/stats/", response_model=Dict[str, Any], tags=["Advanced Features"])
def get_movie_stats():
    if not db_movies:
        return {
            "total_movies": 0,
            "average_rating": 0.0,
            "movies_per_genre": {},
            "newest_movie": None,
            "oldest_movie": None
        }

    total_movies = len(db_movies)
    average_rating = round(sum(m["rating"] for m in db_movies) / total_movies, 2)
    genres = [m["genre"] for m in db_movies]
    movies_per_genre = Counter(genres)
    newest_movie = max(db_movies, key=lambda x: x["year"])
    oldest_movie = min(db_movies, key=lambda x: x["year"])

    return {
        "total_movies": total_movies,
        "average_rating": average_rating,
        "movies_per_genre": movies_per_genre,
        "newest_movie": newest_movie,
        "oldest_movie": oldest_movie
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)