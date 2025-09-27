import uvicorn
import csv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional

SQLALCHEMY_DATABASE_URL = "sqlite:///./cities.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class CityModel(Base):
    __tablename__ = "cities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, index=True)
    population = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    continent = Column(String)


class CityBase(BaseModel):
    name: str
    country: str
    population: int
    latitude: float
    longitude: float
    continent: str


class CityCreate(CityBase):
    pass


class CitySchema(CityBase):
    id: int

    class Config:
        orm_mode = True


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cities/", response_model=CitySchema, tags=["Cities"])
def add_city(city: CityCreate, db: Session = Depends(get_db)):
    existing_city = db.query(CityModel).filter(CityModel.name.ilike(city.name)).first()
    if existing_city:
        raise HTTPException(status_code=400, detail=f"City '{city.name}' already exists.")

    db_city = CityModel(**city.model_dump())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@app.post("/populate-cities/", tags=["Cities"])
def populate_cities(db: Session = Depends(get_db)):
    if db.query(CityModel).first():
        raise HTTPException(status_code=400, detail="City data has already been populated.")

    try:
        with open('CountryInfo.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            cities_to_add = []
            for row in reader:
                if not row:
                    continue
                try:
                    city = CityModel(
                        name=row[0], country=row[1], population=int(row[2]),
                        latitude=float(row[3]), longitude=float(row[4]), continent=row[5]
                    )
                    cities_to_add.append(city)
                except (ValueError, IndexError) as e:
                    print(f"Skipping row due to error: {row} - {e}")
                    continue
            if not cities_to_add:
                raise HTTPException(status_code=400, detail="No valid city data found in the CSV file.")
            db.add_all(cities_to_add)
            db.commit()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CountryInfo.csv file not found.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    return {"message": f"{len(cities_to_add)} cities have been successfully added to the database."}


@app.get("/cities/", response_model=List[CitySchema], tags=["Cities"])
def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = db.query(CityModel).offset(skip).limit(limit).all()
    return cities


@app.get("/cities/continent/{continent_name}", response_model=List[CitySchema], tags=["Cities"])
def get_cities_by_continent(continent_name: str, db: Session = Depends(get_db)):
    cities = db.query(CityModel).filter(CityModel.continent.ilike(continent_name)).all()
    if not cities:
        raise HTTPException(status_code=404, detail=f"No cities found for continent: {continent_name}")
    return cities


@app.get("/cities/by-population/", response_model=List[CitySchema], tags=["Cities"])
def get_cities_by_population(min_pop: int = 0, max_pop: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(CityModel).filter(CityModel.population >= min_pop)
    if max_pop is not None:
        query = query.filter(CityModel.population <= max_pop)

    return query.all()


@app.put("/cities/{city_name}", response_model=CitySchema, tags=["Cities"])
def update_city(city_name: str, city_update: CityCreate, db: Session = Depends(get_db)):
    db_city = db.query(CityModel).filter(CityModel.name.ilike(city_name)).first()
    if not db_city:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found.")

    update_data = city_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city


@app.delete("/cities/{city_name}", response_model=dict, tags=["Cities"])
def delete_city(city_name: str, db: Session = Depends(get_db)):
    city_to_delete = db.query(CityModel).filter(CityModel.name.ilike(city_name)).first()
    if not city_to_delete:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found.")

    deleted_city_name = city_to_delete.name
    db.delete(city_to_delete)
    db.commit()
    return {"message": f"City '{deleted_city_name}' deleted successfully."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

