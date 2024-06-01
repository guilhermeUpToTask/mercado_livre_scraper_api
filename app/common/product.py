from pydantic import BaseModel

class Product(BaseModel):
    id:int
    name: str
    url: str
    price: float
    rating_number: float
    rating_amount: int


class ProductPrice(BaseModel):
    product_id: int
    price: float
    price_date: str
