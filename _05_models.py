"""
==============================================================================
数据模型模块 (models.py)
==============================================================================

【学习目标】
本模块帮助你学习Python面向对象编程（OOP）的核心概念：
1. 类(class)的定义
2. 构造函数(__init__)
3. 实例属性和方法
4. 类的继承(inheritance)
5. 方法重写(override)
6. 特殊方法(__str__, __repr__)

【什么是面向对象编程？】
面向对象编程是一种编程范式，它将数据和操作数据的方法组织在一起，
称为"对象"。类是对象的模板或蓝图。

想象一下：
- 类(Class) = 汽车设计图
- 对象(Object) = 根据设计图制造的具体汽车
- 属性(Attribute) = 汽车的颜色、品牌、价格
- 方法(Method) = 汽车能做的事情，如启动、加速、刹车

==============================================================================
"""

# 导入需要的模块
from datetime import datetime  # 日期时间处理
from typing import List, Optional  # 类型提示（帮助理解代码，非必须）
import uuid  # 生成唯一标识符


# ==============================================================================
# 第一部分：基础类定义 - Transaction（交易记录类）
# ==============================================================================

class Transaction:
    """
    交易记录类
    
    【类的定义语法】
    class 类名:
        类的内容（属性和方法）
    
    【命名规范】
    类名使用大驼峰命名法（PascalCase）：每个单词首字母大写
    例如：Transaction, PaymentChannel, BankTransfer
    
    【文档字符串(docstring)】
    在类或函数定义后紧跟的三引号字符串，用于说明其用途
    可以通过 help(Transaction) 或 Transaction.__doc__ 查看
    """
    
    # =========================================================================
    # 构造函数 __init__
    # =========================================================================
    def __init__(
        self,
        amount: float,
        currency: str,
        channel_id: str,
        transaction_type: str = "payment"  # 默认参数
    ):
        """
        构造函数：创建对象时自动调用
        
        【参数说明】
        self: 指向对象自身的引用，必须是第一个参数
              通过self可以访问对象的属性和方法
        amount: 交易金额
        currency: 货币类型
        channel_id: 支付通道ID
        transaction_type: 交易类型，有默认值"payment"
        
        【类型提示】
        amount: float 表示amount参数期望是浮点数类型
        这只是提示，Python不会强制检查类型
        """
        
        # -----------------------------------------------------------------
        # 实例属性的定义
        # 使用 self.属性名 = 值 来定义实例属性
        # 每个对象都有自己独立的一份实例属性
        # -----------------------------------------------------------------
        
        # 生成唯一的交易ID
        # uuid.uuid4() 生成一个随机的唯一标识符
        # str() 将其转换为字符串
        # [:8] 切片操作，只取前8个字符
        self.transaction_id = str(uuid.uuid4())[:8]
        
        # 直接赋值的属性
        self.amount = amount
        self.currency = currency
        self.channel_id = channel_id
        self.transaction_type = transaction_type
        
        # 自动生成的属性
        self.created_at = datetime.now()  # 创建时间
        self.status = "pending"  # 交易状态：pending/completed/failed
        
        # 费用相关属性（初始为None，后续计算填充）
        # None 在Python中表示"空"或"没有值"
        self.fee: Optional[float] = None
        self.fee_rate: Optional[float] = None
        self.amount_cny: Optional[float] = None  # 转换后的人民币金额
        self.total_cost: Optional[float] = None  # 总成本
    
    # =========================================================================
    # 实例方法
    # =========================================================================
    def calculate_fee(self, base_rate: float, fixed_fee: float = 0) -> float:
        """
        计算交易手续费
        
        【实例方法】
        - 定义在类内部的函数称为方法
        - 第一个参数必须是self
        - 通过 对象.方法名() 来调用
        
        【参数】
        base_rate: 费率（如0.02表示2%）
        fixed_fee: 固定费用，默认为0
        
        【返回值】
        -> float 表示返回值类型是浮点数
        """
        # 费用 = 金额 × 费率 + 固定费用
        self.fee = self.amount * base_rate + fixed_fee
        self.fee_rate = base_rate
        return self.fee
    
    def set_converted_amount(self, exchange_rate: float) -> float:
        """
        设置转换后的人民币金额
        
        【参数】
        exchange_rate: 汇率（如 7.25 表示 1外币=7.25人民币）
        """
        self.amount_cny = self.amount * exchange_rate
        return self.amount_cny
    
    def complete(self) -> None:
        """
        将交易标记为完成
        
        -> None 表示这个方法不返回任何值
        """
        self.status = "completed"
        self.completed_at = datetime.now()
    
    def fail(self, reason: str = "Unknown error") -> None:
        """将交易标记为失败"""
        self.status = "failed"
        self.failure_reason = reason
    
    # =========================================================================
    # 特殊方法（魔术方法）
    # =========================================================================
    def __str__(self) -> str:
        """
        字符串表示方法
        
        【特殊方法】
        以双下划线开头和结尾的方法称为特殊方法或魔术方法
        Python在特定情况下会自动调用它们
        
        __str__ 在以下情况被调用：
        - print(对象)
        - str(对象)
        
        用于返回对象的"用户友好"的字符串表示
        """
        return f"交易[{self.transaction_id}]: {self.currency} {self.amount:.2f} via {self.channel_id}"
    
    def __repr__(self) -> str:
        """
        官方字符串表示方法
        
        __repr__ 在以下情况被调用：
        - 在交互式解释器中直接输入对象名
        - repr(对象)
        
        用于返回对象的"开发者友好"的字符串表示
        理想情况下，eval(repr(obj)) 应该能重新创建该对象
        """
        return f"Transaction(amount={self.amount}, currency='{self.currency}', channel_id='{self.channel_id}')"
    
    def to_dict(self) -> dict:
        """
        将对象转换为字典
        
        这是一个常用的模式，方便：
        - 序列化为JSON
        - 存储到数据库
        - 转换为DataFrame
        """
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "currency": self.currency,
            "channel_id": self.channel_id,
            "transaction_type": self.transaction_type,
            "status": self.status,
            "fee": self.fee,
            "fee_rate": self.fee_rate,
            "amount_cny": self.amount_cny,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }


