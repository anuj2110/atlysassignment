from pydantic import BaseModel

class JsonEntity(BaseModel):
    path_to_image:str
    prodcut_title:str
    product_price:float