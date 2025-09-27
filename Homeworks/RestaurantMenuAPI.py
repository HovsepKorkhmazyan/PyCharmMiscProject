from enum import Enum
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, delete, func, or_, select

DATABASE_URL = "sqlite:///RestaurantMenu.db"
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(title="Restaurant Menu API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


class MenuItemBase(SQLModel):
    name: str = Field(index=True, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, index=True, max_length=255)
    price: float = Field(gt=0, description="The price must be positive.")
    is_available: bool = Field(default=True)


class MenuItem(MenuItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemRead(MenuItemBase):
    id: int


class MenuItemUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    price: Optional[float] = Field(default=None, gt=0)
    is_available: Optional[bool] = None


class BulkDeleteRequest(SQLModel):
    ids: List[int]


class MenuStats(SQLModel):
    total_items: int
    available_items: int
    average_price: Optional[float]
    most_expensive_item: Optional[MenuItemRead]
    cheapest_item: Optional[MenuItemRead]


class SortField(str, Enum):
    ID = "id"
    NAME = "name"
    PRICE = "price"


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/menu/", response_model=List[MenuItemRead], tags=["Menu"])
def list_menu_items(
        session: Session = Depends(get_session),
        is_available: Optional[bool] = Query(None, description="Filter by availability"),
        min_price: Optional[float] = Query(None, description="Filter by minimum price"),
        max_price: Optional[float] = Query(None, description="Filter by maximum price"),
        search: Optional[str] = Query(None, description="Search in name and description"),
        skip: int = Query(0, ge=0, description="Number of items to skip"),
        limit: int = Query(100, gt=0, le=200, description="Number of items to return"),
        sort_by: SortField = Query(SortField.ID, description="Field to sort by"),
        sort_dir: SortDirection = Query(SortDirection.ASC, description="Sort direction"),
):
    query = select(MenuItem)
    if is_available is not None:
        query = query.where(MenuItem.is_available == is_available)
    if min_price is not None:
        query = query.where(MenuItem.price >= min_price)
    if max_price is not None:
        query = query.where(MenuItem.price <= max_price)
    if search:
        query = query.where(
            or_(MenuItem.name.contains(search), MenuItem.description.contains(search))
        )
    sort_column = getattr(MenuItem, sort_by.value)
    if sort_dir == SortDirection.DESC:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    query = query.offset(skip).limit(limit)
    items = session.exec(query).all()
    return items


@app.post("/menu/", response_model=MenuItemRead, status_code=201, tags=["Menu"])
def add_menu_item(item: MenuItemCreate, session: Session = Depends(get_session)):
    db_item = MenuItem.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.get("/menu/{item_id}", response_model=MenuItemRead, tags=["Menu"])
def get_menu_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@app.put("/menu/{item_id}", response_model=MenuItemRead, tags=["Menu"])
def update_menu_item(
        item_id: int, item_update: MenuItemUpdate, session: Session = Depends(get_session)
):
    db_item = session.get(MenuItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.delete("/menu/{item_id}", status_code=204, tags=["Menu"])
def delete_menu_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    session.delete(item)
    session.commit()
    return None


@app.post("/menu/bulk/", status_code=201, tags=["Bulk Operations"])
def add_menu_items_bulk(
        items: List[MenuItemCreate], session: Session = Depends(get_session)
):
    db_items = [MenuItem.model_validate(item) for item in items]
    session.add_all(db_items)
    session.commit()
    return {"detail": f"Successfully added {len(db_items)} items."}


@app.delete("/menu/bulk/", tags=["Bulk Operations"])
def delete_menu_items_bulk(
        request: BulkDeleteRequest, session: Session = Depends(get_session)
):
    query = delete(MenuItem).where(MenuItem.id.in_(request.ids))
    result = session.exec(query)
    session.commit()
    deleted_count = result.rowcount
    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail="None of the specified items were found."
        )
    return {"deleted_count": deleted_count}


@app.get("/menu/stats/", response_model=MenuStats, tags=["Statistics"])
def get_menu_stats(session: Session = Depends(get_session)):
    total_items = session.exec(select(func.count(MenuItem.id))).one_or_none() or 0
    available_items = session.exec(
        select(func.count(MenuItem.id)).where(MenuItem.is_available == True)
    ).one_or_none() or 0
    average_price = session.exec(select(func.avg(MenuItem.price))).one_or_none() or 0.0
    cheapest_item = session.exec(
        select(MenuItem).order_by(MenuItem.price.asc())
    ).first()
    most_expensive_item = session.exec(
        select(MenuItem).order_by(MenuItem.price.desc())
    ).first()

    return MenuStats(
        total_items=total_items,
        available_items=available_items,
        average_price=round(average_price, 2) if average_price else None,
        cheapest_item=cheapest_item,
        most_expensive_item=most_expensive_item,
    )