# ==============================================================================
# 第二部分：类的继承 - PaymentChannel（支付通道基类）
# ==============================================================================

class PaymentChannel:
    """
    支付通道基类
    
    【什么是基类？】
    基类（也叫父类或超类）是其他类继承的类
    它定义了所有子类共有的属性和方法
    
    【为什么要使用继承？】
    1. 代码复用：子类自动获得父类的所有功能
    2. 统一接口：所有子类有相同的方法名，调用方式一致
    3. 多态：可以用父类类型来处理所有子类对象
    """
    
    def __init__(
        self,
        channel_id: str,
        name: str,
        base_rate: float,
        fixed_fee: float = 0,
        min_fee: float = 0,
        max_fee: float = 0,
    ):
        """初始化支付通道"""
        self.channel_id = channel_id
        self.name = name
        self.base_rate = base_rate
        self.fixed_fee = fixed_fee
        self.min_fee = min_fee
        self.max_fee = max_fee
        self.channel_type = "base"  # 通道类型，子类会重写
        self.supported_currencies: List[str] = []  # 支持的货币列表
    
    def calculate_fee(self, amount: float) -> float:
        """
        计算手续费
        
        这是一个基础实现，子类可以重写（override）这个方法
        """
        # 基础费用 = 金额 × 费率 + 固定费用
        fee = amount * self.base_rate + self.fixed_fee
        
        # 应用最低和最高收费限制
        if self.min_fee > 0 and fee < self.min_fee:
            fee = self.min_fee
        if self.max_fee > 0 and fee > self.max_fee:
            fee = self.max_fee
        
        return fee
    
    def is_currency_supported(self, currency: str) -> bool:
        """检查是否支持指定货币"""
        return currency in self.supported_currencies
    
    def get_fee_rate_display(self) -> str:
        """获取费率的显示文本"""
        return f"{self.base_rate:.2%}"  # 格式化为百分比
    
    def __str__(self) -> str:
        return f"{self.name} ({self.channel_type}): {self.get_fee_rate_display()}"


# ==============================================================================
# 第三部分：继承示例 - 银行通道子类
# ==============================================================================

