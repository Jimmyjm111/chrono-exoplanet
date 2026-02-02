"""
==============================================================================
可视化模块 (visualizer.py)
==============================================================================

【学习目标】
本模块帮助你学习Python数据可视化：
1. matplotlib库的基本使用
2. 各种图表类型：柱状图、折线图、饼图、热力图
3. 图表样式和配置
4. 中文显示设置
5. 保存图表到文件

【什么是matplotlib？】
matplotlib是Python最流行的绑定库，提供：
- 高度自定义的图表样式
- 支持多种图表类型
- 可保存为多种格式（PNG, PDF, SVG等）

==============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import os

# 导入项目模块
from _01_config import CHART_CONFIG, CHARTS_DIR
from _02_utils import ensure_directory_exists


# ==============================================================================
# 第一部分：matplotlib基础设置
# ==============================================================================

def setup_chinese_font():
    """
    设置中文字体
    
    【matplotlib中文显示问题】
    matplotlib默认不支持中文，需要手动设置字体
    Windows系统可以使用SimHei（黑体）
    """
    # 方法1：设置全局字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    
    # 解决负号显示问题
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置默认图表大小
    plt.rcParams['figure.figsize'] = CHART_CONFIG.get('figure_size', (12, 8))
    
    # 设置DPI
    plt.rcParams['figure.dpi'] = CHART_CONFIG.get('dpi', 100)


# 初始化时设置字体
setup_chinese_font()


def demonstrate_matplotlib_basics():
    """
    演示matplotlib基础用法
    
    【创建图表的基本步骤】
    1. 创建图形和坐标轴：plt.figure() 或 plt.subplots()
    2. 绑制数据：plt.plot(), plt.bar() 等
    3. 添加标签和标题
    4. 显示或保存图表
    """
    print("【matplotlib基础演示】")
    
    # 创建示例数据
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    
    # 创建图形
    # figsize参数设置图表大小（宽, 高），单位是英寸
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 绑制折线图
    # plot()函数用于绑制折线图
    # marker参数设置数据点标记
    # linestyle参数设置线型
    ax.plot(x, y, marker='o', linestyle='-', color='blue', label='示例数据')
    
    # 添加标题和标签
    ax.set_title('matplotlib基础示例', fontsize=14)
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    
    # 添加图例
    ax.legend()
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 关闭图形（不显示）
    plt.close(fig)
    
    print("  基础图表创建完成（未显示）")


# ==============================================================================
# 第二部分：柱状图 - 费率对比
# ==============================================================================

def create_fee_rate_bar_chart(
    data: pd.DataFrame,
    save_path: str = None,
    title: str = "各通道费率对比",
) -> str:
    """
    创建费率对比柱状图
    
    【柱状图适用场景】
    - 比较不同类别的数值大小
    - 显示排名和差异
    
    【参数】
    data: 包含channel_name和avg_fee_rate列的DataFrame
    save_path: 保存路径（可选）
    title: 图表标题
    
    【返回】
    保存的文件路径
    """
    # 准备数据
    channels = data['channel_name'].tolist()
    rates = data['avg_fee_rate'].tolist()
    
    # 获取配色方案
    colors = CHART_CONFIG.get('color_palette', ['#2E86AB'])
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 创建柱状图
    # bar()函数参数：
    # - x: x轴位置
    # - height: 柱子高度
    # - color: 颜色
    # - edgecolor: 边框颜色
    bars = ax.bar(
        range(len(channels)),  # x位置
        [r * 100 for r in rates],  # 转换为百分比
        color=colors[0],
        edgecolor='white',
        linewidth=0.5,
    )
    
    # 在柱子上显示数值
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax.annotate(
            f'{rate:.2%}',  # 显示的文本
            xy=(bar.get_x() + bar.get_width() / 2, height),  # 位置
            xytext=(0, 3),  # 偏移
            textcoords="offset points",
            ha='center',  # 水平对齐
            va='bottom',  # 垂直对齐
            fontsize=10,
        )
    
    # 设置x轴标签
    ax.set_xticks(range(len(channels)))
    ax.set_xticklabels(channels, rotation=45, ha='right')
    
    # 设置标题和标签
    ax.set_title(title, fontsize=CHART_CONFIG.get('title_fontsize', 16), pad=20)
    ax.set_xlabel('支付通道', fontsize=CHART_CONFIG.get('label_fontsize', 12))
    ax.set_ylabel('平均费率 (%)', fontsize=CHART_CONFIG.get('label_fontsize', 12))
    
    # 添加网格（只显示水平线）
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)  # 网格线在柱子下面
    
    # 调整布局
    plt.tight_layout()
    
    # 保存或显示
    if save_path is None:
        ensure_directory_exists(CHARTS_DIR)
        save_path = os.path.join(CHARTS_DIR, "fee_rate_comparison.png")
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"  费率对比图已保存: {save_path}")
    return save_path


# ==============================================================================
# 第三部分：饼图 - 交易量分布
# ==============================================================================

def create_volume_pie_chart(
    data: pd.DataFrame,
    group_by: str = 'channel_name',
    value_column: str = 'total_amount',
    save_path: str = None,
    title: str = "交易量分布",
) -> str:
    """
    创建交易量分布饼图
    
    【饼图适用场景】
    - 显示各部分占总体的比例
    - 适合3-7个类别的数据
    
    【参数】
    data: 包含分组和数值列的DataFrame
    group_by: 分组列名
    value_column: 数值列名
    """
    # 准备数据
    labels = data[group_by].tolist()
    values = data[value_column].tolist()
    
    # 获取配色方案
    colors = CHART_CONFIG.get('color_palette', plt.cm.Set3.colors)
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 创建饼图
    # pie()函数参数：
    # - x: 数据
    # - labels: 标签
    # - autopct: 显示百分比的格式
    # - startangle: 起始角度
    # - explode: 突出显示某个扇区
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',  # 显示1位小数的百分比
        startangle=90,  # 从12点方向开始
        colors=colors[:len(labels)],
        explode=[0.02] * len(labels),  # 轻微分离
        shadow=False,
        textprops={'fontsize': 10},
    )
    
    # 设置百分比文字样式
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # 设置标题
    ax.set_title(title, fontsize=CHART_CONFIG.get('title_fontsize', 16), pad=20)
    
    # 确保饼图是圆的
    ax.axis('equal')
    
    # 保存
    if save_path is None:
        ensure_directory_exists(CHARTS_DIR)
        save_path = os.path.join(CHARTS_DIR, "volume_distribution.png")
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"  交易量分布图已保存: {save_path}")
    return save_path


# ==============================================================================
# 第四部分：折线图 - 费率趋势
# ==============================================================================

def create_trend_line_chart(
    data: pd.DataFrame,
    x_column: str,
    y_columns: List[str],
    labels: List[str] = None,
    save_path: str = None,
    title: str = "费率趋势分析",
) -> str:
    """
    创建趋势折线图
    
    【折线图适用场景】
    - 显示数据随时间的变化趋势
    - 比较多条数据线的走势
    
    【参数】
    data: 数据DataFrame
    x_column: x轴数据列
    y_columns: y轴数据列列表
    labels: 每条线的标签
    """
    # 获取配色
    colors = CHART_CONFIG.get('color_palette', plt.cm.tab10.colors)
    
    # 如果没有提供标签，使用列名
    if labels is None:
        labels = y_columns
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 绘制每条数据线
    for i, (y_col, label) in enumerate(zip(y_columns, labels)):
        ax.plot(
            data[x_column],
            data[y_col],
            marker='o',
            markersize=6,
            linewidth=2,
            color=colors[i % len(colors)],
            label=label,
        )
    
    # 设置标题和标签
    ax.set_title(title, fontsize=CHART_CONFIG.get('title_fontsize', 16), pad=15)
    ax.set_xlabel(x_column, fontsize=CHART_CONFIG.get('label_fontsize', 12))
    ax.set_ylabel('数值', fontsize=CHART_CONFIG.get('label_fontsize', 12))
    
    # 添加图例
    ax.legend(loc='best', fontsize=10)
    
    # 添加网格
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 旋转x轴标签
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    # 保存
    if save_path is None:
        ensure_directory_exists(CHARTS_DIR)
        save_path = os.path.join(CHARTS_DIR, "trend_analysis.png")
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"  趋势分析图已保存: {save_path}")
    return save_path


# ==============================================================================
# 第五部分：热力图 - 通道货币费率矩阵
# ==============================================================================

def create_heatmap(
    data: pd.DataFrame,
    save_path: str = None,
    title: str = "费率热力图",
    fmt: str = ".2%",
) -> str:
    """
    创建热力图
    
    【热力图适用场景】
    - 显示二维矩阵数据
    - 用颜色深浅表示数值大小
    - 适合展示通道×货币的费率矩阵
    
    【参数】
    data: DataFrame（行和列分别代表两个维度）
    fmt: 数值显示格式
    """
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 准备数据
    # 将DataFrame转换为numpy数组
    matrix = data.values.astype(float)
    
    # 处理NaN值（用0替代）
    matrix = np.nan_to_num(matrix, nan=0)
    
    # 绘制热力图
    # imshow()函数用于显示矩阵数据
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    # 添加颜色条
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('费率', rotation=-90, va="bottom", fontsize=12)
    
    # 设置刻度标签
    ax.set_xticks(range(len(data.columns)))
    ax.set_yticks(range(len(data.index)))
    ax.set_xticklabels(data.columns, rotation=45, ha='right')
    ax.set_yticklabels(data.index)
    
    # 在每个格子中显示数值
    for i in range(len(data.index)):
        for j in range(len(data.columns)):
            value = matrix[i, j]
            if value != 0:  # 只显示非零值
                text_color = 'white' if value > matrix.max() * 0.5 else 'black'
                ax.text(
                    j, i, f'{value:.2%}',
                    ha='center', va='center',
                    color=text_color, fontsize=9
                )
    
    # 设置标题
    ax.set_title(title, fontsize=CHART_CONFIG.get('title_fontsize', 16), pad=15)
    ax.set_xlabel('货币', fontsize=CHART_CONFIG.get('label_fontsize', 12))
    ax.set_ylabel('支付通道', fontsize=CHART_CONFIG.get('label_fontsize', 12))
    
    plt.tight_layout()
    
    # 保存
    if save_path is None:
        ensure_directory_exists(CHARTS_DIR)
        save_path = os.path.join(CHARTS_DIR, "fee_rate_heatmap.png")
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"  热力图已保存: {save_path}")
    return save_path


# ==============================================================================
# 第六部分：组合图表
# ==============================================================================

def create_channel_summary_chart(
    channel_data: pd.DataFrame,
    save_path: str = None,
) -> str:
    """
    创建通道汇总组合图表
    
    【子图（subplots）】
    可以在一个图形中包含多个子图
    plt.subplots(nrows, ncols) 创建多行多列的子图
    
    【本图包含】
    - 左上：交易量柱状图
    - 右上：费用占比饼图
    - 左下：费率对比
    - 右下：交易金额排名
    """
    # 创建2x2子图
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    colors = CHART_CONFIG.get('color_palette', plt.cm.Set2.colors)
    
    # 子图1：交易数量柱状图
    ax1 = axes[0, 0]
    channels = channel_data['channel_name'].tolist()
    counts = channel_data['transaction_count'].tolist()
    
    ax1.barh(channels, counts, color=colors[0])
    ax1.set_title('各通道交易数量', fontsize=12)
    ax1.set_xlabel('交易数量')
    
    # 子图2：费用占比饼图
    ax2 = axes[0, 1]
    fees = channel_data['total_fee'].tolist()
    ax2.pie(fees, labels=channels, autopct='%1.1f%%', colors=colors[:len(channels)])
    ax2.set_title('费用占比', fontsize=12)
    
    # 子图3：平均费率对比
    ax3 = axes[1, 0]
    rates = [r * 100 for r in channel_data['avg_fee_rate'].tolist()]
    bars = ax3.bar(channels, rates, color=colors[1])
    ax3.set_title('平均费率对比', fontsize=12)
    ax3.set_ylabel('费率 (%)')
    ax3.set_xticks(range(len(channels)))
    ax3.set_xticklabels(channels, rotation=45, ha='right')
    
    # 在柱子上标注数值
    for bar, rate in zip(bars, channel_data['avg_fee_rate'].tolist()):
        ax3.annotate(f'{rate:.2%}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                    xytext=(0, 3), textcoords='offset points', ha='center', fontsize=9)
    
    # 子图4：交易金额排名
    ax4 = axes[1, 1]
    amounts = channel_data['total_amount'].tolist()
    sorted_data = sorted(zip(channels, amounts), key=lambda x: x[1], reverse=True)
    sorted_channels, sorted_amounts = zip(*sorted_data)
    
    ax4.barh(sorted_channels, sorted_amounts, color=colors[2])
    ax4.set_title('交易金额排名', fontsize=12)
    ax4.set_xlabel('交易金额')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存
    if save_path is None:
        ensure_directory_exists(CHARTS_DIR)
        save_path = os.path.join(CHARTS_DIR, "channel_summary.png")
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"  通道汇总图已保存: {save_path}")
    return save_path


# ==============================================================================
# 第七部分：生成所有图表
# ==============================================================================

def generate_all_charts(df: pd.DataFrame, analysis_data: dict) -> List[str]:
    """
    生成所有分析图表
    
    【参数】
    df: 原始交易数据DataFrame
    analysis_data: 分析结果数据（包含各种汇总表）
    
    【返回】
    生成的图表文件路径列表
    """
    print("\n开始生成图表...")
    chart_paths = []
    
    # 确保输出目录存在
    ensure_directory_exists(CHARTS_DIR)
    
    # 1. 费率对比柱状图
    if 'channel_summary' in analysis_data:
        path = create_fee_rate_bar_chart(
            analysis_data['channel_summary'],
            title="各支付通道费率对比"
        )
        chart_paths.append(path)
    
    # 2. 交易量分布饼图
    if 'channel_summary' in analysis_data:
        path = create_volume_pie_chart(
            analysis_data['channel_summary'],
            group_by='channel_name',
            value_column='total_amount',
            title="各通道交易量分布"
        )
        chart_paths.append(path)
    
    # 3. 费率热力图
    if 'fee_matrix' in analysis_data:
        path = create_heatmap(
            analysis_data['fee_matrix'],
            title="通道-货币费率矩阵"
        )
        chart_paths.append(path)
    
    # 4. 通道汇总组合图
    if 'channel_summary' in analysis_data:
        path = create_channel_summary_chart(analysis_data['channel_summary'])
        chart_paths.append(path)
    
    print(f"\n图表生成完成，共 {len(chart_paths)} 个文件")
    return chart_paths


# ==============================================================================
# 学习小结
# ==============================================================================
"""
【本模块学到的内容】

