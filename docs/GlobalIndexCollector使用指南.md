# GlobalIndexCollector 使用指南

## 简介

`GlobalIndexCollector` 是一个全球股指数据采集器,支持获取56+个国家和地区的股指实时行情数据。

## 快速开始

### 基础使用

```python
from src.collectors import GlobalIndexCollector

# 创建采集器实例
collector = GlobalIndexCollector()

# 获取所有全球指数
df = collector.get_all_indices()
print(df.head())
```

## 主要功能

### 1. 获取全部指数

```python
# 获取全球56+个指数的实时行情
df = collector.get_all_indices()
```

**返回字段**:
- `序号`: 序号
- `代码`: 指数代码
- `名称`: 指数名称
- `最新价`: 最新价格
- `涨跌额`: 涨跌金额
- `涨跌幅`: 涨跌百分比
- `开盘价`: 开盘价
- `最高价`: 最高价
- `最低价`: 最低价
- `昨收价`: 昨日收盘价
- `振幅`: 振幅百分比
- `最新行情时间`: 更新时间

### 2. 按地区获取指数

#### 美国市场

```python
# 获取美国主要指数 (标普500, 道琼斯, 纳斯达克)
us_data = collector.get_us_indices()
print(us_data[['名称', '最新价', '涨跌幅']])
```

#### 亚洲市场

```python
# 获取亚洲主要指数 (日经225, 恒生, 韩国综合等)
asia_data = collector.get_asian_indices()
print(asia_data[['名称', '最新价', '涨跌幅']])
```

#### 欧洲市场

```python
# 获取欧洲主要指数 (富时100, DAX, CAC40等)
europe_data = collector.get_european_indices()
print(europe_data[['名称', '最新价', '涨跌幅']])
```

### 3. 获取特定指数

```python
# 获取标普500
sp500 = collector.get_index_by_name('标普500')
if sp500 is not None:
    print(f"标普500: {sp500['最新价']}, 涨跌幅: {sp500['涨跌幅']}%")

# 获取恒生指数
hsi = collector.get_index_by_name('恒生')
print(f"恒生指数: {hsi['最新价']}")

# 获取日经225
nikkei = collector.get_index_by_name('日经225')
print(f"日经225: {nikkei['最新价']}")
```

### 4. 市场情绪分析

```python
# 获取全球市场整体情绪
sentiment = collector.get_market_sentiment()

if sentiment['success']:
    print(f"市场情绪: {sentiment['sentiment']}")
    print(f"上涨占比: {sentiment['rising_pct']}%")
    print(f"平均涨跌幅: {sentiment['avg_change']}%")
```

**返回数据**:
```python
{
    'success': True,
    'total': 56,              # 总指数数量
    'rising': 37,             # 上涨数量
    'falling': 19,            # 下跌数量
    'flat': 0,                # 持平数量
    'rising_pct': 66.07,      # 上涨百分比
    'falling_pct': 33.93,     # 下跌百分比
    'avg_change': 0.17,       # 平均涨跌幅
    'sentiment': '乐观',       # 市场情绪
    'sentiment_level': 'bullish'  # 情绪等级
}
```

### 5. 涨跌幅排行榜

```python
# 获取涨幅前10名
top10 = collector.get_top_performers(10)
print(top10[['名称', '涨跌幅', '最新价']])

# 获取跌幅前10名
bottom10 = collector.get_bottom_performers(10)
print(bottom10[['名称', '涨跌幅', '最新价']])
```

### 6. 完整市场概况

```python
# 打印完整的市场概况报告
collector.print_market_summary()
```

**输出示例**:
```
================================================================================
                                全球市场实时概况                                    
================================================================================

【市场情绪】: 乐观 (bullish)
总指数数: 56
上涨: 37 (66.07%)
下跌: 19 (33.93%)
平均涨跌幅: 0.17%

--------------------------------------------------------------------------------
美国市场
--------------------------------------------------------------------------------
       名称      最新价    涨跌额   涨跌幅
    标普500  6881.16   2.67  0.04
     纳斯达克 23444.59  15.76  0.07
      道琼斯 48265.82 -96.86 -0.20
...
```

## 支持的国家和地区

### 美洲
- 🇺🇸 美国: 标普500, 道琼斯, 纳斯达克
- 🇨🇦 加拿大: S&P/TSX综合指数
- 🇧🇷 巴西: BOVESPA
- 🇲🇽 墨西哥: BOLSA

