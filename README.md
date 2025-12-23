# finance-crawler

## 项目概述

**项目名称**: finance-crawler  
**项目类型**: 金融数据采集程序  
**核心技术**: Python 3.13 + AKShare  
**包管理器**: uv  
**主要用途**: 采集金融市场数据,包括新闻、指数、情绪指标、贵金属等

---

## 项目架构

### 目录结构

```
finance-crawler/
├── .agent/                    # Agent配置文件
│   └── rules/
│       └── project-rules.md   # 项目规则文档 (本文件)
├── docs/                      # 项目文档
│   ├── AKSHARE_NEWS_APIS.md           # 新闻接口文档
│   ├── GLOBAL_INDEX_REPORT.md         # 全球指数调查报告
│   ├── GlobalIndexCollector使用指南.md # 全球指数采集器使用指南
│   ├── SENTIMENT_INDEX_REPORT.md      # 情绪指数调查报告
│   └── sentiment_index_apis.md        # 情绪指数接口文档
├── src/                       # 源代码
│   ├── collectors/            # 数据采集器模块
│   │   ├── __init__.py        # 导出所有采集器
│   │   ├── news.py            # 新闻采集器
│   │   ├── indices.py         # A股指数采集器
│   │   ├── global_index.py    # 全球指数采集器
│   │   ├── sentiment.py       # 情绪指数采集器
│   │   └── metals.py          # 贵金属采集器
│   └── main.py                # 主程序入口
├── tests/                     # 测试和示例文件
├── pyproject.toml             # 项目配置和依赖
└── README.md                  # 项目README
```

---

## 开发规范

### 1. 代码风格

- **遵循 PEP 8** 代码风格指南
- **使用类型注解**: 为函数参数和返回值添加类型提示
- **文档字符串**: 每个类和公共方法必须有docstring
- **命名规范**:
  - 类名: PascalCase (例: GlobalIndexCollector)
  - 函数/方法: snake_case (例: get_all_indices)
  - 常量: UPPER_SNAKE_CASE

### 2. 采集器开发规范

#### 采集器类命名
- 统一后缀: Collector
- 例如: NewsCollector, GlobalIndexCollector, SentimentIndexCollector

#### 采集器必备方法
1. __init__(): 初始化方法,设置采集器名称
2. 主要数据获取方法: 返回 pd.DataFrame 或 Dict
3. 错误处理: 所有方法必须包含 try-except 块
4. 返回空值: 出错时返回空DataFrame或包含error信息的Dict

---

## 数据采集器详解

### 已实现的采集器

#### 1. GlobalIndexCollector (全球指数采集器) ⭐
**文件**: src/collectors/global_index.py  
**功能**: 采集全球56+个国家和地区的股指数据  
**主要方法**:
- get_all_indices() - 获取所有全球指数
- get_us_indices() - 美国指数
- get_asian_indices() - 亚洲指数 (包括港股)
- get_market_sentiment() - 全球市场情绪分析

#### 2. SentimentIndexCollector (情绪指数采集器) ⭐
**文件**: src/collectors/sentiment.py  
**功能**: 采集市场情绪相关指标  
**主要方法**:
- get_fear_greed_index() - 恐慌贪婪指数
- get_market_activity() - 市场活跃度
- get_comprehensive_sentiment() - 综合情绪分析

#### 3. NewsCollector (新闻采集器)
**文件**: src/collectors/news.py  
**功能**: 采集各类财经新闻和资讯

#### 4. IndexCollector (A股指数采集器)
**文件**: src/collectors/indices.py  
**功能**: 采集A股各类指数数据

#### 5. MetalsCollector (贵金属采集器)
**文件**: src/collectors/metals.py  
**功能**: 采集贵金属价格数据

---

## 开发工作流

### 运行和测试

```bash
# 安装依赖
uv sync

# 运行主程序
uv run python src/main.py

# 运行测试
uv run python tests/test_*.py

# 直接测试采集器
uv run python src/collectors/global_index.py
```

### 添加新依赖

```bash
uv add package_name
```

---

## 最佳实践

### 错误处理
```python
try:
    df = ak.some_interface()
    if df is not None and len(df) > 0:
        return df
    return pd.DataFrame()
except Exception as e:
    print(f"Error: {e}")
    return pd.DataFrame()
```

---

**最后更新**: 2025-12-23  
**项目版本**: 0.1.0  
**Python版本**: 3.13+

