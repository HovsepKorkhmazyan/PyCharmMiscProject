from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()



class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, description="User name (required)")
    email: EmailStr = Field(..., description="User email address (required, valid email format)")
    age: Optional[int] = Field(None, gt=0, description="User age (optional, must be positive)")
    is_subscribed: Optional[bool] = Field(None, description="Newsletter subscription flag (optional)")



@app.post("/create_user")
async def create_user(user: UserCreate):


    return {
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "is_subscribed": user.is_subscribed
    }


from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
    "product_id": 456,
    "name": "Phone Case",
    "category": "Accessories",
    "price": 19.99
}

sample_product_3 = {
    "product_id": 789,
    "name": "iPhone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]


@app.get("/products/search")
async def search_products(keyword: str, category: Optional[str] = None, limit: int = 10):
    results = []

    for product in sample_products:
        keyword_match = keyword.lower() in product["name"].lower()
        category_match = category is None or product["category"].lower() == category.lower()

        if keyword_match and category_match:
            results.append(product)

    return results[:limit]


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")



