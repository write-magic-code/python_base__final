from typing import List

from pydantic import BaseModel
# BaseModel 是 FastAPI 要这么干的，方便路由验证类型时处理

class WarehouseData(BaseModel):
    wid: int
    name: str
    tel: str
    address: str
    selling_price: List[float]
    transport_price: List[List[float]]

class OrderData(BaseModel):
    order_id: int
    wid: int
    date: str
    transport_volume: List[List[int]]
    selling_volume: List[int]