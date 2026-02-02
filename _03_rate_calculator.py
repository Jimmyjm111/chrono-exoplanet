"""
==============================================================================
费率计算模块 (rate_calculator.py)
==============================================================================

【学习目标】
本模块帮助你学习Python的条件判断：
1. if/elif/else语句
2. 比较运算符和逻辑运算符
3. 嵌套条件判断
4. 条件表达式（三元运算符）
5. 实际业务逻辑中的条件处理

【业务背景】
跨境支付中，费率计算是核心功能：
- 不同通道有不同的基础费率
- 大额交易可能有阶梯费率（金额越大费率越低）
- 还需要考虑汇率损耗和其他隐性成本

==============================================================================
"""

from typing import Optional, Tuple, List
from _01_config import PAYMENT_CHANNELS, TIERED_RATES, EXCHANGE_RATES


# ==============================================================================
# 第一部分：比较运算符和逻辑运算符
# ==============================================================================

def demonstrate_operators():
    """
    演示Python的比较运算符和逻辑运算符
    
    【比较运算符】返回布尔值
    ==  等于
    !=  不等于
    >   大于
    <   小于
    >=  大于等于
    <=  小于等于
    
    【逻辑运算符】组合多个条件
    and  与：两个条件都为True才返回True
    or   或：其中一个条件为True就返回True
    not  非：取反
    
    【成员运算符】
    in      在...中
    not in  不在...中
    """
    print("【运算符演示】")
    
    # 比较运算符
    x = 10
    print(f"\nx = {x}")
    print(f"x == 10: {x == 10}")   # True
    print(f"x != 5: {x != 5}")     # True
    print(f"x > 5: {x > 5}")       # True
    print(f"x < 20: {x < 20}")     # True
    print(f"x >= 10: {x >= 10}")   # True
    print(f"x <= 10: {x <= 10}")   # True
    
    # 逻辑运算符
    print(f"\n逻辑运算符:")
    print(f"x > 5 and x < 15: {x > 5 and x < 15}")  # True
    print(f"x < 5 or x > 8: {x < 5 or x > 8}")      # True
    print(f"not (x > 20): {not (x > 20)}")          # True
    
    # 成员运算符
    currencies = ["USD", "EUR", "GBP"]
    print(f"\n成员运算符:")
    print(f"'USD' in {currencies}: {'USD' in currencies}")    # True
    print(f"'JPY' not in {currencies}: {'JPY' not in currencies}")  # True


# ==============================================================================
# 第二部分：基础if语句
# ==============================================================================

def calculate_simple_fee(amount: float, rate: float = 0.02) -> float:
    """
    简单费用计算（固定费率）
    
    【if语句基础语法】
    if 条件:
        条件为True时执行的代码
    
    【注意】
    - 条件后面要有冒号:
    - 下面的代码块要缩进（通常4个空格）
    """
    # 简单的条件检查
    if amount <= 0:
        # 金额无效，返回0
        return 0
    
    fee = amount * rate
    return fee


def calculate_fee_with_minimum(
    amount: float,
    rate: float = 0.02,
    min_fee: float = 10.0,
) -> float:
    """
    带最低收费的费用计算
    
    【if-else语句】
    if 条件:
        条件为True时执行
    else:
        条件为False时执行
    """
    if amount <= 0:
        return 0
    
    # 计算费用
    fee = amount * rate
    
    # 判断是否低于最低收费
    if fee < min_fee:
        return min_fee  # 返回最低收费
    else:
        return fee      # 返回计算的费用


# ==============================================================================
# 第三部分：多条件判断 if-elif-else
# ==============================================================================

def get_fee_tier(amount: float) -> str:
    """
    根据金额判断费用等级
    
    【if-elif-else语句】
    用于多个互斥条件的判断
    
    if 条件1:
        ...
    elif 条件2:
        ...
    elif 条件3:
        ...
    else:
        以上条件都不满足时执行
    
    【执行顺序】
    从上到下依次判断，一旦某个条件为True，
    执行对应代码块后就不再判断剩余条件
    """
    if amount <= 0:
        return "无效金额"
    elif amount < 1000:
        return "小额"
    elif amount < 10000:
        return "中额"
    elif amount < 100000:
        return "大额"
    else:
        return "超大额"


