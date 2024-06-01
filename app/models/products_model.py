from pydantic import BaseModel
from typing import Union, List
from app.common.product import Product, ProductPrice, ProductPrice
from app.common.db_credentials import db_uri
from os import path
from fastapi import HTTPException
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi


class ProductModel:

    def __init__(self):
        print("Initializing database connection...")
        print(db_uri)
        self.client = None
        self.db = None
        try:
            self.client = MongoClient(str(db_uri), server_api=ServerApi('1'))
            self.db = self.client.mercado_livre

        except errors.ConnectionFailure as e:
            print(f"Error connecting to MongoDB: {e}")

    def close_connection(self):
        try:
            if self.client:
                self.client.close()
            print("Database connection closed.")
        except errors.ConnectionFailure as e:
            print(f"Error closing database connection: {e}")

    def get_all_products(self) -> Union[List[Product], None]:
        try:
            products = list(self.db.products.find())
            print('porudcts:', products)
            if products:
                return [
                    Product(id=str(product['_id']),
                            name=product['name'],
                            url=product['url'],
                            price=product['price'],
                            rating_number=product['rating_number'],
                            rating_amount=product['rating_amount'])
                    for product in products
                ]
            else:
                print(f"No products found.")
                raise HTTPException(
                    status_code=404, detail="No products found")

        except errors.PyMongoError as e:
            print(f"Error getting products: {e}")
            raise HTTPException(
                status_code=500, detail='Database Internal Server Error')

    def get_product_by_id(self, id: int) -> Union[Product, None]:
        try:
            product = self.db.products.find_one({"_id": id})
            product = self.cursor.fetchone()
            if product:
                return Product(
                    id=product['_id'],
                    name=product['name'],
                    url=product['url'],
                    price=product['price'],
                    rating_number=product['rating_number'],
                    rating_amount=product['rating_amount']
                )
            else:
                print(f"Product with id {id} not found.")
                raise HTTPException(
                    status_code=404, detail="Product not found")

        except errors.PyMongoError as e:
            print(f"Error getting product by id: {e}")
            raise HTTPException(
                status_code=500, detail='Database Internal Server Error')

    def get_prices_by_product_id(self, product_id: int) -> Union[list[ProductPrice], None]:
        try:
            prices = list(self.db.product_prices.find(
                {"product_id": product_id}))
            if prices:
                print('prices:', prices)
                return [
                    ProductPrice(id=price['_id'],
                                 product_id=str(price['product_id']),
                                 price=price['price'],
                                 price_date=price['price_date'].strftime("%Y-%m-%d %H:%M:%S"))
                    for price in prices
                ]
            else:
                raise HTTPException(
                    status_code=404, detail="Prices not found for product")

        except errors.PyMongoError as e:
            print(f"Error getting prices by product id: {e}")
            raise HTTPException(
                status_code=500, detail='Database Internal Server Error')

    def get_products_size(self) -> Union[int, None]:
        try:
            products_size = self.db.products.count_documents({})
            return products_size

        except errors.PyMongoError as e:
            print(f"Error getting rows size: {e}")
            raise HTTPException(
                status_code=500, detail='Database Internal Server Error')

    def get_products_by_page(self, page: int, page_size: int) -> Union[List[Product], None]:
        try:
            start = (page - 1) * page_size
            products = list(self.db.products.find().skip(
                start).limit(page_size))
            if products:
                return [
                    Product(id=str(product['_id']),
                            name=product['name'],
                            url=product['url'],
                            price=product['price'],
                            rating_number=product['rating_number'],
                            rating_amount=product['rating_amount'])
                    for product in products
                ]
            else:
                print(f"No products found.")
                raise HTTPException(
                    status_code=404, detail="No products found")

        except errors.PyMongoError as e:
            print(f"Error getting products by page: {e}")
            raise HTTPException(
                status_code=500, detail='Database Internal Server Error')
