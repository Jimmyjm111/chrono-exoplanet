"""
==============================================================================
数据生成模块 (data_generator.py)
==============================================================================

【学习目标】
本模块帮助你学习Python的循环和随机数生成：
1. for循环和while循环
2. range()函数的使用
3. random模块的各种方法
4. 列表的操作（添加、遍历）
5. 综合运用类和函数

【业务背景】
在实际项目中，我们需要测试数据来验证系统功能
这个模块会生成模拟的跨境支付交易数据

==============================================================================
"""

import random
from datetime import datetime, timedelta
from typing import List, Optional

# 导入我们自己写的模块
from _01_config import (
    SUPPORTED_CURRENCIES,
    PAYMENT_CHANNELS,
    AMOUNT_RANGES,
    EXCHANGE_RATES,
    DEFAULT_TRANSACTION_COUNT,
)
from _05_models import Transaction, create_channel_from_config


# ==============================================================================
# 第一部分：random模块基础
# ==============================================================================

def demonstrate_random_basics():
    """
    演示random模块的基本用法
    
    【random模块常用函数】
    - random.random(): 返回0-1之间的随机浮点数
    - random.randint(a, b): 返回a-b之间的随机整数（包含a和b）
    - random.uniform(a, b): 返回a-b之间的随机浮点数
    - random.choice(seq): 从序列中随机选择一个元素
    - random.choices(seq, k=n): 从序列中随机选择n个元素（可重复）
    - random.sample(seq, k=n): 从序列中随机选择n个不重复的元素
    - random.shuffle(list): 打乱列表顺序（原地修改）
    """
    print("【random模块演示】")
    
    # random(): 0-1之间的随机浮点数
    print(f"random.random(): {random.random():.4f}")
    
    # randint: 随机整数，包含两端
    print(f"random.randint(1, 100): {random.randint(1, 100)}")
    
    # uniform: 随机浮点数
    print(f"random.uniform(10.0, 20.0): {random.uniform(10.0, 20.0):.2f}")
    
    # choice: 从列表中随机选一个
    currencies = ["USD", "EUR", "GBP"]
    print(f"random.choice({currencies}): {random.choice(currencies)}")
    
    # choices: 随机选择多个（可重复）
    print(f"random.choices({currencies}, k=5): {random.choices(currencies, k=5)}")
    
    # sample: 随机选择多个（不重复）
    print(f"random.sample({currencies}, k=2): {random.sample(currencies, k=2)}")


# ==============================================================================
# 第二部分：for循环详解
# ==============================================================================

def demonstrate_for_loops():
    """
    演示for循环的各种用法
    
    【for循环语法】
    for 变量 in 可迭代对象:
        循环体
    
    【可迭代对象】
    - 列表(list)
    - 字符串(str)
    - 字典(dict)
    - range对象
    - 其他可迭代类型
    """
    print("\n【for循环演示】")
    
    # 1. 遍历列表
    print("\n1. 遍历列表:")
    currencies = ["USD", "EUR", "GBP"]
    for currency in currencies:
        print(f"  货币: {currency}")
    
    # 2. 使用range()
    # range(n): 生成0到n-1的序列
    # range(start, stop): 生成start到stop-1的序列
    # range(start, stop, step): 带步长的序列
    print("\n2. 使用range():")
    print("  range(5):", end=" ")
    for i in range(5):
        print(i, end=" ")
    print()
    
    print("  range(1, 6):", end=" ")
    for i in range(1, 6):
        print(i, end=" ")
    print()
    
    print("  range(0, 10, 2):", end=" ")
    for i in range(0, 10, 2):  # 步长为2
        print(i, end=" ")
    print()
    
    # 3. enumerate(): 同时获取索引和值
    print("\n3. enumerate()获取索引:")
    for index, currency in enumerate(currencies):
        print(f"  索引{index}: {currency}")
    
    # 4. 遍历字典
    print("\n4. 遍历字典:")
    rates = {"USD": 7.25, "EUR": 7.85}
    
    # 只遍历键
    print("  只遍历键:")
    for key in rates:
        print(f"    {key}")
    
    # 遍历键和值
    print("  遍历键和值:")
    for key, value in rates.items():
        print(f"    {key}: {value}")
    
    # 5. 列表推导式（简洁的循环写法）
    print("\n5. 列表推导式:")
    # 传统写法
    squares = []
    for i in range(5):
        squares.append(i ** 2)
    print(f"  传统写法: {squares}")
    
    # 列表推导式
    squares_comprehension = [i ** 2 for i in range(5)]
    print(f"  列表推导式: {squares_comprehension}")
    
    # 带条件的列表推导式
    even_squares = [i ** 2 for i in range(10) if i % 2 == 0]
    print(f"  带条件: {even_squares}")


