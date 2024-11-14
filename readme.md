# Kaishek 凯申物流

码奇码 Python Base 系列课程的 Final 项目

## 项目结构
- db：数据库相关，包括
  - tables 数据定义
  - sqlite 数据库行为封装
- public: 免费赠送的前端，方便组合成完整前后端项目
- routes: 路由相关，包括
  - order 订单路由
  - warehouse 仓库路由
- service: 后端服务，包括
  - cal_revenue 计算营业额相关
  - draw_chart 绘制图表
- data_gen 生成测试用数据
- local_run 本地启动整个后端项目
- requirements.txt 依赖包列表

## 设计稿
- design.md

请参照该文档进行施工

# Usage 运行
* 创建虚拟环境：
```sh
py -m venv venv
```
* 启动虚拟环境：
```sh
./venv/Scripts/activate
```
or
```sh
source venv/bin/activate
```
* 安装依赖包：
```sh
pip install -r requirements.txt
```
* 本地启动项目：
```sh
py local_run.py
```

本项目仅供学习参考，请勿用于商业用途。要知道傻子是不会买这种东西的。