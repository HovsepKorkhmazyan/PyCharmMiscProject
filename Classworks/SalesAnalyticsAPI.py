import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel, ConfigDict
from typing import List, Literal
import pandas as pd
import datetime
import os
from contextlib import asynccontextmanager
import io
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fastapi.responses import Response

DATABASE_URL = "sqlite:///./sales.db"
CSV_FILE = "sales_data.csv"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SaleDB(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, index=True)
    category = Column(String, index=True)
    quantity = Column(Integer)
    price = Column(Float)
    date = Column(Date)


class SaleBase(BaseModel):
    product: str
    category: str
    quantity: int
    price: float
    date: datetime.date


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class AnalyticsSummary(BaseModel):
    total_revenue: float
    total_items_sold: int
    average_order_value: float
    sales_by_category: dict
    revenue_by_category: dict


class MessageResponse(BaseModel):
    detail: str


def create_db_and_seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        is_empty = db.query(SaleDB).first() is None
        if is_empty and os.path.exists(CSV_FILE):
            print(f"Database is empty. Seeding data from {CSV_FILE}...")
            df = pd.read_csv(CSV_FILE)

            df['date'] = pd.to_datetime(df['date']).dt.date

            df.to_sql(SaleDB.__tablename__, con=engine, if_exists='append', index=False)
            print("Database seeding complete.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan: Startup event triggered.")
    create_db_and_seed()
    print("Lifespan: Database and seeding complete. Yielding control.")
    yield
    print("Lifespan: Shutdown event triggered.")


app = FastAPI(
    title="Sales Analytics API",
    description="API for managing sales data and running analytics.",
    version="1.0.0",
    lifespan=lifespan
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/sales/", response_model=Sale, status_code=status.HTTP_201_CREATED, summary="Add a new sale")
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = SaleDB(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@app.get("/sales/", response_model=List[Sale], summary="List all sales")
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = db.query(SaleDB).offset(skip).limit(limit).all()
    return sales


@app.get("/sales/{sale_id}", response_model=Sale, summary="Get a specific sale")
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(SaleDB).filter(SaleDB.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale


@app.put("/sales/{sale_id}", response_model=Sale, summary="Update a sale")
def update_sale(sale_id: int, sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = db.query(SaleDB).filter(SaleDB.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    for key, value in sale.model_dump().items():
        setattr(db_sale, key, value)

    db.commit()
    db.refresh(db_sale)
    return db_sale


@app.delete("/sales/{sale_id}", response_model=MessageResponse, summary="Delete a sale")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(SaleDB).filter(SaleDB.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(db_sale)
    db.commit()
    return {"detail": "Sale deleted successfully"}


@app.get("/analytics/summary", response_model=AnalyticsSummary, summary="Get sales analytics summary")
def get_analytics_summary(db: Session = Depends(get_db)):
    try:
        query = db.query(SaleDB).statement
        df = pd.read_sql(query, con=db.bind)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data for analytics: {e}")

    if df.empty:
        return {
            "total_revenue": 0,
            "total_items_sold": 0,
            "average_order_value": 0,
            "sales_by_category": {},
            "revenue_by_category": {}
        }

    df['revenue'] = df['quantity'] * df['price']

    total_revenue = round(df['revenue'].sum(), 2)
    total_items_sold = int(df['quantity'].sum())

    num_orders = len(df)
    average_order_value = round(total_revenue / num_orders, 2) if num_orders > 0 else 0

    sales_by_category = df.groupby('category')['quantity'].sum().astype(int).to_dict()
    revenue_by_category = df.groupby('category')['revenue'].sum().round(2).to_dict()

    return {
        "total_revenue": total_revenue,
        "total_items_sold": total_items_sold,
        "average_order_value": average_order_value,
        "sales_by_category": sales_by_category,
        "revenue_by_category": revenue_by_category
    }


@app.get("/analytics/plot", summary="Generate a plot for a specific sales metric")
def get_analytics_plot(
        metric: Literal[
            "total_revenue",
            "total_items_sold",
            "average_order_value",
            "sales_by_category",
            "revenue_by_category"
        ],
        db: Session = Depends(get_db)
):
    try:
        query = db.query(SaleDB).statement
        df = pd.read_sql(query, con=db.bind)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data for analytics: {e}")

    if df.empty:
        raise HTTPException(status_code=404, detail="No sales data found to plot.")

    df['date'] = pd.to_datetime(df['date'])
    df['revenue'] = df['quantity'] * df['price']
    df = df.sort_values('date')

    fig, ax = plt.subplots(figsize=(10, 6))

    if metric in ["total_revenue", "total_items_sold", "average_order_value"]:
        daily_data = df.groupby('date').agg(
            total_revenue=('revenue', 'sum'),
            total_items_sold=('quantity', 'sum'),
            total_orders=('id', 'count')
        )
        daily_data['average_order_value'] = (daily_data['total_revenue'] / daily_data['total_orders']).round(2).fillna(
            0)
        daily_data = daily_data.reset_index()

        if metric == "total_revenue":
            color = 'tab:blue'
            ax.set_xlabel("Date")
            ax.set_ylabel("Total Revenue (USD)", color=color)
            ax.plot(daily_data['date'], daily_data['total_revenue'], marker='o', linestyle='-', color=color,
                    label="Total Revenue")
            ax.tick_params(axis='y', labelcolor=color)
            plt.title("Total Revenue Over Time")

        elif metric == "total_items_sold":
            color = 'tab:green'
            ax.set_xlabel("Date")
            ax.set_ylabel("Items Sold", color=color)
            ax.plot(daily_data['date'], daily_data['total_items_sold'], marker='s', linestyle='--', color=color,
                    label="Total Items Sold")
            ax.tick_params(axis='y', labelcolor=color)
            plt.title("Total Items Sold Over Time")

        elif metric == "average_order_value":
            color = 'tab:red'
            ax.set_xlabel("Date")
            ax.set_ylabel("Average Order Value (USD)", color=color)
            ax.plot(daily_data['date'], daily_data['average_order_value'], marker='x', linestyle=':', color=color,
                    label="Average Order Value")
            ax.tick_params(axis='y', labelcolor=color)
            plt.title("Average Order Value Over Time")

        ax.legend(loc='upper left')

    elif metric in ["sales_by_category", "revenue_by_category"]:
        if metric == "sales_by_category":
            category_data = df.groupby('category')['quantity'].sum().astype(int)
            title = "Total Items Sold by Category"
            y_label = "Total Items Sold"
            color = 'tab:cyan'
        else:
            category_data = df.groupby('category')['revenue'].sum().round(2)
            title = "Total Revenue by Category"
            y_label = "Total Revenue (USD)"
            color = 'tab:purple'

        category_data.plot(kind='bar', ax=ax, color=color)
        ax.set_xlabel("Category")
        ax.set_ylabel(y_label)
        plt.title(title)
        plt.xticks(rotation=45, ha='right')

    fig.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return Response(content=buf.getvalue(), media_type="image/png")


if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    print("Access API docs at http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)

