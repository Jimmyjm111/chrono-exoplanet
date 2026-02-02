"""
==============================================================================
工具函数模块 (utils.py)
==============================================================================

【学习目标】
本模块帮助你学习Python函数的高级用法：
1. 函数定义和参数
2. 默认参数和关键字参数
3. 文档字符串(docstring)
4. 类型提示(type hints)
5. 函数的返回值
6. 异常处理(try/except)

【什么是工具函数？】
工具函数是一些通用的、可复用的小函数
它们通常不属于某个特定类，而是作为独立的函数存在
可以被项目中的多个模块调用

==============================================================================
"""

from datetime import datetime, timedelta
from typing import Union, List, Optional, Any
import os


# ==============================================================================
# 第一部分：基础函数定义
# ==============================================================================

def format_currency(amount: float, currency: str = "CNY", decimal_places: int = 2) -> str:
    """
    格式化货币金额
    
    【函数定义语法】
    def 函数名(参数1, 参数2=默认值) -> 返回类型:
        '''文档字符串'''
        函数体
        return 返回值
    
    【参数类型】
    - 位置参数: amount（必须提供）
    - 关键字参数: currency, decimal_places（有默认值，可省略）
    
    【示例】
    >>> format_currency(1234.5)
    'CNY 1,234.50'
    >>> format_currency(1234.5, "USD")
    'USD 1,234.50'
    >>> format_currency(1234.567, "EUR", 3)
    'EUR 1,234.567'
    """
    # 货币符号映射
    currency_symbols = {
        "CNY": "¥",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "HKD": "HK$",
        "SGD": "S$",
        "PHP": "₱",
    }
    
    # 获取符号，如果没有对应符号则使用货币代码
    # dict.get(key, default) 方法：获取key对应的值，如果不存在返回default
    symbol = currency_symbols.get(currency, currency)
    
    # 格式化数字
    # :,.{n}f 表示：千位分隔符，n位小数
    # f-string中可以嵌套使用格式化
    formatted = f"{amount:,.{decimal_places}f}"
    
    return f"{symbol}{formatted}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    将小数转换为百分比字符串
    
    【参数】
    value: 要转换的值（如0.025表示2.5%）
    decimal_places: 小数位数
    
    【示例】
    >>> format_percentage(0.025)
    '2.50%'
    >>> format_percentage(0.1, 0)
    '10%'
    """
    percentage = value * 100
    return f"{percentage:.{decimal_places}f}%"


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """
    格式化日期
    
    【常用日期格式代码】
    %Y: 四位年份 (2024)
    %m: 两位月份 (01-12)
    %d: 两位日期 (01-31)
    %H: 小时24制 (00-23)
    %M: 分钟 (00-59)
    %S: 秒 (00-59)
    
    【示例】
    >>> format_date(datetime.now())
    '2024-01-15'
    >>> format_date(datetime.now(), "%Y年%m月%d日")
    '2024年01月15日'
    """
    return date.strftime(format_str)


# ==============================================================================
# 第二部分：数据验证函数
# ==============================================================================

def validate_amount(amount: Any) -> float:
    """
    验证并转换金额
    
    【异常处理】
    try/except 用于捕获和处理错误
    语法：
    try:
        可能出错的代码
    except 错误类型:
        处理错误的代码
    
    【参数】
    amount: 要验证的值（可以是任意类型）
    
    【返回】
    验证通过的浮点数金额
    
    【异常】
    ValueError: 如果金额无效（无法转换为数字或为负数）
    """
    try:
        # 尝试将输入转换为浮点数
        amount_float = float(amount)
        
        # 检查是否为负数
        if amount_float < 0:
            # raise 用于主动抛出异常
            raise ValueError("金额不能为负数")
        
        return amount_float
        
    except (ValueError, TypeError) as e:
        # 捕获转换错误或类型错误
        # as e 将捕获的异常保存到变量e中
        raise ValueError(f"无效的金额: {amount}, 错误: {e}")


def validate_currency(currency: str, supported_currencies: List[str]) -> str:
    """
    验证货币代码
    
    【参数】
    currency: 货币代码
    supported_currencies: 支持的货币列表
    
    【返回】
    大写的货币代码
    """
    # upper() 方法将字符串转为大写
    currency_upper = currency.upper()
    
    # 检查是否在支持列表中
    if currency_upper not in supported_currencies:
        supported_list = ", ".join(supported_currencies)
        raise ValueError(f"不支持的货币: {currency}. 支持的货币: {supported_list}")
    
    return currency_upper


def is_valid_exchange_rate(rate: float) -> bool:
    """
    检查汇率是否有效
    
    【返回布尔值的函数】
    以 is_、has_、can_ 等开头的函数通常返回布尔值
    这是一种命名约定，让代码更易读
    """
    # 汇率必须是正数且在合理范围内
    return 0 < rate < 10000


# ==============================================================================
# 第三部分：计算辅助函数
# ==============================================================================

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    计算百分比变化
    
    【参数】
    old_value: 原始值
    new_value: 新值
    
    【返回】
    变化百分比（如0.1表示增长10%，-0.05表示下降5%）
    
    【异常处理】
    如果原始值为0，返回None避免除零错误
    """
    if old_value == 0:
        return None  # 避免除以零
    
    return (new_value - old_value) / old_value


