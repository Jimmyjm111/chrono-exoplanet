"""
==============================================================================
数据分析模块 (analyzer.py)
==============================================================================

【学习目标】
本模块帮助你学习Pandas库和数据分析基础：
1. DataFrame的创建和基本操作
2. 数据筛选和过滤
3. 分组聚合（groupby）
4. 数据透视表（pivot table）
5. 基本统计计算

【什么是Pandas？】
Pandas是Python最重要的数据分析库，提供：
- DataFrame：二维表格数据结构（类似Excel表格）
- Series：一维数据结构（类似表格的一列）
- 强大的数据处理和分析功能

==============================================================================
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

# 导入项目模块
from _01_config import PAYMENT_CHANNELS, EXCHANGE_RATES
from _05_models import Transaction


# ==============================================================================
# 第一部分：DataFrame基础
# ==============================================================================

def demonstrate_dataframe_basics():
    """
    演示DataFrame的基本用法
    
    【创建DataFrame】
    1. 从字典创建：pd.DataFrame(dict)
    2. 从列表创建：pd.DataFrame(list_of_dicts)
    3. 从CSV读取：pd.read_csv(filepath)
    """
    print("【DataFrame基础演示】")
    
    # 方式1：从字典创建
    # 字典的key是列名，value是列数据（列表）
    data_dict = {
        "channel": ["bank", "wallet", "card"],
        "fee_rate": [0.015, 0.02, 0.012],
        "volume": [100000, 150000, 80000],
    }
    df1 = pd.DataFrame(data_dict)
    print("\n从字典创建:")
    print(df1)
    
    # 方式2：从字典列表创建
    # 每个字典是一行数据
    data_list = [
        {"channel": "bank", "fee_rate": 0.015, "volume": 100000},
        {"channel": "wallet", "fee_rate": 0.02, "volume": 150000},
        {"channel": "card", "fee_rate": 0.012, "volume": 80000},
    ]
    df2 = pd.DataFrame(data_list)
    print("\n从列表创建:")
    print(df2)
    
    # 基本属性
    print(f"\n形状(行,列): {df2.shape}")
    print(f"列名: {list(df2.columns)}")
    print(f"数据类型:\n{df2.dtypes}")
    
    # 基本操作
    print("\n【基本操作】")
    
    # 选择单列（返回Series）
    print(f"选择channel列: {list(df2['channel'])}")
    
    # 选择多列（返回DataFrame）
    print(f"选择多列:\n{df2[['channel', 'fee_rate']]}")
    
    # 选择行（使用iloc按位置，loc按标签）
    print(f"\n第一行（iloc[0]）: {dict(df2.iloc[0])}")
    
    # 添加新列
    df2['revenue'] = df2['volume'] * df2['fee_rate']
    print(f"\n添加revenue列后:\n{df2}")


# ==============================================================================
# 第二部分：将交易数据转换为DataFrame
# ==============================================================================

def transactions_to_dataframe(transactions: List[Transaction]) -> pd.DataFrame:
    """
    将Transaction对象列表转换为DataFrame
    
    【参数】
    transactions: Transaction对象列表
    
    【返回】
    包含交易数据的DataFrame
    """
    # 使用列表推导式将对象转换为字典列表
    records = [tx.to_dict() for tx in transactions]
    
    # 创建DataFrame
    df = pd.DataFrame(records)
    
    # 数据类型转换
    # pd.to_datetime()将字符串转换为日期时间类型
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
    
    # 添加一些衍生列
    if 'created_at' in df.columns:
        # 提取日期部分
        df['date'] = df['created_at'].dt.date
        # 提取月份
        df['month'] = df['created_at'].dt.to_period('M')
    
    return df


# ==============================================================================
# 第三部分：数据筛选和过滤
# ==============================================================================

def filter_transactions(
    df: pd.DataFrame,
    currency: str = None,
    channel_id: str = None,
    status: str = None,
    min_amount: float = None,
    max_amount: float = None,
) -> pd.DataFrame:
    """
    筛选交易数据
    
    【DataFrame筛选语法】
    df[条件] 返回满足条件的行
    
    条件使用比较运算符创建布尔Series：
    df['column'] == value
    df['column'] > value
    
    多个条件用 & (与) 或 | (或) 连接
    每个条件要用括号包围
    
    【参数】
    df: 交易数据DataFrame
    其他参数: 筛选条件
    
    【返回】
    筛选后的DataFrame
    """
    # 创建初始掩码（全部为True）
    # 掩码是布尔Series，True表示保留，False表示过滤掉
    mask = pd.Series([True] * len(df))
    
    # 根据参数添加筛选条件
    if currency is not None:
        # & 运算符：与操作
        mask = mask & (df['currency'] == currency)
    
    if channel_id is not None:
        mask = mask & (df['channel_id'] == channel_id)
    
    if status is not None:
        mask = mask & (df['status'] == status)
    
    if min_amount is not None:
        mask = mask & (df['amount'] >= min_amount)
    
    if max_amount is not None:
        mask = mask & (df['amount'] <= max_amount)
    
    # 应用掩码筛选
    # .copy() 创建副本，避免修改原数据时的警告
    return df[mask].copy()


def filter_by_date_range(
    df: pd.DataFrame,
    start_date: datetime = None,
    end_date: datetime = None,
) -> pd.DataFrame:
    """
    按日期范围筛选
    """
    mask = pd.Series([True] * len(df))
    
    if 'created_at' in df.columns:
        if start_date is not None:
            mask = mask & (df['created_at'] >= start_date)
        if end_date is not None:
            mask = mask & (df['created_at'] <= end_date)
    
    return df[mask].copy()


# ==============================================================================
# 第四部分：分组聚合（groupby）
# ==============================================================================

def analyze_by_channel(df: pd.DataFrame) -> pd.DataFrame:
    """
    按支付通道分组分析
    
    【groupby基础】
    df.groupby('列名') 按指定列分组
    然后可以使用聚合函数：
    - .sum()     求和
    - .mean()    平均值
    - .count()   计数
    - .min()     最小值
    - .max()     最大值
    - .agg()     多个聚合操作
    
    【返回】
    按通道汇总的统计数据
    """
    # 按channel_id分组
    grouped = df.groupby('channel_id')
    
    # 使用agg()进行多种聚合
    # 字典的key是列名，value是聚合操作
    summary = grouped.agg({
        'amount': ['count', 'sum', 'mean'],  # 交易数量、总金额、平均金额
        'fee': ['sum', 'mean'],              # 总费用、平均费用
        'amount_cny': 'sum',                 # 总人民币金额
    })
    
    # 扁平化多级列名
    # 原来是 ('amount', 'count'), ('amount', 'sum') 等
    # 转换为 'amount_count', 'amount_sum' 等
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    
    # 添加通道名称
    summary['channel_name'] = summary.index.map(
        lambda x: PAYMENT_CHANNELS.get(x, {}).get('name', x)
    )
    
    # 计算平均费率
    summary['avg_fee_rate'] = summary['fee_sum'] / summary['amount_sum'].replace(0, float('nan'))
    
    # 重置索引，将channel_id从索引变为普通列
    summary = summary.reset_index()
    
    # 重命名列使其更易读
    summary = summary.rename(columns={
        'amount_count': 'transaction_count',
        'amount_sum': 'total_amount',
        'amount_mean': 'avg_amount',
        'fee_sum': 'total_fee',
        'fee_mean': 'avg_fee',
        'amount_cny_sum': 'total_amount_cny',
    })
    
    return summary


def analyze_by_currency(df: pd.DataFrame) -> pd.DataFrame:
    """
    按货币分组分析
    """
    grouped = df.groupby('currency')
    
    summary = grouped.agg({
        'amount': ['count', 'sum', 'mean'],
        'fee': ['sum', 'mean'],
        'amount_cny': 'sum',
    })
    
    summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
    
    # 添加货币对人民币汇率
    summary['exchange_rate'] = summary.index.map(
        lambda x: EXCHANGE_RATES.get(x, 1.0)
    )
    
    summary = summary.reset_index()
    
    summary = summary.rename(columns={
        'amount_count': 'transaction_count',
        'amount_sum': 'total_amount',
        'amount_mean': 'avg_amount',
        'fee_sum': 'total_fee',
        'fee_mean': 'avg_fee',
        'amount_cny_sum': 'total_amount_cny',
    })
    
    return summary


# ==============================================================================
# 第五部分：数据透视表
# ==============================================================================

def create_channel_currency_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """
    创建通道-货币交叉表
    
    【数据透视表】
    pd.pivot_table() 创建类似Excel透视表的汇总
    
    参数：
    - index: 行标签
    - columns: 列标签
    - values: 要汇总的值
    - aggfunc: 聚合函数
    - fill_value: 填充空值
    
    【返回】
    按通道和货币汇总的交易金额透视表
    """
    pivot = pd.pivot_table(
        df,
        index='channel_id',        # 行：支付通道
        columns='currency',        # 列：货币
        values='amount',           # 值：交易金额
        aggfunc='sum',             # 聚合方式：求和
        fill_value=0,              # 空值填充为0
    )
    
    # 添加行合计
    pivot['总计'] = pivot.sum(axis=1)  # axis=1 表示按行求和
    
    # 添加列合计
    pivot.loc['总计'] = pivot.sum(axis=0)  # axis=0 表示按列求和
    
    return pivot


def create_fee_rate_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    创建费率矩阵（通道×货币的平均费率）
    """
    # 先计算费率
    df_with_rate = df.copy()
    df_with_rate['fee_rate_calc'] = df_with_rate['fee'] / df_with_rate['amount'].replace(0, float('nan'))
    
    pivot = pd.pivot_table(
        df_with_rate,
        index='channel_id',
        columns='currency',
        values='fee_rate_calc',
        aggfunc='mean',  # 平均费率
        fill_value=None,
    )
    
    return pivot