1. matplotlib基础:
   fig, ax = plt.subplots()  # 创建图形和坐标轴
   ax.plot(x, y)             # 绑制折线
   ax.bar(x, height)         # 绘制柱状图
   ax.pie(data)              # 绘制饼图
   plt.savefig(path)         # 保存图片
   plt.close()               # 关闭图形

2. 常用图表类型:
   - 柱状图 (bar): 比较类别数值
   - 折线图 (plot): 显示趋势变化
   - 饼图 (pie): 显示比例分布
   - 热力图 (imshow): 显示矩阵数据

3. 图表美化:
   ax.set_title()           # 设置标题
   ax.set_xlabel/ylabel()   # 设置轴标签
   ax.legend()              # 添加图例
   ax.grid()                # 添加网格
   plt.tight_layout()       # 自动调整布局

4. 子图:
   fig, axes = plt.subplots(nrows, ncols)
   axes[0, 0].plot(...)     # 访问子图

5. 中文显示:
   plt.rcParams['font.sans-serif'] = ['SimHei']
   plt.rcParams['axes.unicode_minus'] = False

【练习建议】
1. 尝试创建其他类型的图表（散点图、面积图）
2. 自定义颜色和样式
3. 添加数据标签和注释
"""


# ==============================================================================
# 模块测试代码
# ==============================================================================

if __name__ == "__main__":
    # 演示基础
    demonstrate_matplotlib_basics()
    
    print("\n" + "=" * 60)
    print("可视化模块测试")
    print("=" * 60)
    
    # 生成测试数据
    from _04_data_generator import generate_transactions
    from _06_analyzer import transactions_to_dataframe, analyze_by_channel, create_fee_rate_matrix
    
    print("\n生成测试数据...")
    transactions = generate_transactions(count=500)
    df = transactions_to_dataframe(transactions)
    
    # 生成分析数据
    channel_summary = analyze_by_channel(df)
    fee_matrix = create_fee_rate_matrix(df)
    
    print("\n生成图表...")
    
    # 费率对比图
    create_fee_rate_bar_chart(channel_summary)
    
    # 交易量饼图
    create_volume_pie_chart(channel_summary)
    
    # 热力图
    create_heatmap(fee_matrix)
    
    # 组合图
    create_channel_summary_chart(channel_summary)
    
    print("\n所有图表生成完成！")
    print(f"图表保存位置: {os.path.abspath(CHARTS_DIR)}")