### 亚洲
- 🇯🇵 日本: 日经225
- 🇭🇰 香港: 恒生指数
- 🇹🇼 台湾: 台湾加权
- 🇰🇷 韩国: 首尔综合指数
- 🇮🇳 印度: 孟买SENSEX
- 🇻🇳 越南: 越南胡志明
- 🇸🇬 新加坡: 富时新加坡海峡时报
- 🇮🇩 印度尼西亚: 雅加达综合
- 🇹🇭 泰国
- 🇲🇾 马来西亚

### 欧洲
- 🇬🇧 英国: 富时100
- 🇩🇪 德国: DAX指数
- 🇫🇷 法国: CAC40
- 🇮🇹 意大利: MIB指数
- 🇪🇸 西班牙: IBEX
- 🇳🇱 荷兰: AEX综合
- 🇨🇭 瑞士
- 🇷🇺 俄罗斯: RTS, MICEX

### 大洋洲
- 🇦🇺 澳大利亚: 标普200
- 🇳🇿 新西兰: NZSE 50

### 其他
- 🇪🇬 埃及: CASE 30
- 波罗的海BDI指数
- 路透CRB商品指数

**总计**: 56+ 个全球主要股指

## 实用示例

### 示例1: 监控大中华区市场

```python
collector = GlobalIndexCollector()
df = collector.get_all_indices()

# 筛选大中华区指数
china_keywords = '上证|深证|恒生|香港|台湾'
china_indices = df[df['名称'].str.contains(china_keywords, na=False)]

print("大中华区市场:")
print(china_indices[['名称', '最新价', '涨跌幅']])
```

### 示例2: 对比主要经济体

```python
collector = GlobalIndexCollector()

# 美国
us = collector.get_index_by_name('标普500')
# 欧洲
eu = collector.get_index_by_name('DAX')
# 日本
jp = collector.get_index_by_name('日经225')
# 中国
cn = collector.get_index_by_name('恒生')

print(f"美国 标普500: {us['涨跌幅']}%")
print(f"欧洲 DAX: {eu['涨跌幅']}%")
print(f"日本 日经225: {jp['涨跌幅']}%")
print(f"香港 恒生: {cn['涨跌幅']}%")
```

### 示例3: 全球市场热度分析

```python
collector = GlobalIndexCollector()
sentiment = collector.get_market_sentiment()

if sentiment['rising_pct'] > 60:
    print("🔥 全球市场火热,大多数指数上涨!")
elif sentiment['rising_pct'] < 40:
    print("❄️ 全球市场低迷,大多数指数下跌!")
else:
    print("➡️ 全球市场中性,涨跌参半")
```

## 运行示例

### 命令行测试

```bash
# 测试采集器
uv run python src/collectors/global_index.py

# 运行完整示例
uv run python tests/example_global_index.py
```

### Python 脚本

```python
from src.collectors import GlobalIndexCollector

collector = GlobalIndexCollector()

# 打印市场概况
collector.print_market_summary()
```

## API 参考

### 类: GlobalIndexCollector

#### 方法

| 方法 | 说明 | 返回类型 |
|------|------|---------|
| `get_all_indices()` | 获取所有全球指数 | DataFrame |
| `get_index_name_table()` | 获取指数名称表 | DataFrame |
| `get_us_indices()` | 获取美国指数 | DataFrame |
| `get_asian_indices()` | 获取亚洲指数 | DataFrame |
| `get_european_indices()` | 获取欧洲指数 | DataFrame |
| `get_index_by_name(name)` | 获取特定指数 | Series or None |
| `get_market_sentiment()` | 获取市场情绪 | Dict |
| `get_top_performers(n)` | 获取涨幅榜 | DataFrame |
| `get_bottom_performers(n)` | 获取跌幅榜 | DataFrame |
| `print_market_summary()` | 打印市场概况 | None |

## 注意事项

1. **数据更新频率**: 实时行情数据,根据各市场交易时间更新
2. **时区**: 注意各国市场的交易时间和时区差异
3. **数据源**: 东方财富 (AKShare)
4. **网络要求**: 需要网络连接以获取最新数据

## 更多示例

完整的使用示例请参考: `tests/example_global_index.py`

## 相关文档

- [AKShare 全球股指调查报告](../docs/GLOBAL_INDEX_REPORT.md)
- [测试文件](../tests/test_global_index.py)
