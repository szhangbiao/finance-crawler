# AKShare 全球股指数据接口调查报告

## 📋 调查总结

AKShare **完全支持**获取美国、日本、印度、越南等国家的股指数据!

---

## ✅ 可用接口

### 1. **index_global_spot_em** - 全球指数实时行情 ⭐⭐⭐⭐⭐

**功能**: 获取全球主要股指的实时行情数据

**数据来源**: 东方财富

**支持国家/地区**: 56+ 个全球指数

**返回字段**:
```python
['序号', '代码', '名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '最高价', '最低价', '昨收价', '振幅', '最新行情时间']
```

**使用示例**:
```python
import akshare as ak

# 获取全球指数实时行情
df = ak.index_global_spot_em()

# 查看美国主要指数
usa_data = df[df['名称'].str.contains('标普|道琼斯|纳斯达克', na=False)]
print(usa_data[['名称', '最新价', '涨跌额', '涨跌幅']])

# 查看日本指数
japan_data = df[df['名称'].str.contains('日经', na=False)]
print(japan_data[['名称', '最新价', '涨跌额', '涨跌幅']])

# 查看印度指数
india_data = df[df['名称'].str.contains('印度|孟买', na=False)]
print(india_data[['名称', '最新价', '涨跌额', '涨跌幅']])

# 查看越南指数
vietnam_data = df[df['名称'].str.contains('越南', na=False)]
print(vietnam_data[['名称', '最新价', '涨跌额', '涨跌幅']])
```

**实测结果** (2025-12-23):
```
美国主要指数实时行情:
           名称       最新价     涨跌额   涨跌幅       开盘价       昨收价
9       标普500   6878.49   43.99  0.64   6865.21   6834.50
13       纳斯达克  23428.83  121.21  0.52  23450.53  23307.62
14        道琼斯  48362.68  227.79  0.47  48211.88  48134.89

日本主要指数实时行情:
       名称       最新价    涨跌额   涨跌幅       开盘价       昨收价
31  日经225  50412.87  10.48  0.02  50374.48  50402.39

印度主要指数实时行情:
            名称       最新价    涨跌额   涨跌幅       开盘价       昨收价
37  印度孟买SENSEX  85524.84 -42.64 -0.05  85599.94  85567.48

越南主要指数实时行情:
      名称      最新价    涨跌额   涨跌幅      开盘价      昨收价
3  越南胡志明  1772.15  21.12  1.21  1751.03  1751.03
```

---

### 2. **index_global_name_table** - 全球指数名称表

**功能**: 获取全球指数的名称和代码映射表

**支持国家/地区**: 20+ 个主要国家和地区

**返回字段**:
```python
['指数名称', '代码']
```

**包含的指数**:
- 🇬🇧 英国: 富时100指数
- 🇩🇪 德国: DAX 30指数
- 🇫🇷 法国: CAC40指数
- 🇯🇵 日本: 日经225指数
- 🇮🇳 印度: 孟买SENSEX指数、雅加达综合指数
- 🇨🇦 加拿大: S&P/TSX综合指数
- 🇧🇷 巴西: BOVESPA股票指数
- 🇹🇼 中国台湾: 加权指数
- 🇰🇷 韩国: 首尔综合指数
- 🇦🇺 澳大利亚: 标准普尔200指数
- 等等...

**使用示例**:
```python
import akshare as ak

# 获取全球指数名称表
df = ak.index_global_name_table()
print(df)

# 查找日本指数
japan_indices = df[df['指数名称'].str.contains('日经', na=False)]
print(japan_indices)

# 查找印度指数
india_indices = df[df['指数名称'].str.contains('印度|孟买', na=False)]
print(india_indices)
```

---

### 3. **index_global_hist_em** - 全球指数历史数据

**功能**: 获取特定指数的历史K线数据

**参数**: 
- `symbol`: 指数代码 (注意:与名称表中的代码可能不同)

**注意事项**:
- 历史数据接口使用的代码映射与名称表不同
- 建议优先使用实时行情接口
- 如需历史数据,可能需要通过其他接口获取

---

## 🌍 支持的国家和主要指数

| 国家/地区 | 支持状态 | 主要指数 | 实时数据 |
|----------|---------|---------|---------|
| 🇺🇸 美国 | ✅ | 标普500, 道琼斯, 纳斯达克 | ✅ |
| 🇯🇵 日本 | ✅ | 日经225, 东证指数 | ✅ |
| 🇮🇳 印度 | ✅ | 孟买SENSEX, Nifty50 | ✅ |
| 🇻🇳 越南 | ✅ | 越南胡志明指数 | ✅ |
| 🇨🇳 中国 | ✅ | 台湾加权指数 | ✅ |
| 🇬🇧 英国 | ✅ | 富时100 | ✅ |
| 🇩🇪 德国 | ✅ | DAX指数 | ✅ |
| 🇫🇷 法国 | ✅ | CAC40 | ✅ |
| 🇨🇦 加拿大 | ✅ | S&P/TSX综合指数 | ✅ |
| 🇧🇷 巴西 | ✅ | BOVESPA | ✅ |
| 🇰🇷 韩国 | ✅ | 首尔综合指数 | ✅ |
| 🇦🇺 澳大利亚 | ✅ | 标普200 | ✅ |

