from typing import List
import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Microsoft YaHei' # 找个本机系统支持的字体
matplotlib.use('Agg')
def revenueChartBuf(income: List[float], expense: List[float], date: List[str]):
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建一个新的图形和轴
    # x轴数据（假设长度相同）
    x = np.arange(len(income))
    # 绘制折线图和柱状图
    ax.plot(x, income, label="Income 收入", color="green", marker="o")
    ax.bar(x, expense, label="Expense 支出", color="orange", alpha=0.6)
    # 设置 x 轴标签为日期
    ax.set_xticks(x)
    ax.set_xticklabels(date, rotation=45, ha="right")  # 日期标签倾斜45度方便显示
    # 设置轴标签和单位
    ax.set_xlabel("Date 日期", fontsize=12)
    ax.set_ylabel("单位 元", fontsize=12)
    ax.set_title("收支表", fontsize=14)
    # 添加图例
    ax.legend()
    # 保存到内存字节流中
    revenueBuf = io.BytesIO()
    fig.savefig(revenueBuf, format="png")
    revenueBuf.seek(0)
    plt.close(fig)
    return revenueBuf

def profitChartBuf(income: List[float], expense: List[float], date: List[str]):
    fig, ax = plt.subplots(figsize=(10, 6))  # 创建一个新的图形和轴
    # x轴数据（假设长度相同）
    x = np.arange(len(income))
    # 绘制折线图和柱状图
    ax.plot(x, np.array(income) - np.array(expense), label="Income 收入", color="green", marker="o")
    # 设置 x 轴标签为日期
    ax.set_xticks(x)
    ax.set_xticklabels(date, rotation=45, ha="right")  # 日期标签倾斜45度方便显示
    # 设置轴标签和单位
    ax.set_xlabel("Date 日期", fontsize=12)
    ax.set_ylabel("单位 元", fontsize=12)
    ax.set_title("利润表", fontsize=14)
    # 添加图例
    ax.legend()
    profitBuf = io.BytesIO()
    fig.savefig(profitBuf, format="png")
    profitBuf.seek(0)
    plt.close(fig)
    return profitBuf