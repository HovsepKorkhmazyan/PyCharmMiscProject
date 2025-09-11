import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

app = FastAPI(title="Movie API")

SECRET_KEY = ""
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": get_password_hash("testpassword")
    }
}

def get_user(db, username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token, summary="User Login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

class MovieBase(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field("Unknown")
    year: int = Field(..., gt=1888)
    rating: float = Field(..., ge=0.0, le=10.0)

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2)
    genre: Optional[str] = None
    year: Optional[int] = Field(None, gt=1888)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)

db_movies = [
    Movie(id=1, title="The Shawshank Redemption", genre="Drama", year=1994, rating=9.3),
    Movie(id=2, title="The Godfather", genre="Crime", year=1972, rating=9.2),
    Movie(id=3, title="The Dark Knight", genre="Action", year=2008, rating=9.0),
]
movie_counter = len(db_movies) + 1

@app.post("/movies/", response_model=Movie, summary="Create a Movie")
async def create_movie(movie: MovieCreate, current_user: User = Depends(get_current_user)):
    global movie_counter
    new_movie = Movie(
        id=movie_counter,
        title=movie.title,
        genre=movie.genre,
        year=movie.year,
        rating=movie.rating
    )
    db_movies.append(new_movie)
    movie_counter += 1
    return new_movie

@app.get("/movies/", response_model=List[Movie], summary="Get All Movies")
async def get_movies():
    return db_movies

@app.get("/movies/{movie_id}", response_model=Movie, summary="Get Movie by ID")
async def get_movie(movie_id: int, current_user: User = Depends(get_current_user)):
    for movie in db_movies:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

@app.put("/movies/{movie_id}", response_model=Movie, summary="Update a Movie")
async def update_movie(movie_id: int, movie_data: MovieUpdate, current_user: User = Depends(get_current_user)):
    for movie in db_movies:
        if movie.id == movie_id:
            if movie_data.title is not None:
                movie.title = movie_data.title
            if movie_data.genre is not None:
                movie.genre = movie_data.genre
            if movie_data.year is not None:
                movie.year = movie_data.year
            if movie_data.rating is not None:
                movie.rating = movie_data.rating
            return movie
    raise HTTPException(status_code=44, detail="Movie not found")

@app.delete("/movies/{movie_id}", summary="Delete a Movie")
async def delete_movie(movie_id: int, current_user: User = Depends(get_current_user)):
    for movie in db_movies:
        if movie.id == movie_id:
            db_movies.remove(movie)
            return {"message": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)