**总计**: 56+ 个全球主要股指,覆盖美洲、欧洲、亚洲、大洋洲等地区

---

## 💡 实用示例

### 示例1: 监控全球主要市场
```python
import akshare as ak
import pandas as pd

def get_global_markets_summary():
    """获取全球主要市场概况"""
    df = ak.index_global_spot_em()
    
    # 筛选主要市场
    major_markets = ['标普500', '道琼斯', '纳斯达克', '日经225', 
                    '印度孟买SENSEX', '越南胡志明', '富时100', 'DAX']
    
    result = []
    for market in major_markets:
        市值data = df[df['名称'].str.contains(market, na=False)]
        if len(market_data) > 0:
            result.append(market_data.iloc[0])
    
    summary = pd.DataFrame(result)
    return summary[['名称', '最新价', '涨跌幅', '最新行情时间']]

# 使用
summary = get_global_markets_summary()
print(summary)
```

### 示例2: 亚洲市场对比
```python
import akshare as ak

def compare_asian_markets():
    """对比亚洲主要市场表现"""
    df = ak.index_global_spot_em()
    
    # 筛选亚洲市场
    asian_markets = df[df['名称'].str.contains(
        '日经|韩国|印度|越南|新加坡|台湾|香港', 
        na=False
    )]
    
    # 按涨跌幅排序
    result = asian_markets.sort_values('涨跌幅', ascending=False)
    return result[['名称', '最新价', '涨跌额', '涨跌幅']]

# 使用
print(compare_asian_markets())
```

### 示例3: 全球市场情绪指标
```python
import akshare as ak

def global_market_sentiment():
    """计算全球市场情绪"""
    df = ak.index_global_spot_em()
    
    total = len(df)
    rising = len(df[df['涨跌幅'] > 0])
    falling = len(df[df['涨跌幅'] < 0])
    
    sentiment_score = rising / total * 100
    
    return {
        '总指数数量': total,
        '上涨数量': rising,
        '下跌数量': falling,
        '上涨占比': f'{sentiment_score:.2f}%',
        '市场情绪': '乐观' if sentiment_score > 50 else '悲观'
    }

# 使用
print(global_market_sentiment())
```

---

## 🎯 应用场景

### 1. 全球市场监控
- 实时跟踪美国、欧洲、亚洲主要市场
- 构建全球市场仪表板
- 监控跨市场联动

### 2. 跨市场分析
- 对比不同国家股市表现
- 分析区域市场关联性
- 识别全球资金流向

### 3. 投资决策辅助
- 海外市场投资参考
- QDII基金跟踪
- 避险资产配置

### 4. 数据研究
- 全球市场相关性研究
- 跨市场套利机会发现
- 宏观经济指标关联分析

---

## 📝 已创建的工具

### 测试脚本
📁 `/Users/szhangbiao/Projects/python/finance-crawler/tests/test_global_index.py`

**功能**:
- 获取并显示全球指数名称表
- 获取美国、日本、印度、越南等国家指数实时行情
- 验证接口可用性

**运行**:
```bash
uv run python tests/test_global_index.py
```

---

## ⚠️ 注意事项

1. **数据更新频率**: 实时行情数据根据交易时间更新
2. **时区问题**: 注意各国市场的交易时间和时区差异
3. **代码映射**: 历史数据接口的代码与名称表可能不一致
4. **数据完整性**: 部分指数在非交易时段可能数据不更新

---

## 🎉 总结

### 核心优势
✅ **全面覆盖**: 56+ 个全球主要股指  
✅ **实时更新**: 提供最新的市场行情  
✅ **易于使用**: 简单的 API 调用  
✅ **数据丰富**: 包含开高低收、涨跌幅等完整数据  

### 推荐使用
主要使用 `index_global_spot_em()` 接口,可以满足:
- ✅ 美国股指监控 (标普500, 道琼斯, 纳斯达克)
- ✅ 日本股指监控 (日经225)
- ✅ 印度股指监控 (孟买SENSEX)
- ✅ 越南股指监控 (越南胡志明)
- ✅ 其他50+个全球主要市场

**完全满足你的需求!** 🎯