# ==============================================================================
# 第三部分：生成随机交易数据
# ==============================================================================

def generate_random_amount(amount_range: tuple = None) -> float:
    """
    生成随机交易金额
    
    【参数】
    amount_range: 金额范围元组 (最小值, 最大值)
                  如果不提供，则从预定义的范围中随机选择
    
    【返回】
    随机生成的金额（保留2位小数）
    """
    if amount_range is None:
        # 从预定义的金额范围中随机选择一个
        amount_range = random.choice(AMOUNT_RANGES)
    
    min_amount, max_amount = amount_range  # 元组解包
    
    # 生成随机金额
    amount = random.uniform(min_amount, max_amount)
    
    # 四舍五入到2位小数
    return round(amount, 2)


def generate_random_currency() -> str:
    """
    随机选择一个货币
    
    【返回】
    随机选择的货币代码
    """
    return random.choice(SUPPORTED_CURRENCIES)


def generate_random_channel() -> str:
    """
    随机选择一个支付通道
    
    【返回】
    随机选择的通道ID
    """
    # list()将字典的键转换为列表
    channel_ids = list(PAYMENT_CHANNELS.keys())
    return random.choice(channel_ids)


def generate_random_date(days_back: int = 30) -> datetime:
    """
    生成指定天数内的随机日期
    
    【参数】
    days_back: 往前多少天的范围
    
    【返回】
    随机日期时间对象
    """
    # 当前日期
    now = datetime.now()
    
    # 随机往前的天数
    random_days = random.randint(0, days_back)
    
    # timedelta用于日期时间的加减
    random_date = now - timedelta(days=random_days)
    
    # 加上随机的小时和分钟
    random_date = random_date.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )
    
    return random_date


# ==============================================================================
# 第四部分：生成单个交易
# ==============================================================================

def generate_single_transaction(
    amount: float = None,
    currency: str = None,
    channel_id: str = None,
) -> Transaction:
    """
    生成单个模拟交易
    
    【参数】
    amount: 金额（可选，不提供则随机生成）
    currency: 货币（可选，不提供则随机选择）
    channel_id: 通道ID（可选，不提供则随机选择）
    
    【返回】
    Transaction对象
    """
    # 如果没有提供参数，则随机生成
    if amount is None:
        amount = generate_random_amount()
    
    if currency is None:
        currency = generate_random_currency()
    
    if channel_id is None:
        channel_id = generate_random_channel()
    
    # 创建交易对象
    transaction = Transaction(
        amount=amount,
        currency=currency,
        channel_id=channel_id,
    )
    
    # 设置创建时间为随机日期
    transaction.created_at = generate_random_date()
    
    # 获取通道配置并计算费用
    channel_config = PAYMENT_CHANNELS.get(channel_id, {})
    base_rate = channel_config.get("base_rate", 0.02)
    fixed_fee = channel_config.get("fixed_fee", 0)
    
    # 计算手续费
    transaction.calculate_fee(base_rate, fixed_fee)
    
    # 转换为人民币
    exchange_rate = EXCHANGE_RATES.get(currency, 1.0)
    transaction.set_converted_amount(exchange_rate)
    
    # 随机设置交易状态
    # 大部分交易应该是成功的
    status_weights = [0.85, 0.10, 0.05]  # completed, pending, failed的概率
    statuses = ["completed", "pending", "failed"]
    transaction.status = random.choices(statuses, weights=status_weights)[0]
    
    return transaction


