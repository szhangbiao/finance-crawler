---
trigger: always_on
glob: "**/*"
alwaysApply: true
---

# finance-crawler 项目开发规则

## 核心约束

### 技术栈 (不可更改)
- **Python版本**: 必须使用 Python 3.13+
- **包管理器**: 只能使用 `uv`,禁止使用 pip/poetry
- **数据源**: 只能使用 AKShare 库,不引入其他金融数据源
- **数据处理**: 使用 pandas 处理数据

### 项目结构 (严格遵守)
```
src/collectors/    # 所有采集器必须放这里
tests/            # 所有测试文件必须放这里  
docs/             # 所有文档必须放这里
```

---

## 代码规范 (强制执行)

### 1. 采集器实现规则

**必须遵循的模式**:
```python
class XxxCollector:
    """采集器必须以Collector结尾"""
    
    def __init__(self):
        """必须有初始化方法"""
        self.name = "collector_name"
    
    def get_xxx(self) -> pd.DataFrame:
        """
        - 方法名必须以 get_ 开头
        - 必须返回 pd.DataFrame 或 Dict
        - 必须包含完整的docstring
        """
        try:
            # 调用AKShare接口
            df = ak.some_interface()
            return df
        except Exception as e:
            # 必须捕获并处理异常
            print(f"Error: {e}")
            return pd.DataFrame()  # 失败时返回空DataFrame
```

**禁止的做法**:
- ❌ 不要使用其他数据源库
- ❌ 不要在采集器中做复杂的数据处理
- ❌ 不要忽略异常处理
- ❌ 不要在采集器中写死配置参数

### 2. 命名规范 (严格)

**类名**: 
- 采集器: `XxxCollector` (必须以Collector结尾)
- 其他类: `PascalCase`

**方法名**:
- 获取数据: `get_xxx()` (必须以get_开头)
- 分析数据: `analyze_xxx()`
- 打印输出: `print_xxx()`

**变量名**:
- DataFrame: `df`, `xxx_df`, `result_df`
- 字典: `xxx_dict`, `xxx_data`
- 采集器实例: `collector`

### 3. 错误处理 (强制)

**所有对外方法必须有错误处理**:
```python
def get_data(self):
    try:
        result = ak.some_api()
        if result is not None and len(result) > 0:
            return result
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in get_data: {e}")
        return pd.DataFrame()
```

**不允许**:
- ❌ 裸露的 API 调用(不加try-except)
- ❌ 传播异常到上层(除非明确设计)
- ❌ 静默失败(不打印错误信息)

### 4. 文档规范

**每个采集器方法必须包含**:
```python
def get_data(self) -> pd.DataFrame:
    """
    方法功能简述
    
    Returns:
        DataFrame: 返回数据说明
    
    Example:
        >>> collector = Collector()
        >>> df = collector.get_data()
    """
```

---

## 开发流程规则

### 添加新采集器时必须:

1. ✅ 在 `src/collectors/` 创建新文件
2. ✅ 实现采集器类,遵循命名和结构规范
3. ✅ 在 `src/collectors/__init__.py` 中导入和导出
4. ✅ 创建测试文件 `tests/test_xxx.py`
5. ✅ 创建文档 `docs/` (API文档或使用指南)

### 修改现有代码时必须:

1. ✅ 保持向后兼容
2. ✅ 更新相关文档
3. ✅ 测试修改后的功能
4. ✅ 保持代码风格一致

---

## AKShare 使用规则

### 接口调用模式

**标准模式** (必须遵循):
```python
import akshare as ak

# 1. 无参数接口
df = ak.interface_name()

# 2. 有参数接口  
df = ak.interface_name(symbol="代码", period="日")

# 3. 必须有错误处理
try:
    df = ak.interface_name()
except Exception as e:
    print(f"Error: {e}")
    df = pd.DataFrame()
```

**禁止**:
- ❌ 不要硬编码接口参数
- ❌ 不要假设接口永远可用
- ❌ 不要忽略数据验证

---

## 已实现的采集器清单

### 必须了解以下采集器的功能和用法:

1. **GlobalIndexCollector** - 全球股指 (56+国家)
   - get_all_indices() - 所有指数
   - get_us_indices() - 美国
   - get_asian_indices() - 亚洲(含港股)
   - get_market_sentiment() - 市场情绪

2. **SentimentIndexCollector** - 市场情绪
   - get_fear_greed_index() - 恐慌指数
   - get_market_activity() - 活跃度
   - get_comprehensive_sentiment() - 综合分析

3. **NewsCollector** - 新闻采集
4. **IndexCollector** - A股指数
5. **MetalsCollector** - 贵金属

### 添加新功能时:
- 先检查是否已有类似功能
- 参考现有采集器的实现模式
- 保持API设计的一致性

---

## 命令使用规则

### 只能使用以下命令:

**依赖管理**:
```bash
uv sync          # 安装依赖
uv add <pkg>     # 添加依赖
```

**运行程序**:
```bash
uv run python src/main.py
uv run python src/collectors/xxx.py
uv run python tests/test_xxx.py
```

**禁止使用**:
- ❌ `pip install` 
- ❌ `python -m pip`
- ❌ `poetry`

---

## 文件组织规则

### src/collectors/
- 每个采集器一个文件
- 文件名小写加下划线: `global_index.py`
- `__init__.py` 必须导出所有采集器

### tests/
- 测试文件: `test_xxx.py`
- 示例文件: `example_xxx.py`
- 演示文件: `demo_xxx.py`

### docs/
- API文档: `xxx_apis.md` 或 `xxx_REPORT.md`
- 使用指南: `Xxx使用指南.md`

---

## 性能和质量要求

### 代码质量:
- ✅ 所有公开方法必须有docstring
- ✅ 复杂逻辑必须有注释
- ✅ 遵循PEP 8代码风格

### 性能要求:
- ✅ 避免重复调用API
- ✅ 合理处理大数据集
- ✅ 使用 pandas 而不是循环处理数据

### 错误处理:
- ✅ 优雅降级,不崩溃
- ✅ 打印有意义的错误信息
- ✅ 返回空数据而不是抛出异常

---

## 禁止事项 (Don'ts)

### 绝对禁止:
- ❌ 修改包管理器 (必须用uv)
- ❌ 降级Python版本 (必须3.13+)
- ❌ 引入AKShare以外的金融数据源
- ❌ 在采集器中直接写文件/数据库
- ❌ 硬编码敏感信息
- ❌ 忽略错误处理

### 强烈不建议:
- ⚠️ 采集器方法过于复杂 (拆分)
- ⚠️ 单个文件超过500行 (分模块)
- ⚠️ 方法参数过多 (使用配置对象)
- ⚠️ 深层嵌套 (重构)

---

## 特殊说明

### 关于全球指数数据:
- 使用 GlobalIndexCollector
- 支持56+个国家和地区
- 包含美国、日本、香港、越南等主要市场

### 关于市场情绪:
- 使用 SentimentIndexCollector  
- QVIX指数: >40极度恐慌, <15极度贪婪
- 综合评分: 0-100分

### 关于数据更新:
- 实时数据根据交易时间更新
- 注意不同市场的时区差异
- 部分接口可能有延迟

---

**规则版本**: 1.0  
**最后更新**: 2025-12-23
