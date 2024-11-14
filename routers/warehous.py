from typing import Literal, Optional

from service.cal_revenue import calOrderIncome, calOrderExpenses
from service.draw_chart import revenueChartBuf, profitChartBuf
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from db.sqlite import db
from db.tables import WarehouseData

class Condition(BaseModel):
    name: Optional[str]
    tel: Optional[str]
    address: Optional[str]

class WarehousePostBody(BaseModel):
    type: Literal['query', 'add', 'delete', 'update']
    condition: Optional[Condition]
    data: Optional[WarehouseData]

class WarehouseStatisticsBody(BaseModel):
    start_date: str
    end_date: str

def conditionToSql(condition: Condition) -> str:
    sql = ''
    if condition.name:
        sql += f"name = '{condition.name}'"
    if condition.tel:
        if sql != '':
            sql += " AND "
        sql += f"tel = '{condition.tel}'"
    if condition.address:
        if sql != '':
            sql += " AND "
        sql += f"address = '{condition.address}'"
    return sql

router = APIRouter()

@router.get('/{wid}')
def GetWarehouse(wid: int):
    res = db.get_warehouse(f'wid = {wid}')
    return res[0] if res else {}

@router.post('/crud')
def WarehouseCrud(body: WarehousePostBody):
    res = None
    if body.type == 'query':
        sql_condition = conditionToSql(body.condition)
        res = db.get_warehouse(sql_condition)
    elif body.type == 'add':
        res = db.add_warehouse(body.data)
    elif body.type == 'delete':
        sql_condition = conditionToSql(body.condition)
        res = db.delete_warehouse(sql_condition)
    elif body.type == 'update':
        res = db.update_warehouse(body.data)
    return res

@router.post('/statistics/{wid}')
def WarehouseStatistics(wid: int, body: WarehouseStatisticsBody):
    w = db.get_warehouse(f'wid = {wid}')
    if not w:
        return {"error": "wid not found"}
    w = w[0]
    orders = db.get_order(
        f"date >= '{body.start_date}' AND date <= '{body.end_date}' AND wid = {wid}"
    )
    income = calOrderIncome(w, orders)
    expenses = calOrderExpenses(w, orders)
    return { 
        "income": sum(income),
        "expenses": sum(expenses),
    }

@router.post('/chart/revenue/{wid}')
def WarehouseRevenueChart(wid: int, body: WarehouseStatisticsBody):
    w = db.get_warehouse(f'wid = {wid}')
    if not w:
        return {"error": "wid not found"}
    w = w[0]
    orders = db.get_order(
        f"date >= '{body.start_date}' AND date <= '{body.end_date}' AND wid = {wid}"
    )
    income = calOrderIncome(w, orders)
    expenses = calOrderExpenses(w, orders)
    revenueBuf = revenueChartBuf(income, expenses, [order.date for order in orders])
    return StreamingResponse(revenueBuf, media_type="image/png")

@router.post('/chart/profit/{wid}')
def WarehouseProfitChart(wid: int, body: WarehouseStatisticsBody):
    w = db.get_warehouse(f'wid = {wid}')
    if not w:
        return {"error": "wid not found"}
    w = w[0]
    orders = db.get_order(
        f"date >= '{body.start_date}' AND date <= '{body.end_date}' AND wid = {wid}"
    )
    income = calOrderIncome(w, orders)
    expenses = calOrderExpenses(w, orders)
    ProfitBuf = profitChartBuf(income, expenses, [order.date for order in orders])
    return StreamingResponse(ProfitBuf, media_type="image/png")