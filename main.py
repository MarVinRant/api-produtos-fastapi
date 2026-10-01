from __future__ import annotations

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    produto: str
    categoria: str
    preco: float = Field(ge=0)
    quantidade_vendida: int = Field(ge=0)


class ProductCreate(BaseModel):
    produto: str = Field(min_length=2)
    categoria: str = Field(min_length=2)
    preco: float = Field(ge=0)
    quantidade_vendida: int = Field(ge=0)


app = FastAPI(title="API de Produtos", version="1.0.0")
products: list[Product] = [
    Product(id=1, produto="Notebook Pro", categoria="Informática", preco=4599.90, quantidade_vendida=12),
    Product(id=2, produto="Mouse sem Fio", categoria="Informática", preco=89.90, quantidade_vendida=85),
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/produtos", response_model=list[Product])
def list_products(categoria: Annotated[str | None, Query()] = None) -> list[Product]:
    if not categoria:
        return products
    return [item for item in products if item.categoria.lower() == categoria.lower()]


@app.get("/produtos/filtro/preco", response_model=list[Product])
def products_by_max_price(max_price: float = Query(gt=0)) -> list[Product]:
    return [item for item in products if item.preco <= max_price]


@app.get("/produtos/{product_id}", response_model=Product)
def get_product(product_id: int) -> Product:
    for item in products:
        if item.id == product_id:
            return item
    raise HTTPException(status_code=404, detail="Produto não encontrado")


@app.post("/produtos", response_model=Product, status_code=201)
def create_product(payload: ProductCreate) -> Product:
    new_product = Product(id=max((item.id for item in products), default=0) + 1, **payload.model_dump())
    products.append(new_product)
    return new_product


@app.delete("/produtos/{product_id}", status_code=204)
def delete_product(product_id: int) -> None:
    for index, item in enumerate(products):
        if item.id == product_id:
            products.pop(index)
            return
    raise HTTPException(status_code=404, detail="Produto não encontrado")

