# Kaishek 凯申物流
每个网点的业务有：
- 运输货物：指将不属于本站的货物运送到其它站点
- 销售货物：指将本站货物卖给顾客

对于一家站点所有的发货、销售行为，其收入支出都自行负担、方便管理。（如：A 向 B 发货，同时 A 销售。为方便管理，A 承担所有成本与收益）

货物分为 5 个等级：5kg、10kg、15kg、20kg、25kg。同等级货物在价格上视为一类。

## Data Definition 数据定义

### Warehouse 仓库数据
- **wid int**: warehouse id 仓库 id, unique identifier
- **name string**: 仓库名
- **tel string**: 电话
- **address string**: 地址
- **selling_price [float]**: 各等级货物的单价
- **transport_price [[float]]**: 各等级货物运送到各网点的单价。对于该矩阵 $T[i][j]$ 表示 $i$ 级货物，送至 $j$ 网点的单价。
  -  [[1级: to A, to B, to C,...],
  -  [2级: to A, to B, to C,...],
  -  [3级: to A, to B, to C,...],...]

### Oder 订单数据
- **oder_id int**: 订单 id, unique identifier
- **wid int**: refer
- **date string**: 日期
- **transport_volume [[int]]**: 各等级货物，送至各网点的运输量。对于该矩阵 $T[i][j]$ 表示 $i$ 级货物，送至 $j$ 网点的运输量。
  - [[1级: to A, to B, to C,...],
  -  [2级: to A, to B, to C,...],
  -  [3级: to A, to B, to C,...],...]
- **selling_volume [int]**: 各等级货物销售量

## API
### 1. /warehouse

#### 1.1 GET /warehouses/{wid}
获取仓库信息

#### 1.2 POST /warehouses
按条件增删查改仓库
* body 类型
```ts
body: {
    type: "query" | "add" | "delete" | "update",
    
    condition: {
        name?: string,
        tel?: string,
        address?: string,
    } | data: {
        name: string,
        tel: string,
        address: string,
        selling_price: [float],
        transport_price: [[float]],
    }
}
```
`type`字段用于表示：该项目中，对本次请求类型的定义
- `query`、`delete`：使用 `conditon` 字段，返回 `Warehouse[]`
- `add`、`update`：使用 `data` 字段，返回 `int`（sqlite cursor 的操作信息，并不多）

* 返回：
```ts
Warehouse[] | int
```

#### 1.3 POST /warehouses/statistics/{wid}
按条件查询仓库统计信息
* body 类型
```ts
body: {
    start_date?: string,
    end_date?: string,
}
```
返回该时间段内，该仓库收入与支出的统计数字。
* 返回：
```ts
{
    income: float,
    expenses: float,
}
```

#### 1.4 POST /chart/revenue/{wid}
按条件绘制仓库收支图表
* body 类型
```ts
body: {
    start_date: string,
    end_date: string,
}
```
* 返回：
```ts
Stream Response of Chart in png
```

#### 1.5 POST /chart/profit/{wid}
按条件绘制仓库利润图表
* body 类型
```ts
body: {
    start_date: string,
    end_date: string,
}
```
* 返回：
```ts
Stream Response of Chart in png
```
---

### 2. /order

#### 2.1 GET /orders/{wid}
获取订单信息
* 返回：
```ts
Oder
```

#### 2.2 POST /orders
按条件查询订单
* body 类型
```ts
body: {
    type: "query" | "add" | "delete" | "update",
    condition:{
        wid!: int,
        start_date?: string,
        end_date?: string,
    } | data: {
        wid: int,
        date: string,
        transport_volume: [[int]],
        selling_volume: [int],
    }
}
```
`type`字段用于表示：该项目中，对本次请求类型的定义
- `query`、`delete`：使用 `conditon` 字段，返回 `Oder[]`
- `add`、`update`：使用 `data` 字段，返回 `int`（sqlite cursor 的操作信息，并不多）
```ts
Oder[] | int
```

## Tips 提示

### 开发前
* 不方便发送请求测试？用 fastapi 的交互式请求文档——他们在官网首页就有介绍。
* 如果没有把握，最好像搭积木一样，每完成一个小功能就及时测试——学习阶段手动测试不要让未掌握的代码积累过多。
  * 抓不出问题，是不是你没有输出查错与看 Error 的习惯？
  * 有些问题会在进入（后端）服务器前发生，有些则会发生在服务器内（Internal Server Error），有些则会被服务器处理抛出状态码（如 404）。你并不总能在 **服务器终端/客户端（前端、发包者）** 看到完整报错信息。
