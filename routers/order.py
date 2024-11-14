from typing import Literal, Optional
from fastapi import APIRouter
from pydantic import BaseModel
from db.sqlite import db
from db.tables import OrderData

class Condition(BaseModel):
    wid: int
    start_date: str
    end_date: str

class OrderPostBody(BaseModel):
    type: Literal['query', 'add', 'delete', 'update']
    data: Optional[OrderData] = None
    condition: Optional[Condition] = None

def conditionToSql(condition: Condition) -> str:
    sql = f"wid = {condition.wid}"
    if condition.start_date:
        sql += f" AND date >= '{condition.start_date}'"
    if condition.end_date:
        sql += f" AND date <= '{condition.end_date}'"
    return sql

router = APIRouter()

@router.get('/{wid}')
def getOrder(wid: int):
    res = db.get_order(f'wid = {wid}')
    return res if res else {}

@router.post('/crud')
def OrderCrud(body: OrderPostBody):
    res = None
    if body.type == 'query':
        sql_condition = conditionToSql(body.condition)
        res = db.get_order(sql_condition)
    elif body.type == 'add':
        res = db.add_order(body.data)
    elif body.type == 'delete':
        sql_condition = conditionToSql(body.condition)
        res = db.delete_order(sql_condition)
    elif body.type == 'update':
        res = db.update_order(body.data)
    return res