def calculate_tiered_rate(amount: float, channel_id: str) -> float:
    """
    计算阶梯费率
    
    【业务场景】
    很多通道对大额交易有优惠费率：
    - 0-10000元：1.5%
    - 10001-50000元：1.2%
    - 50001-100000元：1.0%
    - 100001以上：0.8%
    
    【返回】
    适用的费率
    """
    # 检查通道是否有阶梯费率配置
    if channel_id not in TIERED_RATES:
        # 没有阶梯费率，返回基础费率
        channel_config = PAYMENT_CHANNELS.get(channel_id, {})
        return channel_config.get("base_rate", 0.02)
    
    # 获取该通道的阶梯费率
    tiers = TIERED_RATES[channel_id]
    
    # 遍历阶梯，找到适用的费率
    for tier in tiers:
        if amount <= tier["max_amount"]:
            return tier["rate"]
    
    # 如果没找到（理论上不会发生），返回最后一个费率
    return tiers[-1]["rate"]


# ==============================================================================
# 第四部分：完整的费用计算
# ==============================================================================

def calculate_channel_fee(
    amount: float,
    channel_id: str,
    use_tiered_rate: bool = True,
) -> dict:
    """
    计算指定通道的完整费用
    
    【参数】
    amount: 交易金额
    channel_id: 支付通道ID
    use_tiered_rate: 是否使用阶梯费率
    
    【返回】
    包含费用明细的字典
    """
    # 获取通道配置
    channel_config = PAYMENT_CHANNELS.get(channel_id)
    
    # 如果通道不存在
    if channel_config is None:
        return {
            "success": False,
            "error": f"未知的支付通道: {channel_id}",
        }
    
    # 如果通道未启用
    if not channel_config.get("is_active", True):
        return {
            "success": False,
            "error": f"支付通道已停用: {channel_id}",
        }
    
    # 确定使用的费率
    if use_tiered_rate and channel_id in TIERED_RATES:
        rate = calculate_tiered_rate(amount, channel_id)
    else:
        rate = channel_config["base_rate"]
    
    # 计算费用
    fixed_fee = channel_config.get("fixed_fee", 0)
    calculated_fee = amount * rate + fixed_fee
    
    # 应用最低和最高限制
    min_fee = channel_config.get("min_fee", 0)
    max_fee = channel_config.get("max_fee", 0)
    
    # 使用嵌套条件判断
    final_fee = calculated_fee
    fee_note = ""
    
    if min_fee > 0 and calculated_fee < min_fee:
        final_fee = min_fee
        fee_note = "已应用最低收费"
    elif max_fee > 0 and calculated_fee > max_fee:
        final_fee = max_fee
        fee_note = "已应用最高收费"
    
    return {
        "success": True,
        "channel_id": channel_id,
        "channel_name": channel_config["name"],
        "amount": amount,
        "rate": rate,
        "fixed_fee": fixed_fee,
        "calculated_fee": round(calculated_fee, 2),
        "final_fee": round(final_fee, 2),
        "fee_note": fee_note,
    }


# ==============================================================================
# 第五部分：汇率计算
# ==============================================================================

def calculate_exchange_cost(
    amount: float,
    from_currency: str,
    to_currency: str = "CNY",
    spread_rate: float = 0.005,  # 汇率点差，默认0.5%
) -> dict:
    """
    计算货币兑换成本
    
    【业务背景】
    银行或支付平台在兑换货币时通常会加收"点差"
    即实际使用的汇率比市场汇率略差
    这是一种隐性成本
    
    【参数】
    amount: 原币金额
    from_currency: 原币种
    to_currency: 目标币种
    spread_rate: 汇率点差比例
    """
    # 获取汇率
    if from_currency not in EXCHANGE_RATES:
        return {
            "success": False,
            "error": f"不支持的货币: {from_currency}",
        }
    
    # 获取市场汇率（这里用配置中的汇率模拟）
    market_rate = EXCHANGE_RATES[from_currency]
    
    # 计算包含点差的实际汇率（对客户不利的方向）
    # 当客户卖出外币时，汇率会低于市场价
    actual_rate = market_rate * (1 - spread_rate)
    
    # 按市场汇率计算的金额
    market_amount = amount * market_rate
    
    # 按实际汇率计算的金额
    actual_amount = amount * actual_rate
    
    # 汇率损耗
    exchange_loss = market_amount - actual_amount
    
    return {
        "success": True,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "original_amount": amount,
        "market_rate": market_rate,
        "actual_rate": round(actual_rate, 4),
        "spread_rate": spread_rate,
        "market_amount": round(market_amount, 2),
        "actual_amount": round(actual_amount, 2),
        "exchange_loss": round(exchange_loss, 2),
        "loss_percentage": round(spread_rate * 100, 2),
    }