# ==============================================================================
# 第六部分：统计分析
# ==============================================================================

def calculate_summary_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    计算汇总统计数据
    
    【describe()方法】
    df.describe() 自动计算常用统计量：
    count, mean, std, min, 25%, 50%, 75%, max
    """
    stats = {
        "total_transactions": len(df),
        "total_amount": df['amount'].sum(),
        "total_amount_cny": df['amount_cny'].sum() if 'amount_cny' in df.columns else 0,
        "total_fee": df['fee'].sum() if 'fee' in df.columns else 0,
        "avg_amount": df['amount'].mean(),
        "avg_fee": df['fee'].mean() if 'fee' in df.columns else 0,
    }
    
    # 按状态统计
    if 'status' in df.columns:
        status_counts = df['status'].value_counts().to_dict()
        stats["status_distribution"] = status_counts
        stats["success_rate"] = status_counts.get('completed', 0) / len(df)
    
    # 货币分布
    if 'currency' in df.columns:
        currency_counts = df['currency'].value_counts().to_dict()
        stats["currency_distribution"] = currency_counts
    
    # 通道分布
    if 'channel_id' in df.columns:
        channel_counts = df['channel_id'].value_counts().to_dict()
        stats["channel_distribution"] = channel_counts
    
    return stats


def calculate_percentiles(df: pd.DataFrame, column: str) -> Dict[str, float]:
    """
    计算指定列的百分位数
    
    【quantile()方法】
    df['column'].quantile(0.5) 返回50%百分位数（中位数）
    """
    percentiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
    
    result = {}
    for p in percentiles:
        value = df[column].quantile(p)
        result[f"p{int(p*100)}"] = round(value, 2)
    
    return result


# ==============================================================================
# 第七部分：数据排序和排名
# ==============================================================================

def get_top_transactions(
    df: pd.DataFrame,
    n: int = 10,
    by: str = 'amount',
    ascending: bool = False,
) -> pd.DataFrame:
    """
    获取排名前N的交易
    
    【sort_values()方法】
    df.sort_values(by='列名', ascending=False) 按指定列排序
    ascending=False 表示降序（从大到小）
    """
    sorted_df = df.sort_values(by=by, ascending=ascending)
    return sorted_df.head(n)


def rank_channels_by_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    按交易量对通道进行排名
    """
    channel_volume = df.groupby('channel_id').agg({
        'amount': 'sum',
        'transaction_id': 'count',
    }).rename(columns={
        'amount': 'total_volume',
        'transaction_id': 'transaction_count',
    })
    
    # 按交易量排序
    channel_volume = channel_volume.sort_values('total_volume', ascending=False)
    
    # 添加排名
    channel_volume['rank'] = range(1, len(channel_volume) + 1)
    
    # 添加通道名称
    channel_volume['channel_name'] = channel_volume.index.map(
        lambda x: PAYMENT_CHANNELS.get(x, {}).get('name', x)
    )
    
    return channel_volume.reset_index()


