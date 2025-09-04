from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from statistics import mean

app = FastAPI(title="Movie Collection API")


class SortField(str, Enum):
    title = "title"
    year = "year"
    rating = "rating"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class MovieBase(BaseModel):
    title: str = Field(..., min_length=2)
    genre: Optional[str] = "Unknown"
    year: int = Field(..., gt=1888)
    rating: float = Field(..., ge=0.0, le=10.0)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    genre: Optional[str]
    year: Optional[int] = Field(None, gt=1888)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)


class Movie(MovieBase):
    id: int


movies_db: Dict[int, Movie] = {}
next_id = 1


def get_next_id():
    global next_id
    id_ = next_id
    next_id += 1
    return id_


@app.post("/movies/", response_model=Movie, status_code=201)
def add_movie(movie: MovieCreate):
    movie_id = get_next_id()
    movie_obj = Movie(id=movie_id, **movie.model_dump())
    movies_db[movie_id] = movie_obj
    return movie_obj


@app.get("/movies/", response_model=List[Movie])
def list_movies(
        genre: Optional[str] = Query(None),
        min_rating: Optional[float] = Query(None, ge=0.0, le=10.0),
        from_year: Optional[int] = Query(None, gt=1888),
        to_year: Optional[int] = Query(None, gt=1888),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        sort_by: SortField = Query(SortField.title),
        order: SortOrder = Query(SortOrder.asc)
):
    results = list(movies_db.values())
    if genre:
        results = [m for m in results if m.genre.lower() == genre.lower()]
    if min_rating is not None:
        results = [m for m in results if m.rating >= min_rating]
    if from_year is not None:
        results = [m for m in results if m.year >= from_year]
    if to_year is not None:
        results = [m for m in results if m.year <= to_year]

    reverse = order == SortOrder.desc
    results.sort(key=lambda m: getattr(m, sort_by.value), reverse=reverse)

    return results[skip: skip + limit]


@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    movie = movies_db.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie_update: MovieUpdate):
    movie = movies_db.get(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    update_data = movie_update.dict(exclude_unset=True)
    updated = movie.model_copy(update=update_data)
    movies_db[movie_id] = updated
    return updated


@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int):
    if movie_id not in movies_db:
        raise HTTPException(status_code=404, detail="Movie not found")
    del movies_db[movie_id]
    return


@app.post("/movies/bulk/", response_model=List[Movie], status_code=201)
def bulk_add_movies(movies: List[MovieCreate]):
    added = []
    for movie in movies:
        movie_id = get_next_id()
        movie_obj = Movie(id=movie_id, **movie.model_dump())
        movies_db[movie_id] = movie_obj
        added.append(movie_obj)
    return added


@app.delete("/movies/bulk/", status_code=204)
def bulk_delete_movies(ids: List[int] = Body(..., embed=True)):
    not_found = [mid for mid in ids if mid not in movies_db]
    if not_found:
        raise HTTPException(status_code=404, detail=f"Movies not found: {not_found}")
    for mid in ids:
        del movies_db[mid]
    return


@app.get("/movies/search/", response_model=List[Movie])
def search_movies(q: str = Query(..., min_length=1)):
    q_lower = q.lower()
    results = [m for m in movies_db.values() if q_lower in m.title.lower() or q_lower in m.genre.lower()]
    return results


@app.get("/movies/stats/")
def movies_stats():
    total = len(movies_db)
    if total == 0:
        avg_rating = 0.0
        newest = None
        oldest = None
        per_genre = {}
    else:
        avg_rating = round(mean(m.rating for m in movies_db.values()), 2)
        years = [m.year for m in movies_db.values()]
        newest = max(years)
        oldest = min(years)
        per_genre = {}
        for m in movies_db.values():
            per_genre[m.genre] = per_genre.get(m.genre, 0) + 1
    return {
        "total_movies": total,
        "average_rating": avg_rating,
        "movies_per_genre": per_genre,
        "newest_movie_year": newest,
        "oldest_movie_year": oldest,
    }