def round_to_decimal(value: float, decimal_places: int = 2) -> float:
    """
    四舍五入到指定小数位
    
    【内置函数round】
    round(number, ndigits) 将数字四舍五入到指定小数位
    """
    return round(value, decimal_places)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    将值限制在指定范围内
    
    【min/max内置函数】
    min(...) 返回最小值
    max(...) 返回最大值
    
    【示例】
    >>> clamp(5, 0, 10)
    5
    >>> clamp(-5, 0, 10)
    0
    >>> clamp(15, 0, 10)
    10
    """
    return max(min_value, min(value, max_value))


# ==============================================================================
# 第四部分：文件和路径操作
# ==============================================================================

def ensure_directory_exists(directory_path: str) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    【os模块】
    os模块提供了与操作系统交互的功能
    os.path: 路径操作
    os.makedirs: 创建目录（包括父目录）
    
    【参数】
    directory_path: 目录路径
    
    【返回】
    True表示目录已存在或创建成功
    """
    if not os.path.exists(directory_path):
        try:
            # exist_ok=True: 如果目录已存在不报错
            os.makedirs(directory_path, exist_ok=True)
            print(f"创建目录: {directory_path}")
            return True
        except OSError as e:
            print(f"创建目录失败: {e}")
            return False
    return True


def get_output_filepath(filename: str, subdirectory: str = "") -> str:
    """
    获取输出文件的完整路径
    
    【路径拼接】
    os.path.join() 用于安全地拼接路径
    比直接用 + 或 / 拼接更安全，能处理不同操作系统的路径分隔符
    """
    base_dir = "output"
    
    if subdirectory:
        full_path = os.path.join(base_dir, subdirectory, filename)
    else:
        full_path = os.path.join(base_dir, filename)
    
    # 确保目录存在
    directory = os.path.dirname(full_path)
    ensure_directory_exists(directory)
    
    return full_path


