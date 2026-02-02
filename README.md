# 跨境支付费率分析系统

> 一个面向Python初学者的实战学习项目

## 📖 项目简介

这是一个专为Python初学者设计的学习项目，通过模拟跨境支付费率分析的真实业务场景，帮助你掌握Python核心编程概念。

### 🎯 学习目标

完成本项目后，你将掌握：

| Python概念 | 对应模块 | 学习内容 |
|-----------|---------|---------|
| 变量和数据类型 | `config.py` | 字符串、数字、列表、字典 |
| 函数定义 | `utils.py` | 参数、返回值、文档字符串 |
| 条件判断 | `rate_calculator.py` | if/elif/else、比较运算符 |
| 循环结构 | `data_generator.py` | for循环、while循环、列表推导式 |
| 面向对象 | `models.py` | 类、继承、方法、构造函数 |
| 数据处理 | `analyzer.py` | pandas DataFrame操作 |
| 数据可视化 | `visualizer.py` | matplotlib图表绑制 |
| 文件操作 | `report_generator.py` | Excel文件读写 |

## 🚀 快速开始

### 1. 环境准备

```powershell
# 进入项目目录
cd c:\Users\Admin\.gemini\antigravity\playground\chrono-exoplanet

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行程序

```powershell
# 运行完整分析流程
python main.py

# 或者指定交易数量
python main.py 500

# 交互模式
python main.py -i
```

### 3. 查看结果

程序运行后会生成：
- `output/charts/` - 可视化图表（PNG格式）
- `output/reports/` - Excel分析报表

## 📁 项目结构

```
chrono-exoplanet/
├── _01_config.py            # ① 配置文件 - 学习变量和数据类型
├── _02_utils.py             # ② 工具函数 - 学习函数定义
├── _03_rate_calculator.py   # ③ 费率计算 - 学习条件判断
├── _04_data_generator.py    # ④ 数据生成 - 学习循环结构
├── _05_models.py            # ⑤ 数据模型 - 学习面向对象编程
├── _06_analyzer.py          # ⑥ 数据分析 - 学习pandas
├── _07_visualizer.py        # ⑦ 可视化 - 学习matplotlib
├── _08_report_generator.py  # ⑧ 报表生成 - 学习文件操作
├── _09_main.py              # ⑨ 主程序入口 ⭐ 最后阅读
├── requirements.txt         # 依赖包列表
└── output/                  # 输出目录
    ├── charts/              # 图表文件
    └── reports/             # 报表文件
```

## 📚 学习路线建议

### 阶段一：Python基础（第1-3天）

1. **`_01_config.py`** - 从这里开始
   - 理解变量的定义和赋值
   - 学习基本数据类型：str, int, float, bool
   - 掌握列表(list)和字典(dict)

2. **`_02_utils.py`** - 函数入门
   - 学习函数的定义和调用
   - 理解参数和返回值
   - 了解异常处理(try/except)

### 阶段二：控制流程（第4-5天）

3. **`_03_rate_calculator.py`** - 条件判断
   - 掌握if/elif/else语句
   - 学习比较和逻辑运算符
   - 理解嵌套条件

4. **`_04_data_generator.py`** - 循环结构
   - 掌握for循环和range()
   - 学习while循环
   - 理解列表推导式

### 阶段三：面向对象（第6-7天）

5. **`_05_models.py`** - 类与对象
   - 理解类的定义(class)
   - 学习构造函数(__init__)
   - 掌握继承和方法重写

### 阶段四：实用库（第8-10天）

6. **`_06_analyzer.py`** - 数据分析
   - 学习pandas DataFrame
   - 掌握数据筛选和分组
   - 理解聚合操作

7. **`_07_visualizer.py`** - 数据可视化
   - 学习matplotlib基础
   - 掌握常见图表类型
   - 了解图表美化

8. **`_08_report_generator.py`** - 文件操作
   - 学习openpyxl库
   - 掌握Excel读写
   - 了解单元格样式

## 🔍 代码阅读技巧

每个模块都包含：

1. **文件头注释** - 说明学习目标
2. **概念解释** - 首次使用时详细说明
3. **代码示例** - 展示用法
4. **学习小结** - 总结要点
5. **测试代码** - 可直接运行验证

### 单独测试模块

每个模块都可以单独运行测试：

```powershell
# 按顺序测试各模块
python _01_config.py
python _02_utils.py
python _03_rate_calculator.py
python _04_data_generator.py
python _05_models.py
python _06_analyzer.py
python _07_visualizer.py
python _08_report_generator.py

# 运行完整程序
python _09_main.py
```

## 💡 练习建议

### 入门练习

1. 在`config.py`中添加一个新的支付通道
2. 修改汇率配置，添加新货币
3. 调整阶梯费率规则

### 进阶练习

1. 在`models.py`中添加新的通道子类
2. 在`data_generator.py`中添加新的数据分布
3. 在`analyzer.py`中添加日期分析功能

### 挑战练习

1. 添加数据持久化（保存/读取JSON）
2. 实现Web界面展示分析结果
3. 添加自动化测试用例

## 🛠️ 常见问题

### Q: 中文显示乱码怎么办？

在`visualizer.py`中已设置中文字体，如果仍有问题，请确保系统已安装"SimHei"或"Microsoft YaHei"字体。

### Q: 模块导入报错？

确保在项目根目录下运行命令，且已安装所有依赖：
```powershell
pip install -r requirements.txt
```

### Q: 如何了解更多pandas/matplotlib？

推荐资源：
- [pandas官方文档](https://pandas.pydata.org/docs/)
- [matplotlib教程](https://matplotlib.org/stable/tutorials/)

## 📝 版本信息

- 版本：1.0.0
- Python要求：3.8+
- 作者：AI学习助手

## 📄 许可证

本项目仅供学习使用。

---

**祝你学习愉快！** 🎉

有问题随时在代码中添加`print()`语句来调试，这是最简单有效的学习方法！