# ==============================================================================
# 第六部分：综合成本计算
# ==============================================================================

def calculate_total_cost(
    amount: float,
    currency: str,
    channel_id: str,
    spread_rate: float = 0.005,
) -> dict:
    """
    计算交易总成本（手续费 + 汇率损耗）
    
    【综合判断的例子】
    这个函数展示了如何组合多个条件和计算结果
    """
    result = {
        "success": True,
        "amount": amount,
        "currency": currency,
        "channel_id": channel_id,
    }
    
    # 计算手续费
    fee_result = calculate_channel_fee(amount, channel_id)
    
    if not fee_result["success"]:
        return fee_result  # 返回错误信息
    
    result["fee"] = fee_result["final_fee"]
    result["fee_rate"] = fee_result["rate"]
    
    # 如果不是人民币，计算汇率成本
    if currency != "CNY":
        exchange_result = calculate_exchange_cost(
            amount, currency, spread_rate=spread_rate
        )
        
        if not exchange_result["success"]:
            result["success"] = False
            result["error"] = exchange_result["error"]
            return result
        
        result["exchange_loss"] = exchange_result["exchange_loss"]
        result["amount_cny"] = exchange_result["actual_amount"]
        
        # 总成本 = 手续费（换算为人民币）+ 汇率损耗
        fee_cny = result["fee"] * exchange_result["actual_rate"]
        total_cost = fee_cny + result["exchange_loss"]
    else:
        result["exchange_loss"] = 0
        result["amount_cny"] = amount
        total_cost = result["fee"]
    
    result["total_cost"] = round(total_cost, 2)
    
    # 计算总成本率
    if result["amount_cny"] > 0:
        result["total_cost_rate"] = round(
            total_cost / result["amount_cny"], 4
        )
    else:
        result["total_cost_rate"] = 0
    
    return result


# ==============================================================================
# 第七部分：多通道费率对比
# ==============================================================================

def compare_channel_fees(
    amount: float,
    currency: str,
    channel_ids: List[str] = None,
) -> List[dict]:
    """
    比较多个通道的费用
    
    【参数】
    amount: 交易金额
    currency: 货币类型
    channel_ids: 要比较的通道列表（默认比较所有通道）
    
    【返回】
    按总成本排序的通道费用列表
    """
    if channel_ids is None:
        channel_ids = list(PAYMENT_CHANNELS.keys())
    
    results = []
    
    for channel_id in channel_ids:
        # 检查通道是否支持该货币
        channel_config = PAYMENT_CHANNELS.get(channel_id, {})
        supported = channel_config.get("supported_currencies", [])
        
        # 条件判断：是否支持该货币
        if currency not in supported:
            continue  # 跳过不支持的通道
        
        # 计算总成本
        cost_result = calculate_total_cost(amount, currency, channel_id)
        
        if cost_result["success"]:
            results.append({
                "channel_id": channel_id,
                "channel_name": channel_config["name"],
                "fee": cost_result["fee"],
                "exchange_loss": cost_result.get("exchange_loss", 0),
                "total_cost": cost_result["total_cost"],
                "total_cost_rate": cost_result["total_cost_rate"],
            })
    
    # 按总成本排序（使用lambda表达式）
    # sorted() 函数对列表排序
    # key参数指定排序依据
    # lambda x: x["total_cost"] 是一个匿名函数，返回每个元素的total_cost
    results = sorted(results, key=lambda x: x["total_cost"])
    
    # 添加排名
    for i, result in enumerate(results):
        result["rank"] = i + 1
    
    return results