# ==============================================================================
# 第五部分：数据处理辅助函数
# ==============================================================================

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    安全除法，避免除以零错误
    
    【三元表达式】
    value_if_true if condition else value_if_false
    这是if-else的简洁写法
    """
    return numerator / denominator if denominator != 0 else default


def filter_none_values(data: dict) -> dict:
    """
    过滤字典中值为None的项
    
    【字典推导式】
    {key: value for key, value in dict.items() if condition}
    类似列表推导式，用于创建新字典
    """
    return {k: v for k, v in data.items() if v is not None}


def group_by_key(items: List[dict], key: str) -> dict:
    """
    根据指定键对列表进行分组
    
    【参数】
    items: 字典列表
    key: 用于分组的键名
    
    【示例】
    >>> items = [{"type": "a", "val": 1}, {"type": "b", "val": 2}, {"type": "a", "val": 3}]
    >>> group_by_key(items, "type")
    {'a': [{'type': 'a', 'val': 1}, {'type': 'a', 'val': 3}], 'b': [{'type': 'b', 'val': 2}]}
    """
    result = {}
    
    for item in items:
        # 获取分组键的值
        group_key = item.get(key)
        
        if group_key not in result:
            # 如果这个组还不存在，创建空列表
            result[group_key] = []
        
        # 将项添加到对应的组
        result[group_key].append(item)
    
    return result


def flatten_list(nested_list: List[list]) -> list:
    """
    将嵌套列表展平为一维列表
    
    【列表推导式的嵌套】
    [item for sublist in nested_list for item in sublist]
    等价于：
    result = []
    for sublist in nested_list:
        for item in sublist:
            result.append(item)
    """
    return [item for sublist in nested_list for item in sublist]


# ==============================================================================
# 第六部分：统计辅助函数
# ==============================================================================

def calculate_statistics(values: List[float]) -> dict:
    """
    计算基本统计数据
    
    【返回】
    包含以下统计量的字典：
    - count: 数量
    - sum: 总和
    - mean: 平均值
    - min: 最小值
    - max: 最大值
    - range: 范围(最大-最小)
    """
    if not values:
        return {
            "count": 0,
            "sum": 0,
            "mean": 0,
            "min": 0,
            "max": 0,
            "range": 0,
        }
    
    count = len(values)
    total = sum(values)
    mean = total / count
    min_val = min(values)
    max_val = max(values)
    
    return {
        "count": count,
        "sum": round(total, 2),
        "mean": round(mean, 2),
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "range": round(max_val - min_val, 2),
    }


def calculate_percentile(values: List[float], percentile: float) -> float:
    """
    计算百分位数
    
    【参数】
    values: 数值列表
    percentile: 百分位（0-100之间）
    
    【示例】
    >>> calculate_percentile([1, 2, 3, 4, 5], 50)
    3  # 中位数
    """
    if not values:
        return 0
    
    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * percentile / 100
    
    # 如果索引是整数，直接取值
    if index.is_integer():
        return sorted_values[int(index)]
    
    # 否则进行线性插值
    lower_index = int(index)
    upper_index = lower_index + 1
    weight = index - lower_index
    
    return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight


# ==============================================================================
# 学习小结
# ==============================================================================
"""
【本模块学到的内容】

1. 函数定义：
   def function_name(param1, param2=default) -> return_type:
       '''docstring'''
       return value

2. 参数类型：
   - 位置参数：必须按顺序提供
   - 关键字参数：有默认值，可以省略或按名称传递
   - *args: 可变位置参数
   - **kwargs: 可变关键字参数

3. 异常处理：
   try:
       可能出错的代码
   except ErrorType as e:
       处理错误
   finally:
       无论是否出错都执行

4. 常用内置函数：
   - len(): 获取长度
   - sum(): 求和
   - min()/max(): 最小/最大值
   - sorted(): 排序
   - round(): 四舍五入

5. 推导式：
   - 列表推导式: [x for x in list if condition]
   - 字典推导式: {k: v for k, v in dict.items()}

【练习建议】
1. 修改format_currency，添加更多货币符号
2. 编写一个函数，计算列表的标准差
3. 尝试编写一个递归函数（如计算阶乘）
"""


# ==============================================================================
# 模块测试代码
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("测试工具函数")
    print("=" * 60)
    
    # 测试格式化函数
    print("\n【货币格式化测试】")
    print(f"format_currency(1234.5): {format_currency(1234.5)}")
    print(f"format_currency(1234.5, 'USD'): {format_currency(1234.5, 'USD')}")
    print(f"format_currency(9999999.99, 'EUR'): {format_currency(9999999.99, 'EUR')}")
    
    print("\n【百分比格式化测试】")
    print(f"format_percentage(0.025): {format_percentage(0.025)}")
    print(f"format_percentage(0.1234, 1): {format_percentage(0.1234, 1)}")
    
    # 测试验证函数
    print("\n【金额验证测试】")
    try:
        print(f"validate_amount('100.5'): {validate_amount('100.5')}")
        print(f"validate_amount(-50): ", end="")
        validate_amount(-50)  # 这会抛出异常
    except ValueError as e:
        print(f"错误 - {e}")
    
    # 测试统计函数
    print("\n【统计计算测试】")
    test_values = [10, 20, 30, 40, 50]
    stats = calculate_statistics(test_values)
    print(f"数据: {test_values}")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n中位数(50%): {calculate_percentile(test_values, 50)}")
    print(f"75百分位: {calculate_percentile(test_values, 75)}")
