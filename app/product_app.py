import uvicorn

from fastapi import FastAPI

app = FastAPI()

PRODUCTS = [
    {"name": "Product A", "price": 10.99, "category": "Books"},
    {"name": "Product B", "price": 5.99, "category": "Movies"},
    {"name": "Product C", "price": 7.99, "category": "Electronics"},
    {"name": "Product D", "price": 12.99, "category": "Books"},
    {"name": "Product E", "price": 8.99, "category": "Movies"},
    {"name": "Product F", "price": 15.99, "category": "Electronics"},
]


@app.get("/")
async def read_root():
    return {"name": "Product app"}


@app.get("/products")
async def read_products(category: str = None, sort_by: str = None):
    products = PRODUCTS
    if category:
        products = [p for p in products if p["category"] == category]

    if sort_by:
        products = sorted(products, key=lambda p: p[sort_by])

    return {"products": products}


if __name__ == "__main__":
    uvicorn.run("product_app:app", reload=True, port=5002)