class BankChannel(PaymentChannel):
    """
    银行通道类 - 继承自PaymentChannel
    
    【继承语法】
    class 子类名(父类名):
        子类内容
    
    【继承的效果】
    1. 子类自动拥有父类的所有属性和方法
    2. 子类可以添加新的属性和方法
    3. 子类可以重写（override）父类的方法
    """
    
    def __init__(
        self,
        channel_id: str,
        name: str,
        base_rate: float,
        fixed_fee: float = 0,
        min_fee: float = 0,
        max_fee: float = 0,
        processing_days: int = 3,
        swift_code: str = None,
    ):
        """
        银行通道构造函数
        
        【super()函数】
        super() 返回父类的代理对象，用于调用父类的方法
        super().__init__(...) 调用父类的构造函数
        这样可以复用父类的初始化逻辑
        """
        # 调用父类的构造函数
        super().__init__(
            channel_id=channel_id,
            name=name,
            base_rate=base_rate,
            fixed_fee=fixed_fee,
            min_fee=min_fee,
            max_fee=max_fee,
        )
        
        # 银行通道特有的属性
        self.channel_type = "bank"  # 重写父类的属性
        self.processing_days = processing_days
        self.swift_code = swift_code
        
        # 银行通道通常支持这些货币
        self.supported_currencies = ["USD", "EUR", "GBP", "JPY", "HKD"]
    
    def calculate_fee(self, amount: float) -> float:
        """
        重写父类的费用计算方法
        
        【方法重写(Override)】
        子类可以定义与父类同名的方法，这称为重写
        调用时会执行子类的版本，而不是父类的
        
        银行通道的特殊逻辑：大额交易可能有折扣
        """
        # 先调用父类的计算方法
        base_fee = super().calculate_fee(amount)
        
        # 银行通道特殊逻辑：超过5万的交易，额外打9折
        if amount > 50000:
            base_fee = base_fee * 0.9
        
        return base_fee
    
    def get_processing_info(self) -> str:
        """银行通道特有的方法"""
        return f"预计到账时间: {self.processing_days}个工作日"


# ==============================================================================
# 第四部分：另一个子类 - 电子钱包通道
# ==============================================================================

class WalletChannel(PaymentChannel):
    """
    电子钱包通道类 - 继承自PaymentChannel
    
    展示不同子类如何有不同的特性和行为
    """
    
    def __init__(
        self,
        channel_id: str,
        name: str,
        base_rate: float,
        fixed_fee: float = 0,
        instant_transfer: bool = True,
        cashback_rate: float = 0,
    ):
        """电子钱包通道构造函数"""
        # 调用父类构造函数
        super().__init__(
            channel_id=channel_id,
            name=name,
            base_rate=base_rate,
            fixed_fee=fixed_fee,
            min_fee=0,  # 钱包通道通常没有最低收费
            max_fee=0,  # 也没有最高收费上限
        )
        
        # 钱包通道特有的属性
        self.channel_type = "wallet"
        self.instant_transfer = instant_transfer  # 是否即时到账
        self.cashback_rate = cashback_rate  # 返现比例
        
        # 钱包通常支持更多货币
        self.supported_currencies = ["USD", "EUR", "GBP", "JPY", "HKD", "SGD", "PHP"]
    
    def calculate_fee(self, amount: float) -> float:
        """钱包通道的费用计算"""
        # 基础费用
        fee = amount * self.base_rate + self.fixed_fee
        
        # 如果有返现，扣除返现金额
        if self.cashback_rate > 0:
            cashback = amount * self.cashback_rate
            fee = fee - cashback
            # 确保费用不会变成负数
            fee = max(fee, 0)
        
        return fee
    
    def get_transfer_speed(self) -> str:
        """获取转账速度描述"""
        if self.instant_transfer:
            return "即时到账"
        else:
            return "1-2小时内到账"


# ==============================================================================
# 第五部分：卡通道子类
# ==============================================================================

class CardChannel(PaymentChannel):
    """银行卡通道类"""
    
    def __init__(
        self,
        channel_id: str,
        name: str,
        base_rate: float,
        fixed_fee: float = 0,
        min_fee: float = 0,
        max_fee: float = 0,
        card_types: List[str] = None,
    ):
        """银行卡通道构造函数"""
        super().__init__(
            channel_id=channel_id,
            name=name,
            base_rate=base_rate,
            fixed_fee=fixed_fee,
            min_fee=min_fee,
            max_fee=max_fee,
        )
        
        self.channel_type = "card"
        # 如果没有传入card_types，使用默认值
        # 这里展示了处理可变默认参数的正确方式
        self.card_types = card_types if card_types else ["visa", "mastercard", "unionpay"]
        self.supported_currencies = ["USD", "EUR", "GBP", "JPY", "HKD", "SGD"]


# ==============================================================================
# 第六部分：工厂函数 - 创建通道对象的便捷方法
# ==============================================================================