* sqlite 默认是同步数据库，不需要你使用异步（`async`/`await`）写法。正常按同步写法编写即可。
* 不知道从哪下手？那就先为自己的项目搭建方便的 crud 吧。

### 开发中
* 如果数据库脏了，删掉就好。只要不是特别有用的数据，开发阶段随机塞进去的数据都不值钱——我们一般把测试用假数据叫 mock。
  * sqlite 基于文件系统实现，因此删除方法和文件删除相同。
* 用 matplotlib 绘制图表时，记得 utf-8 问题。
* 用 numpy 计算时，记得使用一般的矩阵乘法（对应位置相乘），而不是`dot()`或`@`点乘。
  * 注意 python 原生类型中的 `list` 和 numpy 中的 `ndarray`，结构一样，但支持的行为不同。
* 在你写好一些基础功能后，再考虑逐渐往 fastapi 框架中搭建。
  * fastapi 中的类型系统不够强大，因此不要使用它的`Union[]`类型标注，理由是：*fastapi 会在运行时会拦截 Union 中除首个类型之外的所有类型，因为 fastapi 表面上实现了 Union 的定义，但在运行时没有将所有可能类型都检查一次。fastapi 的逻辑是直接将请求中的数据扔进首个类型的构造函数，导致一旦不符合 Union 中的首个类型，他就会报错，而不是尝试下一个类型。* **但在其他语言中，你根本不会为此受罪。**
  * 因为整个项目很简单，没有异步操作（sqlite），这次你可以不理会 llm 对于 fastapi 项目 `async`/`await` 的建议。
* 如果你想像示例代码一样，用 class 类型来约束数据（**而不是把数据从 db 中取出来以变量的形式漫天乱飞**），使得自己的代码更加可读，记得多查资料，多请教，多看各文件/模块间的关系。因为：
  * pydantic 对初学者不太简单，比如`BaseModel`有一些对于构造函数、运行时检查等行为，也许以你目前的知识并无法全部理解。
  * **你很有可能用有限的想象力把简单的事情办的异常复杂，最后代码烂掉。**
### 完成后
无论你做得怎么样，实现了多少功能，调试运行是否成功已经不重要了，毕竟你没有真的被**凯申物流公司**雇佣。整个项目，从系列课程为你设计需求开始，以你独立完成项目的构思结束。

事实上，除了从“自然语言”翻译到“需求文档”，再产生“项目文档”（这些依赖社会经验和行业经验）之外，你使用 python 干了一件相当了不起的事情：扮演后端架构师/组长，在没有同事的情况下完成了它。尽管它离真实的商业化开发还有一段距离，但你已经能想象公司里的后端项目组会有什么流程了。

同时我们希望你发现 python 的局限性，以及优点。当你真正有底气批评一项技术时，必然是你经历过这样的场面后：你使用这项技术的诸多特性，去解决特定问题，但遇到了许多限制。这些限制是技术设计注定无法绕开这一类问题的——**因此目前为止，没有最厉害的技术，只有最合适，最针对某类问题的技术。**

最核心的从来不是语言，也不仅仅是框架。如这次项目所演示的那样：你使用着不同的 python 模块，将它们更好的组合。这绝非将两个功能写进一个项目这么无脑！在初学时，你会碰到**重复代码、依赖混乱、无结构的散乱、无法维护只好重构项目**等问题。如果你希望这个项目成长为一个庞大的、可商用的项目，**一个科学、稳建的核心架构，才能支撑庞大的四肢**——这点相信你体会到了。

因此非要说，开发的核心是什么，我想仍是前两次工业时代的延续——**工业结构与组装的艺术**。教框架，仅仅是我们认为它更好展现这种技艺，让你看到不同技术路线的取舍，思想之争。

不管你是否投身 it 工业，你都应该了解这些。如果你励志做学术，这些最基础必要的开发知识会帮助你鹤立鸡群，成为合格的工业时代人口；如果你希望从事开发，这才刚入门而已——但，已经可以再练练就去找工作，成为螺丝钉了。