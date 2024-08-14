import os
import uvicorn
import requests

from fastapi import FastAPI

app = FastAPI()

PRODUCTS_SERVICE_HOST_VALUE = "http://127.0.0.1:5002"


@app.get("/")
async def read_root():
    return {"name": "Shop app"}


@app.get("/shop")
async def read_products(category: str = "", sort_by: str = ""):
    PRODUCTS_SERVICE_HOST = os.environ.get(
        "PRODUCTS_SERVICE_HOST", PRODUCTS_SERVICE_HOST_VALUE
    )

    PRODUCTS_URL = f"{PRODUCTS_SERVICE_HOST}/products"

    params = {}
    if category != "":
        params["category"] = category
    if sort_by != "":
        params["sort_by"] = sort_by

    products_resp = requests.get(PRODUCTS_URL, params=params)
    if products_resp.status_code < 300:
        return {"products": products_resp.json()}
    else:
        return {
            "error": True,
            "error_message": products_resp.content,
            "error_status": products_resp.status_code,
        }


if __name__ == "__main__":
    uvicorn.run("shop_app:app", reload=True, port=5001)
