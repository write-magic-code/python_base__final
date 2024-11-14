import random
import string
from datetime import datetime, timedelta
from db.sqlite import db
from db.tables import WarehouseData, OrderData
from typing import List

PRICE_LEVEL = 5
SITE_COUNT = 100


phone_prefixs = ["139", "134", "189", "150", "138", "144", "135"]
# 区、街和号的中文列表
districts = ["高新区", "经开区", "主城区", "下城区", "廉政区", "教育园区", "新工业区"]
streets = ["解放路", "建国路", "跃进路", "文革路", "开放路", "工人路"]
house_numbers = [str(random.randint(1, 100)) for _ in range(1, 101)]  # 随机生成1到100的门牌号

generated_names = set()

def rand_name():
    warehouse_suffixes = [
        "仓库", "物流中心", "配送中心", "储运站", "储备库", "仓储基地", 
        "智能仓储", "货运中心", "库存管理中心", "物流园区", "冷链仓库", 
        "快速配送中心", "国际物流中心", "自动化仓库", "综合物流中心"
    ]
    
    while True:
        # 随机选择仓库名称前缀和后缀
        prefix = random.choice(districts)
        suffix = random.choice(warehouse_suffixes)
        
        # 拼接仓库名称
        name = f"{prefix}{suffix}"
        
        # 如果这个名称已经生成过，继续循环生成新的名称
        if name not in generated_names:
            generated_names.add(name)  # 将生成的仓库名称添加到集合中
            return name
# 生成随机日期
def random_date(start_date: datetime, end_date: datetime) -> str:
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d') # 字典序可比较

# 生成随机浮动价格，价格浮动范围为10到100
def random_price(count) -> List[float]:
    return [round(random.uniform(10, 100), 2) for _ in range(count)]

# 订单数据
def random_order(wid: int, order_id: int) -> OrderData:
    transport_volume = [[random.randint(1, 10) for _ in range(SITE_COUNT)] for _ in range(PRICE_LEVEL)]  # 假设有3个地区
    selling_volume = [random.randint(1, 100) for _ in range(PRICE_LEVEL)]  # 假设有5个商品
    date = random_date(datetime(2042, 1, 1), datetime(2044, 1, 1))
    return OrderData(
        order_id=order_id,  # 提供一个唯一的 order_id
        wid=wid,
        date=date,
        transport_volume=transport_volume,
        selling_volume=selling_volume)

# 生成随机地址
def random_address() -> str:
    district = random.choice(districts)
    street = random.choice(streets)
    house_number = random.choice(house_numbers)
    return f"{district}{street}{house_number}号"

# 生成随机电话
def random_phone() -> str:
    return random.choice(phone_prefixs) + str(random.randint(100000000, 999999999))

# 向数据库插入100条仓库数据
def db_mock():
    order_id = 1  # 设置订单ID的初始值
    for i in range(1, SITE_COUNT + 1):  # 生成100条仓库数据
        name = rand_name()
        tel = random_phone()  # 使用随机生成的电话
        address = random_address()  # 使用随机生成的中文地址

        # 生成浮动的售价和运输价格
        selling_price = random_price(PRICE_LEVEL)  # 返回浮动价格列表
        transport_price = [random_price(SITE_COUNT) for _ in range(PRICE_LEVEL)]  # 假设有3个地区的运输价格

        # 创建仓库数据并添加到数据库
        warehouse = WarehouseData(
            wid=i,  # 这里使用唯一的仓库ID
            name=name,
            tel=tel,
            address=address,
            selling_price=selling_price,
            transport_price=transport_price)
        
        db.add_warehouse(warehouse)  # 向数据库插入仓库数据

        # 批量生成并插入20条订单数据
        orders = []
        for _ in range(1, 21):  # 每个仓库生成20个订单
            order = random_order(i, order_id)  # 传递递增的 order_id
            orders.append(order)
            order_id += 1  # 每次生成一个订单后，递增 order_id

        # 批量插入订单数据
        for order in orders:
            db.add_order(order)

# 开始插入数据
db_mock()