# ==============================================================================
# 第五部分：批量生成交易（使用循环）
# ==============================================================================

def generate_transactions(
    count: int = DEFAULT_TRANSACTION_COUNT,
    currency_filter: List[str] = None,
    channel_filter: List[str] = None,
    min_amount: float = None,
    max_amount: float = None,
) -> List[Transaction]:
    """
    批量生成模拟交易数据
    
    【参数】
    count: 要生成的交易数量
    currency_filter: 限制使用的货币列表（可选）
    channel_filter: 限制使用的通道列表（可选）
    min_amount: 最小金额（可选）
    max_amount: 最大金额（可选）
    
    【返回】
    Transaction对象列表
    
    【学习点】
    这个函数展示了如何使用for循环批量生成数据
    """
    # 创建空列表存储交易
    transactions = []
    
    # 确定可用的货币和通道
    available_currencies = currency_filter if currency_filter else SUPPORTED_CURRENCIES
    available_channels = channel_filter if channel_filter else list(PAYMENT_CHANNELS.keys())
    
    # 使用for循环生成指定数量的交易
    # range(count) 生成 0 到 count-1 的序列
    for i in range(count):
        # 随机选择货币和通道
        currency = random.choice(available_currencies)
        channel_id = random.choice(available_channels)
        
        # 生成金额
        if min_amount is not None and max_amount is not None:
            amount = random.uniform(min_amount, max_amount)
        else:
            amount = generate_random_amount()
        
        # 创建交易
        tx = generate_single_transaction(
            amount=amount,
            currency=currency,
            channel_id=channel_id,
        )
        
        # 将交易添加到列表
        # append() 方法向列表末尾添加元素
        transactions.append(tx)
        
        # 每生成100条数据打印一次进度（可选）
        if (i + 1) % 100 == 0:
            print(f"已生成 {i + 1}/{count} 条交易数据...")
    
    print(f"数据生成完成，共 {len(transactions)} 条交易")
    return transactions


# ==============================================================================
# 第六部分：按条件生成交易（展示while循环）
# ==============================================================================

def generate_transactions_by_total(
    target_total_amount: float,
    currency: str = "USD",
) -> List[Transaction]:
    """
    生成指定总金额的交易数据
    
    【while循环】
    while 条件:
        循环体
    
    只要条件为True，循环就会持续执行
    
    【参数】
    target_total_amount: 目标总金额
    currency: 使用的货币
    
    【返回】
    交易列表（总金额接近目标金额）
    """
    transactions = []
    current_total = 0
    
    # while循环：当总金额未达到目标时继续生成
    while current_total < target_total_amount:
        # 计算剩余需要的金额
        remaining = target_total_amount - current_total
        
        # 如果剩余金额很小，生成剩余金额的交易
        if remaining < 1000:
            amount = remaining
        else:
            # 否则生成随机金额（但不超过剩余金额）
            max_possible = min(remaining, 50000)  # 单笔最大5万
            amount = random.uniform(100, max_possible)
        
        # 生成交易
        tx = generate_single_transaction(
            amount=round(amount, 2),
            currency=currency,
        )
        
        transactions.append(tx)
        current_total += amount
        
        # 防止无限循环的保护措施
        if len(transactions) > 10000:
            print("警告：生成数量超过限制，停止生成")
            break  # break语句立即退出循环
    
    print(f"生成 {len(transactions)} 条交易，总金额: {current_total:.2f} {currency}")
    return transactions


# ==============================================================================
# 第七部分：生成特定分布的数据
# ==============================================================================