# ==============================================================================
# 第八部分：费率对比分析（核心业务分析）
# ==============================================================================

def analyze_fee_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    分析各通道的费率对比
    
    这是项目的核心分析功能
    """
    # 按通道分组
    channel_stats = df.groupby('channel_id').agg({
        'amount': ['count', 'sum', 'mean'],
        'fee': ['sum', 'mean'],
        'fee_rate': 'mean',
        'amount_cny': 'sum',
    })
    
    # 扁平化列名
    channel_stats.columns = [
        'tx_count', 'total_amount', 'avg_amount',
        'total_fee', 'avg_fee', 'avg_fee_rate', 'total_cny'
    ]
    
    # 添加通道信息
    channel_stats['channel_name'] = channel_stats.index.map(
        lambda x: PAYMENT_CHANNELS.get(x, {}).get('name', x)
    )
    
    channel_stats['channel_type'] = channel_stats.index.map(
        lambda x: PAYMENT_CHANNELS.get(x, {}).get('type', 'unknown')
    )
    
    # 计算费用占比
    total_all_fee = channel_stats['total_fee'].sum()
    channel_stats['fee_share'] = channel_stats['total_fee'] / total_all_fee
    
    # 排序
    channel_stats = channel_stats.sort_values('avg_fee_rate')
    
    # 重置索引
    channel_stats = channel_stats.reset_index()
    
    # 四舍五入
    numeric_cols = ['total_amount', 'avg_amount', 'total_fee', 'avg_fee', 'total_cny']
    channel_stats[numeric_cols] = channel_stats[numeric_cols].round(2)
    
    return channel_stats


def find_optimal_channel_for_amount(
    df: pd.DataFrame,
    target_amount: float,
    currency: str = "USD",
) -> Dict[str, Any]:
    """
    为指定金额找到最优通道
    
    基于历史数据分析最适合的通道
    """
    # 筛选相似金额范围的交易
    amount_range = 0.3  # 30%范围
    min_amount = target_amount * (1 - amount_range)
    max_amount = target_amount * (1 + amount_range)
    
    similar_txs = filter_transactions(
        df,
        currency=currency,
        min_amount=min_amount,
        max_amount=max_amount,
    )
    
    if len(similar_txs) == 0:
        return {
            "found": False,
            "message": "没有找到类似交易数据",
        }
    
    # 分析各通道在这个金额范围的表现
    channel_perf = similar_txs.groupby('channel_id').agg({
        'fee_rate': 'mean',
        'amount': 'count',
    }).rename(columns={'amount': 'sample_count'})
    
    # 找最低费率的通道
    if len(channel_perf) > 0:
        best_channel = channel_perf['fee_rate'].idxmin()
        best_rate = channel_perf.loc[best_channel, 'fee_rate']
        sample_count = channel_perf.loc[best_channel, 'sample_count']
        
        return {
            "found": True,
            "best_channel": best_channel,
            "channel_name": PAYMENT_CHANNELS.get(best_channel, {}).get('name', best_channel),
            "avg_fee_rate": round(best_rate, 4),
            "sample_count": int(sample_count),
            "estimated_fee": round(target_amount * best_rate, 2),
        }
    
    return {"found": False, "message": "数据不足"}


# ==============================================================================
# 学习小结
# ==============================================================================
"""
【本模块学到的内容】