def find_cheapest_channel(
    amount: float,
    currency: str,
) -> Optional[dict]:
    """
    找到最便宜的支付通道
    
    【条件表达式（三元运算符）】
    value_if_true if condition else value_if_false
    
    这是if-else的简洁写法
    """
    comparison = compare_channel_fees(amount, currency)
    
    # 使用条件表达式返回结果
    # 如果列表不为空，返回第一个（最便宜的）；否则返回None
    return comparison[0] if comparison else None


# ==============================================================================
# 学习小结
# ==============================================================================
"""
【本模块学到的内容】

1. 条件语句:
   if 条件:
       ...
   elif 另一条件:
       ...
   else:
       ...

2. 比较运算符:
   ==, !=, >, <, >=, <=

3. 逻辑运算符:
   and（与）, or（或）, not（非）

4. 成员运算符:
   in, not in

5. 条件表达式:
   result = value_if_true if condition else value_if_false

6. 循环中的条件控制:
   - continue: 跳过当前循环，继续下一次
   - break: 跳出整个循环

【练习建议】
1. 添加一个基于交易次数的累计折扣计算
2. 实现按月度账单计算费用（达到一定金额免手续费）
3. 添加更多的边界条件检查和错误处理
"""


# ==============================================================================
# 模块测试代码
# ==============================================================================

if __name__ == "__main__":
    # 演示运算符
    demonstrate_operators()
    
    print("\n" + "=" * 60)
    print("费率计算测试")
    print("=" * 60)
    
    # 测试费用等级
    print("\n【费用等级测试】")
    test_amounts = [500, 5000, 50000, 200000]
    for amount in test_amounts:
        tier = get_fee_tier(amount)
        print(f"  金额 {amount:>8} -> {tier}")
    
    # 测试阶梯费率
    print("\n【阶梯费率测试 - 银行电汇】")
    for amount in test_amounts:
        rate = calculate_tiered_rate(amount, "bank_transfer")
        print(f"  金额 {amount:>8} -> 费率 {rate:.2%}")
    
    # 测试完整费用计算
    print("\n【完整费用计算】")
    result = calculate_channel_fee(10000, "swift")
    print(f"  通道: {result['channel_name']}")
    print(f"  金额: {result['amount']}")
    print(f"  费率: {result['rate']:.2%}")
    print(f"  计算费用: {result['calculated_fee']}")
    print(f"  最终费用: {result['final_fee']}")
    if result['fee_note']:
        print(f"  备注: {result['fee_note']}")
    
    # 测试汇率计算
    print("\n【汇率成本计算 - 1000美元】")
    exchange = calculate_exchange_cost(1000, "USD")
    print(f"  市场汇率: {exchange['market_rate']}")
    print(f"  实际汇率: {exchange['actual_rate']}")
    print(f"  市场金额: {exchange['market_amount']} CNY")
    print(f"  实际金额: {exchange['actual_amount']} CNY")
    print(f"  汇率损耗: {exchange['exchange_loss']} CNY")
    
    # 测试通道对比
    print("\n【通道费用对比 - 10000 USD】")
    comparison = compare_channel_fees(10000, "USD")
    print(f"  {'排名':<4} {'通道':<15} {'手续费':>10} {'汇损':>10} {'总成本':>10} {'成本率':>8}")
    print("  " + "-" * 60)
    for item in comparison:
        print(f"  {item['rank']:<4} {item['channel_name']:<15} "
              f"{item['fee']:>10.2f} {item['exchange_loss']:>10.2f} "
              f"{item['total_cost']:>10.2f} {item['total_cost_rate']:>7.2%}")
    
    # 找最便宜的通道
    cheapest = find_cheapest_channel(10000, "USD")
    if cheapest:
        print(f"\n  推荐通道: {cheapest['channel_name']}, 总成本: {cheapest['total_cost']:.2f} CNY")