def generate_transactions_by_distribution(
    total_count: int = 1000,
    currency_distribution: dict = None,
) -> List[Transaction]:
    """
    根据指定的货币分布生成交易
    
    【参数】
    total_count: 总交易数量
    currency_distribution: 货币分布字典，如 {"USD": 0.4, "EUR": 0.3, "GBP": 0.3}
    
    【返回】
    按指定分布生成的交易列表
    """
    if currency_distribution is None:
        # 默认分布
        currency_distribution = {
            "USD": 0.35,
            "EUR": 0.25,
            "GBP": 0.15,
            "JPY": 0.10,
            "HKD": 0.10,
            "SGD": 0.05,
        }
    
    transactions = []
    
    # 根据分布计算每种货币的数量
    for currency, ratio in currency_distribution.items():
        # 计算该货币需要生成的数量
        count = int(total_count * ratio)
        
        # 使用列表推导式生成交易
        currency_transactions = [
            generate_single_transaction(currency=currency)
            for _ in range(count)  # _ 表示不需要使用的循环变量
        ]
        
        # 扩展列表（将另一个列表的元素添加到当前列表）
        # extend() vs append():
        # - append([1,2,3]) 结果: [..., [1,2,3]]（作为单个元素添加）
        # - extend([1,2,3]) 结果: [..., 1, 2, 3]（展开后添加）
        transactions.extend(currency_transactions)
    
    # 打乱顺序
    random.shuffle(transactions)
    
    print(f"按分布生成 {len(transactions)} 条交易")
    return transactions


# ==============================================================================
# 第八部分：转换为其他格式
# ==============================================================================

def transactions_to_dicts(transactions: List[Transaction]) -> List[dict]:
    """
    将交易对象列表转换为字典列表
    
    【用途】
    - 便于转换为DataFrame
    - 便于序列化为JSON
    - 便于存储到数据库
    """
    return [tx.to_dict() for tx in transactions]


def transactions_to_records(transactions: List[Transaction]) -> List[dict]:
    """
    将交易转换为简化的记录格式
    
    只保留分析需要的核心字段
    """
    records = []
    
    for tx in transactions:
        record = {
            "id": tx.transaction_id,
            "amount": tx.amount,
            "currency": tx.currency,
            "channel": tx.channel_id,
            "fee": tx.fee,
            "fee_rate": tx.fee_rate,
            "amount_cny": tx.amount_cny,
            "status": tx.status,
            "date": tx.created_at.strftime("%Y-%m-%d"),
        }
        records.append(record)
    
    return records


# ==============================================================================
# 学习小结
# ==============================================================================
"""
【本模块学到的内容】

1. random模块:
   - random(): 0-1随机浮点数
   - randint(a,b): 随机整数
   - uniform(a,b): 随机浮点数
   - choice(): 随机选择
   - choices(): 带权重随机选择
   - shuffle(): 打乱顺序

2. for循环:
   for item in iterable:
       do_something(item)
   
   - range(n): 0到n-1
   - enumerate(): 获取索引和值
   - dict.items(): 遍历字典

3. while循环:
   while condition:
       do_something()
   
   - break: 跳出循环
   - continue: 跳过本次循环

4. 列表操作:
   - append(): 添加单个元素
   - extend(): 添加多个元素
   - 列表推导式: [x for x in list]

【练习建议】
1. 修改generate_transactions，添加更多过滤条件
2. 实现一个生成器函数（使用yield），逐条生成交易
3. 添加生成特定时间段内交易的功能
"""


# ==============================================================================
# 模块测试代码
# ==============================================================================

if __name__ == "__main__":
    # 演示random基础
    demonstrate_random_basics()
    
    # 演示for循环
    demonstrate_for_loops()
    
    print("\n" + "=" * 60)
    print("测试交易数据生成")
    print("=" * 60)
    
    # 生成单个交易
    print("\n【生成单个交易】")
    tx = generate_single_transaction()
    print(tx)
    print(f"  费用: {tx.fee:.2f}")
    print(f"  费率: {tx.fee_rate:.2%}")
    
    # 批量生成
    print("\n【批量生成交易】")
    transactions = generate_transactions(count=10)
    
    print("\n生成的交易:")
    for i, tx in enumerate(transactions[:5]):  # 只显示前5条
        print(f"  {i+1}. {tx}")
    print(f"  ... 共 {len(transactions)} 条")
    
    # 统计货币分布
    print("\n【货币分布统计】")
    currency_counts = {}
    for tx in transactions:
        currency = tx.currency
        # dict.get(key, default) + 1 是计数的常用模式
        currency_counts[currency] = currency_counts.get(currency, 0) + 1
    
    for currency, count in sorted(currency_counts.items()):
        print(f"  {currency}: {count} 笔")