1. DataFrame创建:
   pd.DataFrame(字典或列表)

2. 数据选择:
   df['列名']           # 选择列
   df[['列1', '列2']]   # 选择多列
   df[条件]             # 筛选行
   df.iloc[0]           # 按位置选择
   df.loc['标签']       # 按标签选择

3. 分组聚合:
   df.groupby('列名').agg({
       '列1': 'sum',
       '列2': ['mean', 'count'],
   })

4. 透视表:
   pd.pivot_table(df, index=, columns=, values=, aggfunc=)

5. 排序:
   df.sort_values('列名', ascending=False)

6. 基本统计:
   df.describe()
   df['列名'].mean() / sum() / count() / min() / max()

【练习建议】
1. 添加按日期分析的功能
2. 实现异常交易检测（费率异常高的交易）
3. 添加环比/同比分析功能
"""


# ==============================================================================
# 模块测试代码
# ==============================================================================

if __name__ == "__main__":
    # 演示DataFrame基础
    demonstrate_dataframe_basics()
    
    # 生成测试数据
    print("\n" + "=" * 60)
    print("数据分析测试")
    print("=" * 60)
    
    # 导入数据生成模块
    from _04_data_generator import generate_transactions
    
    # 生成测试数据
    print("\n生成测试数据...")
    transactions = generate_transactions(count=200)
    
    # 转换为DataFrame
    df = transactions_to_dataframe(transactions)
    print(f"\n数据形状: {df.shape}")
    print(f"列: {list(df.columns)}")
    
    # 查看前几行
    print(f"\n前5条数据:")
    print(df[['transaction_id', 'currency', 'channel_id', 'amount', 'fee']].head())
    
    # 筛选测试
    print("\n【筛选测试 - USD交易】")
    usd_df = filter_transactions(df, currency='USD')
    print(f"  USD交易数: {len(usd_df)}")
    
    # 分组分析
    print("\n【按通道分析】")
    channel_summary = analyze_by_channel(df)
    print(channel_summary[['channel_name', 'transaction_count', 'total_amount', 'avg_fee_rate']].to_string())
    
    # 费率对比
    print("\n【费率对比分析】")
    fee_comparison = analyze_fee_comparison(df)
    print(fee_comparison[['channel_name', 'tx_count', 'avg_fee_rate']].to_string())
    
    # 汇总统计
    print("\n【汇总统计】")
    stats = calculate_summary_statistics(df)
    print(f"  总交易数: {stats['total_transactions']}")
    print(f"  总金额: {stats['total_amount']:.2f}")
    print(f"  总费用: {stats['total_fee']:.2f}")
    print(f"  成功率: {stats.get('success_rate', 0):.2%}")
