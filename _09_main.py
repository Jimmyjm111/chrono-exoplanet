"""
==============================================================================
主程序入口 (main.py)
==============================================================================

【学习目标】
本模块帮助你学习Python程序的组织结构：
1. 模块导入和组织
2. if __name__ == "__main__" 的作用
3. 程序流程控制
4. 命令行参数处理（简单示例）
5. 错误处理和程序优雅退出

【什么是程序入口？】
main.py 通常是Python项目的主入口文件
它负责：
- 导入其他模块
- 协调各模块的调用
- 提供用户交互界面

==============================================================================
"""

# ==============================================================================
# 模块导入
# ==============================================================================

# 标准库导入（Python自带的库）
import sys
import os
from datetime import datetime

# 第三方库导入
import pandas as pd

# 项目模块导入（我们自己写的模块）
# 使用 from ... import ... 语法导入特定函数/类
from _01_config import (
    PROJECT_NAME,
    VERSION,
    DEFAULT_TRANSACTION_COUNT,
    PAYMENT_CHANNELS,
)

from _05_models import Transaction, create_channel_from_config

from _04_data_generator import (
    generate_transactions,
    transactions_to_dicts,
)

from _03_rate_calculator import (
    compare_channel_fees,
    find_cheapest_channel,
)

from _06_analyzer import (
    transactions_to_dataframe,
    analyze_by_channel,
    analyze_by_currency,
    calculate_summary_statistics,
    create_fee_rate_matrix,
    filter_transactions,
)

from _07_visualizer import (
    create_fee_rate_bar_chart,
    create_volume_pie_chart,
    create_heatmap,
    create_channel_summary_chart,
)

from _08_report_generator import create_fee_analysis_report

from _02_utils import ensure_directory_exists


# ==============================================================================
# 主要功能函数
# ==============================================================================

