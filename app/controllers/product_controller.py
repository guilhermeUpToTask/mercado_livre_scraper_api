from typing import Union
from fastapi import APIRouter, HTTPException
from app.models.products_model import ProductModel
from app.common.product import Product, ProductPrice

router = APIRouter()

@router.get("/products",)
async def get_products() -> Union[list[Product],None]:
    try:
        product_model = ProductModel()
        products = product_model.get_all_products()
        return products
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f'Internal Server Error from product Controler... ')
        print(f"{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        product_model.close_connection()


@router.get("/products/{id}")
async def get_product(id: int) -> Union[Product, None]:
    try:
        product_model = ProductModel()
        product = product_model.get_product_by_id(id)
        return product
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print(f'Internal Server Error from product Controler... ')
        print(f"{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        product_model.close_connection()


@router.get("/products/{id}/price_history")
async def get_product_prices(id: int) -> Union[list[ProductPrice], None]:
    try:
        product_model = ProductModel()
        prices = product_model.get_prices_by_product_id(id)
        return prices
    
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f'Internal Server Error from product Controler... ')
        print(f"{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        product_model.close_connection()


@router.get("/products/page/{page}/size/{size}")
async def get_products_page(page: int, size: int) -> Union[list[Product], None]:
    try:
        product_model = ProductModel()
        products = product_model.get_products_by_page(page, size)
        return products

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f'Internal Server Error from product Controler... ')
        print(f"{str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        product_model.close_connection()
