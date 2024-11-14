import sqlite3
import json
import os
from .tables import WarehouseData, OrderData
from typing import List

class DB:
    def __init__(self):
        # 如果数据库不存在，则创建数据库
        if not os.path.exists('warehouse.db'):
            with open('warehouse.db', 'w'):
                pass

        self.conn = sqlite3.connect('warehouse.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS warehouse_data (
                wid INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tel TEXT NOT NULL,
                address TEXT NOT NULL,
                selling_price TEXT NOT NULL,
                transport_price TEXT NOT NULL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_data (
                order_id INTEGER PRIMARY KEY,
                wid INTEGER NOT NULL,
                date TEXT NOT NULL,
                transport_volume TEXT NOT NULL,
                selling_volume TEXT NOT NULL,
                FOREIGN KEY (wid) REFERENCES warehouse_data(wid)
            );
        ''')
        self.conn.commit()

    def add_warehouse(self, warehouse: WarehouseData) -> int:
        self.cursor.execute('INSERT INTO warehouse_data (wid, name, tel, address, selling_price, transport_price) VALUES (?, ?, ?, ?, ?, ?)', 
                (warehouse.wid, warehouse.name, warehouse.tel, warehouse.address, json.dumps(warehouse.selling_price), json.dumps(warehouse.transport_price)))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_warehouse(self, condition: str) -> List[WarehouseData]:
        self.cursor.execute(f'SELECT * FROM warehouse_data WHERE {condition}')
        rows = self.cursor.fetchall()
        result: List[WarehouseData] = []
        for row in rows:
            result.append(WarehouseData(
                wid = row[0],
                name = row[1],
                tel = row[2],
                address = row[3],
                selling_price = json.loads(row[4]),
                transport_price = json.loads(row[5]),
            ))
        return result

    def update_warehouse(self, warehouse: WarehouseData) -> int:
        self.cursor.execute('UPDATE warehouse_data SET name = ?, tel = ?, address = ?, selling_price = ?, transport_price = ? WHERE wid = ?', (warehouse.name, warehouse.tel, warehouse.address, json.dumps(warehouse.selling_price), json.dumps(warehouse.transport_price), warehouse.wid))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_warehouse(self, condition: str) -> int:
        self.cursor.execute(f'DELETE FROM warehouse_data WHERE {condition}')
        self.conn.commit()
        return self.cursor.rowcount

    def add_order(self, order: OrderData) -> int:
        self.cursor.execute('INSERT INTO order_data (order_id, wid, date, transport_volume, selling_volume) VALUES (?, ?, ?, ?, ?)', (order.order_id, order.wid, order.date, json.dumps(order.transport_volume), json.dumps(order.selling_volume)))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_order(self, condition: str) -> List[OrderData]:
        self.cursor.execute(f'SELECT * FROM order_data WHERE {condition}')
        rows = self.cursor.fetchall()
        result: List[OrderData] = []
        for row in rows:
            result.append(OrderData(
                order_id = row[0],
                wid = row[1],
                date = row[2],
                transport_volume = json.loads(row[3]),
                selling_volume = json.loads(row[4])
            ))
        return result

    def update_order(self, order: OrderData) -> int:
        self.cursor.execute('UPDATE order_data SET wid = ?, date = ?, transport_volume = ?, selling_volume = ? WHERE order_id = ?', (order.wid, order.date, json.dumps(order.transport_volume), json.dumps(order.selling_volume), order.order_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_order(self, condition: str) -> int:
        self.cursor.execute(f'DELETE FROM order_data WHERE {condition}')
        self.conn.commit()
        return self.cursor.rowcount

db = DB()