def create_channel_from_config(channel_id: str, config: dict) -> PaymentChannel:
    """
    工厂函数：根据配置创建对应类型的通道对象
    
    【工厂模式】
    这是一种常见的设计模式
    通过一个函数来创建对象，而不是直接使用类
    好处：调用者不需要知道具体使用哪个类
    
    【参数】
    channel_id: 通道ID
    config: 通道配置字典（来自config.py）
    
    【返回】
    对应类型的PaymentChannel子类实例
    """
    channel_type = config.get("type", "base")
    
    # 根据类型创建不同的对象
    if channel_type == "bank":
        return BankChannel(
            channel_id=channel_id,
            name=config["name"],
            base_rate=config["base_rate"],
            fixed_fee=config.get("fixed_fee", 0),
            min_fee=config.get("min_fee", 0),
            max_fee=config.get("max_fee", 0),
            processing_days=config.get("processing_days", 3),
        )
    elif channel_type == "wallet":
        return WalletChannel(
            channel_id=channel_id,
            name=config["name"],
            base_rate=config["base_rate"],
            fixed_fee=config.get("fixed_fee", 0),
            instant_transfer=config.get("processing_days", 1) <= 1,
        )
    elif channel_type == "card":
        return CardChannel(
            channel_id=channel_id,
            name=config["name"],
            base_rate=config["base_rate"],
            fixed_fee=config.get("fixed_fee", 0),
            min_fee=config.get("min_fee", 0),
            max_fee=config.get("max_fee", 0),
        )
    else:
        # 默认返回基类
        return PaymentChannel(
            channel_id=channel_id,
            name=config["name"],
            base_rate=config["base_rate"],
            fixed_fee=config.get("fixed_fee", 0),
        )


# ==============================================================================
# 学习小结
# ==============================================================================
"""
【本模块学到的内容】

1. 类的基本结构：
   class 类名:
       def __init__(self, 参数):
           self.属性 = 值
       def 方法(self):
           方法体

2. 核心概念：
   - self: 对象自身的引用
   - __init__: 构造函数，创建对象时自动调用
   - 实例属性: self.属性名 定义的属性
   - 实例方法: 类中定义的函数

3. 继承:
   class 子类(父类):
       pass
   - 子类继承父类的所有属性和方法
   - super() 用于调用父类的方法

4. 方法重写:
   - 子类可以重新定义父类的方法
   - 调用时会执行子类的版本

5. 特殊方法:
   - __str__: 定义print(对象)时的输出
   - __repr__: 定义对象的官方字符串表示

【练习建议】
1. 创建一个Transaction对象，调用它的方法
2. 创建不同类型的PaymentChannel，比较它们的费用计算
3. 尝试添加一个新的通道子类，如CryptoChannel（加密货币通道）
"""


# ==============================================================================
# 模块测试代码
# ==============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("测试Transaction类")
    print("=" * 60)
    
    # 创建交易对象
    tx = Transaction(
        amount=1000,
        currency="USD",
        channel_id="alipay_global"
    )
    
    # 测试打印（会调用__str__方法）
    print(f"交易对象: {tx}")
    
    # 测试方法
    fee = tx.calculate_fee(base_rate=0.02)
    print(f"手续费: {fee:.2f}")
    
    tx.set_converted_amount(exchange_rate=7.25)
    print(f"人民币金额: {tx.amount_cny:.2f}")
    
    # 测试to_dict
    print(f"\n转换为字典:")
    for key, value in tx.to_dict().items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("测试PaymentChannel继承")
    print("=" * 60)
    
    # 创建不同类型的通道
    bank = BankChannel(
        channel_id="swift",
        name="SWIFT国际汇款",
        base_rate=0.015,
        fixed_fee=30,
        min_fee=80,
        max_fee=800,
        processing_days=5
    )
    
    wallet = WalletChannel(
        channel_id="alipay",
        name="支付宝国际",
        base_rate=0.02,
        instant_transfer=True
    )
    
    # 测试多态：相同的方法调用，不同的行为
    test_amount = 10000
    print(f"\n测试金额: {test_amount}")
    print(f"{bank.name} 费用: {bank.calculate_fee(test_amount):.2f}")
    print(f"{wallet.name} 费用: {wallet.calculate_fee(test_amount):.2f}")
    
    # 测试大额交易（银行有折扣）
    large_amount = 100000
    print(f"\n大额测试: {large_amount}")
    print(f"{bank.name} 费用: {bank.calculate_fee(large_amount):.2f} (含大额折扣)")
    print(f"{wallet.name} 费用: {wallet.calculate_fee(large_amount):.2f}")
