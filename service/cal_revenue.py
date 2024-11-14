import numpy as np
from typing import List, Union
from db.tables import WarehouseData, OrderData

def calOrderIncome(warehouse: WarehouseData, oder: Union[OrderData, List[OrderData]]) -> Union[float, List[float]]:
    if isinstance(oder, OrderData):
        income = np.sum(np.array(oder.selling_volume) * np.array(warehouse.selling_price))
    elif isinstance(oder, list):
        income = []
        for o in oder:
            income.append(np.sum(np.array(o.selling_volume) * np.array(warehouse.selling_price)))
    else :
        raise TypeError("oder should be OrderData or List[OrderData]")
    return income

def calOrderExpenses(warehouse: WarehouseData, oder: Union[OrderData, List[OrderData]]):
    if isinstance(oder, OrderData):
        expenses = np.sum(np.ndarray(oder.transport_volume) * np.ndarray(warehouse.transport_price))
    elif isinstance(oder, list):
        expenses = []
        for o in oder:
            expenses.append(np.sum(np.array(o.transport_volume) * np.array(warehouse.transport_price)))
    else :
        raise TypeError("oder should be OrderData or List[OrderData]")
    return expenses