def print_header():
    """打印程序头信息"""
    print("=" * 70)
    print(f"  {PROJECT_NAME}")
    print(f"  版本: {VERSION}")
    print(f"  运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


def print_section(title: str):
    """打印分节标题"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}")


def run_data_generation(count: int = None) -> pd.DataFrame:
    """
    运行数据生成步骤
    
    【返回】
    生成的交易数据DataFrame
    """
    print_section("步骤1: 生成模拟交易数据")
    
    if count is None:
        count = DEFAULT_TRANSACTION_COUNT
    
    print(f"  正在生成 {count} 条模拟交易数据...")
    
    # 生成交易
    transactions = generate_transactions(count=count)
    
    # 转换为DataFrame
    df = transactions_to_dataframe(transactions)
    
    print(f"  ✓ 数据生成完成")
    print(f"  ✓ 数据形状: {df.shape[0]} 行 × {df.shape[1]} 列")
    
    return df


def run_basic_analysis(df: pd.DataFrame) -> dict:
    """
    运行基础分析
    
    【返回】
    包含各种分析结果的字典
    """
    print_section("步骤2: 数据分析")
    
    results = {}
    
    # 计算汇总统计
    print("  计算汇总统计...")
    results['summary'] = calculate_summary_statistics(df)
    
    # 按通道分析
    print("  按通道分析...")
    results['channel_analysis'] = analyze_by_channel(df)
    
    # 按货币分析
    print("  按货币分析...")
    results['currency_analysis'] = analyze_by_currency(df)
    
    # 费率矩阵
    print("  生成费率矩阵...")
    results['fee_matrix'] = create_fee_rate_matrix(df)
    
    # 保存原始数据引用
    results['raw_data'] = df
    
    print("  ✓ 分析完成")
    
    return results


def display_summary(analysis_results: dict):
    """
    显示分析摘要
    """
    print_section("步骤3: 分析结果摘要")
    
    summary = analysis_results.get('summary', {})
    
    # 基本统计
    print("\n  【基本统计】")
    print(f"    总交易笔数: {summary.get('total_transactions', 0):,}")
    print(f"    总交易金额: {summary.get('total_amount', 0):,.2f}")
    print(f"    总人民币金额: {summary.get('total_amount_cny', 0):,.2f} CNY")
    print(f"    总手续费: {summary.get('total_fee', 0):,.2f}")
    print(f"    平均交易金额: {summary.get('avg_amount', 0):,.2f}")
    print(f"    交易成功率: {summary.get('success_rate', 0):.1%}")
    
    # 通道分析
    print("\n  【各通道费率对比】")
    channel_df = analysis_results.get('channel_analysis')
    if channel_df is not None:
        # 按费率排序
        sorted_df = channel_df.sort_values('avg_fee_rate')
        
        print(f"    {'通道名称':<15} {'交易数':>8} {'总金额':>12} {'平均费率':>10}")
        print(f"    {'-' * 50}")
        
        for _, row in sorted_df.iterrows():
            name = row.get('channel_name', row.get('channel_id', 'N/A'))
            count = row.get('transaction_count', 0)
            amount = row.get('total_amount', 0)
            rate = row.get('avg_fee_rate', 0)
            print(f"    {name:<15} {count:>8} {amount:>12,.0f} {rate:>9.2%}")
    
    # 推荐通道
    print("\n  【费率最低的通道】")
    if channel_df is not None and len(channel_df) > 0:
        best = channel_df.loc[channel_df['avg_fee_rate'].idxmin()]
        print(f"    推荐: {best.get('channel_name', 'N/A')}")
        print(f"    平均费率: {best.get('avg_fee_rate', 0):.2%}")


def run_visualization(analysis_results: dict) -> list:
    """
    运行可视化生成
    
    【返回】
    生成的图表文件路径列表
    """
    print_section("步骤4: 生成可视化图表")
    
    chart_paths = []
    
    channel_df = analysis_results.get('channel_analysis')
    fee_matrix = analysis_results.get('fee_matrix')
    
    if channel_df is not None:
        # 费率对比柱状图
        print("  生成费率对比图...")
        path = create_fee_rate_bar_chart(channel_df)
        chart_paths.append(path)
        
        # 交易量饼图
        print("  生成交易量分布图...")
        path = create_volume_pie_chart(channel_df)
        chart_paths.append(path)
        
        # 通道汇总组合图
        print("  生成通道汇总图...")
        path = create_channel_summary_chart(channel_df)
        chart_paths.append(path)
    
    if fee_matrix is not None:
        # 费率热力图
        print("  生成费率热力图...")
        path = create_heatmap(fee_matrix)
        chart_paths.append(path)
    
    print(f"  ✓ 共生成 {len(chart_paths)} 个图表")
    
    return chart_paths


def run_report_generation(analysis_results: dict) -> str:
    """
    运行报表生成
    
    【返回】
    生成的报表文件路径
    """
    print_section("步骤5: 生成Excel报表")
    
    print("  生成费率分析报表...")
    report_path = create_fee_analysis_report(analysis_results)
    
    print(f"  ✓ 报表生成完成")
    
    return report_path


def print_completion_message(chart_paths: list, report_path: str):
    """
    打印完成信息
    """
    print_section("完成")
    
    print("\n  所有任务已完成！生成的文件：")
    
    print("\n  【图表文件】")
    for path in chart_paths:
        print(f"    • {path}")
    
    print("\n  【报表文件】")
    print(f"    • {report_path}")
    
    print("\n  您可以：")
    print("    1. 打开 output/charts/ 目录查看生成的图表")
    print("    2. 打开 output/reports/ 目录查看Excel报表")
    print("    3. 修改 _01_config.py 调整支付通道配置")
    print("    4. 阅读各模块源码学习Python概念")
    
    print("\n" + "=" * 70)
    print("  感谢使用！祝学习愉快！")
    print("=" * 70)


# ==============================================================================
# 交互式菜单（可选功能）
# ==============================================================================

def interactive_mode():
    """
    交互式模式：让用户选择要执行的操作
    
    【while循环 + input()】
    这是一个典型的交互式菜单实现
    """
    print_header()
    
    while True:
        print("\n请选择操作：")
        print("  1. 运行完整分析流程")
        print("  2. 仅生成测试数据")
        print("  3. 费率对比查询")
        print("  4. 查看通道配置")
        print("  0. 退出程序")
        
        # input()函数获取用户输入
        choice = input("\n请输入选项 (0-4): ").strip()
        
        if choice == "0":
            print("\n再见！")
            break
        
        elif choice == "1":
            # 运行完整流程
            try:
                count = input("请输入要生成的交易数量 (直接回车使用默认值1000): ").strip()
                count = int(count) if count else DEFAULT_TRANSACTION_COUNT
                main(count)
            except ValueError:
                print("  错误：请输入有效的数字")
        
        elif choice == "2":
            # 仅生成数据
            try:
                count = input("请输入要生成的交易数量: ").strip()
                count = int(count) if count else 100
                df = run_data_generation(count)
                print(f"\n数据预览（前5行）：")
                print(df[['transaction_id', 'currency', 'channel_id', 'amount', 'fee']].head())
            except ValueError:
                print("  错误：请输入有效的数字")
        
        elif choice == "3":
            # 费率查询
            amount = input("请输入交易金额: ").strip()
            currency = input("请输入货币 (USD/EUR/GBP等): ").strip().upper()

            if not amount or not currency:
                print("  错误：金额和货币均不能为空")
                continue

            try:
                amount = float(amount)
                if amount <= 0:
                    print("  错误：交易金额必须大于0")
                    continue

                result = find_cheapest_channel(amount, currency)

                if result:
                    print(f"\n  推荐通道: {result['channel_name']}")
                    print(f"  预估费率: {result['avg_fee_rate']:.2%}")
                    print(f"  预估费用: {result['estimated_fee']:.2f}")
                else:
                    print("  未找到合适的通道")
            except ValueError:
                print("  错误：请输入有效的金额")
        
        elif choice == "4":
            # 查看配置
            print("\n当前支付通道配置：")
            print(f"  {'通道ID':<20} {'名称':<15} {'类型':<8} {'费率':>8}")
            print(f"  {'-' * 55}")
            for channel_id, config in PAYMENT_CHANNELS.items():
                print(f"  {channel_id:<20} {config['name']:<15} "
                      f"{config['type']:<8} {config['base_rate']:>7.2%}")
        
        else:
            print("  无效选项，请重新输入")


# ==============================================================================
# 主函数
# ==============================================================================

def main(transaction_count: int = None):
    """
    主函数：执行完整的分析流程
    
    【参数】
    transaction_count: 要生成的交易数量（可选）
    """
    print_header()
    
    try:
        # 步骤1：生成数据
        df = run_data_generation(transaction_count)
        
        # 步骤2：分析数据
        analysis_results = run_basic_analysis(df)
        
        # 步骤3：显示摘要
        display_summary(analysis_results)
        
        # 步骤4：生成图表
        chart_paths = run_visualization(analysis_results)
        
        # 步骤5：生成报表
        report_path = run_report_generation(analysis_results)
        
        # 完成
        print_completion_message(chart_paths, report_path)
        
        return True
        
    except Exception as e:
        # 错误处理
        print(f"\n程序运行出错: {e}")
        print("请检查依赖是否已安装：pip install -r requirements.txt")
        return False


# ==============================================================================
# 程序入口
# ==============================================================================

# 这是Python程序的标准入口写法
# 当直接运行这个文件时，__name__ 的值是 "__main__"
# 当被其他模块导入时，__name__ 的值是模块名（如 "main"）

if __name__ == "__main__":
    """
    【if __name__ == "__main__" 的作用】
    
    这个条件判断确保：
    1. 直接运行 python main.py 时，执行下面的代码
    2. 被其他模块 import main 时，不执行下面的代码
    
    这样可以让模块既可以独立运行，又可以被导入使用
    """
    
    # 检查命令行参数
    # sys.argv 是命令行参数列表
    # sys.argv[0] 是脚本名称
    # sys.argv[1:] 是其他参数
    
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg == "--interactive" or arg == "-i":
            # 交互模式
            interactive_mode()
        elif arg == "--help" or arg == "-h":
            # 帮助信息
            print(f"{PROJECT_NAME} v{VERSION}")
            print("\n用法: python main.py [选项]")
            print("\n选项:")
            print("  -i, --interactive  交互式模式")
            print("  -h, --help         显示帮助信息")
            print("  <数字>             指定生成的交易数量")
            print("\n示例:")
            print("  python main.py           运行默认分析（1000条交易）")
            print("  python main.py 500       生成500条交易并分析")
            print("  python main.py -i        进入交互模式")
        else:
            # 尝试解析为数字
            try:
                count = int(arg)
                main(count)
            except ValueError:
                print(f"未知参数: {arg}")
                print("使用 python main.py --help 查看帮助")
    else:
        # 默认运行
        main()
