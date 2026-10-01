import pytest
from fastapi import HTTPException

from main import get_product, health, list_products, products_by_max_price


def test_health_endpoint_function():
    assert health() == {"status": "ok"}


def test_list_products_can_filter_by_category():
    result = list_products("informática")
    assert result
    assert all(item.categoria == "Informática" for item in result)


def test_get_product_returns_known_product():
    assert get_product(1).produto == "Notebook Pro"


def test_filter_by_max_price():
    result = products_by_max_price(100)
    assert result
    assert all(item.preco <= 100 for item in result)


def test_missing_product_returns_404():
    with pytest.raises(HTTPException) as error:
        get_product(99999)
    assert error.value.status_code == 404

