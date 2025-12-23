# AKShare 股市情绪指数接口文档

## 概述

本文档总结了 AKShare 中可用的股市情绪指数相关数据接口,用于分析市场情绪、恐慌程度和活跃度等指标。

---

## 1. ✅ 市场活跃度指数 (推荐) ⭐⭐⭐⭐⭐

### 接口名称
`stock_market_activity_legu`

### 数据来源
乐咕 (Legu)

### 接口说明
获取当日股市的整体活跃度数据,包括涨跌家数、涨跌停统计、活跃度百分比等。

### 返回字段
| 字段 | 类型 | 说明 |
|------|------|------|
| item | object | 指标名称 |
| value | float64 | 指标值 |

### 数据示例
```
       item   value
0        上涨  1476.0
1        涨停    68.0
2      真实涨停    57.0
3  st st*涨停    14.0
4        下跌  3603.0
5        跌停    77.0
6      真实跌停    61.0
7   st st*跌停     6.0
8         平盘    84.0
9         停牌    15.0
10       活跃度  28.51%
11      统计日期  2025-12-23 15:00:00
```

### 使用方法
```python
import akshare as ak

# 获取当日市场活跃度数据
df = ak.stock_market_activity_legu()
print(df)

# 转换为字典便于查询
data_dict = dict(zip(df['item'], df['value']))
rise_count = data_dict['上涨']
fall_count = data_dict['下跌']
activity = data_dict['活跃度']

print(f"上涨: {rise_count}, 下跌: {fall_count}, 活跃度: {activity}")
```

### 应用场景
- 评估当日市场整体情绪(涨多跌少 vs 涨少跌多)
- 监控极端情况(涨跌停家数)
- 计算市场活跃度指标
- 作为量化策略的市场环境过滤器

---

## 2. ✅ 50ETF期权波动率指数 (恐慌指数) ⭐⭐⭐⭐⭐

### 接口名称
`index_option_50etf_qvix`

### 数据来源
上海证券交易所

### 接口说明
获取 50ETF 期权波动率指数(QVIX),也被称为"中国版恐慌指数"。该指数类似于美国的 VIX 指数,反映市场对未来30天波动率的预期。

### 指数解读
- **QVIX > 40**: 市场出现非理性恐慌,短期内可能反弹
- **QVIX 30-40**: 市场情绪悲观,波动较大
- **QVIX 20-30**: 市场略有担忧,正常偏恐慌
- **QVIX 15-20**: 市场情绪健康,正常区间
- **QVIX < 15**: 市场出现非理性繁荣,可能伴随回调风险

### 返回字段
| 字段 | 类型 | 说明 |
|------|------|------|
| date | object | 日期 |
| open | float64 | 开盘值 |
| high | float64 | 最高值 |
| low | float64 | 最低值 |
| close | float64 | 收盘值 |

### 数据范围
- 历史数据: 约2600+条记录 (2015年至今)
- 更新频率: 每交易日

### 使用方法
```python
import akshare as ak

# 获取50ETF期权波动率指数
df = ak.index_option_50etf_qvix()
print(df.tail(10))  # 查看最近10天数据

# 计算当前恐慌程度
latest_qvix = df.iloc[-1]['close']
if latest_qvix > 40:
    print("⚠️ 市场极度恐慌!")
elif latest_qvix < 15:
    print("⚠️ 市场极度贪婪,警惕回调!")
else:
    print("✓ 市场情绪正常")
```

### 应用场景
- 判断市场恐慌/贪婪程度
- 识别极端情绪的反转机会
- 风险管理和仓位控制
- 期权交易策略制定

---

## 3. ⚠️ A股新闻情绪指数 (部分可用)

### 接口名称
`index_news_sentiment_scope`

### 数据来源
数库科技 (ChinaScope) 联合 J.P. Morgan 亚太量化研究团队

### 接口说明
基于自然语言处理(NLP)技术,对每日数十万篇财经新闻进行情绪识别,构建的A股新闻情绪指数。

### 返回字段
| 字段 | 类型 | 说明 |
|------|------|------|
| 日期 | object | 日期 |
| 市场情绪指数 | float64 | 市场情绪指数值 |
| 沪深300指数 | float64 | 沪深300指数值 |

### 数据范围
- 近一年的数据

### 当前状态
⚠️ **接口存在问题**: 测试时返回数据解析错误,可能是:
1. 数据源临时不可用
2. API 接口发生变化
3. 需要额外的认证或参数

### 使用方法
```python
import akshare as ak

try:
    # 获取A股新闻情绪指数
    df = ak.index_news_sentiment_scope()
    print(df.head())
except Exception as e:
    print(f"接口暂时不可用: {e}")
```

### 应用场景
- 结合新闻情绪判断市场方向
- 验证技术分析信号
- 构建多因子量化模型

---

## 推荐使用组合

### 组合1: 实时情绪监控
```python
import akshare as ak

# 1. 获取市场活跃度(当日)
activity = ak.stock_market_activity_legu()
active_rate = activity[activity['item'] == '活跃度']['value'].values[0]

# 2. 获取恐慌指数(最新)
qvix = ak.index_option_50etf_qvix()
fear_index = qvix.iloc[-1]['close']

print(f"市场活跃度: {active_rate}")
print(f"恐慌指数: {fear_index}")

# 3. 综合判断
if fear_index > 40 and float(active_rate.rstrip('%')) < 30:
    print("⚠️ 市场极度恐慌且成交低迷,可能是底部信号")
elif fear_index < 15 and float(active_rate.rstrip('%')) > 50:
    print("⚠️ 市场极度贪婪且成交活跃,注意风险")
```

### 组合2: 历史情绪分析
```python
import akshare as ak
import pandas as pd

# 获取历史恐慌指数
qvix_df = ak.index_option_50etf_qvix()

# 分析极端情绪出现频率
extreme_fear = qvix_df[qvix_df['close'] > 40]
extreme_greed = qvix_df[qvix_df['close'] < 15]

print(f"极端恐慌天数: {len(extreme_fear)}")
print(f"极端贪婪天数: {len(extreme_greed)}")

# 分析当前处于什么位置
current_qvix = qvix_df.iloc[-1]['close']
percentile = (qvix_df['close'] < current_qvix).sum() / len(qvix_df) * 100
print(f"当前QVIX处于历史 {percentile:.1f}% 分位")
```

---

## 总结

### 可用接口对比

| 接口 | 状态 | 更新频率 | 适用场景 | 推荐度 |
|------|------|----------|----------|--------|
| stock_market_activity_legu | ✅ 可用 | 每日 | 短线择时、市场温度 | ⭐⭐⭐⭐⭐ |
| index_option_50etf_qvix | ✅ 可用 | 每日 | 风险控制、极端情绪识别 | ⭐⭐⭐⭐⭐ |
| index_news_sentiment_scope | ⚠️ 问题 | 每日 | 新闻驱动策略 | ⭐⭐⭐ |

### 建议
1. **主要使用**: `stock_market_activity_legu` + `index_option_50etf_qvix`
2. **定期检查**: `index_news_sentiment_scope` 接口可用性
3. **辅助参考**: 结合成交量、换手率等传统指标

### 实战应用

#### 情绪择时策略
```python
def emotion_timing_strategy():
    """基于情绪指标的择时策略"""
    import akshare as ak
    
    # 获取数据
    qvix = ak.index_option_50etf_qvix().iloc[-1]['close']
    activity = ak.stock_market_activity_legu()
    data_dict = dict(zip(activity['item'], activity['value']))
    
    rise_count = int(data_dict['上涨'])
    total = rise_count + int(data_dict['下跌']) + int(data_dict['平盘'])
    rise_ratio = rise_count / total * 100
    
    # 策略逻辑
    if qvix > 40 and rise_ratio < 20:
        return "买入信号 - 极度恐慌,可能反弹"
    elif qvix < 15 and rise_ratio > 80:
        return "卖出信号 - 极度贪婪,可能回调"
    elif qvix > 30:
        return "减仓信号 - 市场恐慌"
    elif qvix < 18:
        return "警惕信号 - 市场过热"
    else:
        return "持有信号 - 情绪正常"

# 使用
signal = emotion_timing_strategy()
print(signal)
```

---

## 参考资料

- [AKShare 官方文档](https://akfamily.xyz/)
- [数库科技 - A股新闻情绪指数](https://www.chinascope.com/)
- [上海证券交易所 - 期权数据](http://www.sse.com.cn/assortment/options/price/)
- [VIX指数解读](https://www.investopedia.com/terms/v/vix.asp)

---

## 相关采集器

已实现的情绪指数采集器: `src/collectors/sentiment_index_collector.py`

使用方法:
```python
from src.collectors import SentimentIndexCollector

collector = SentimentIndexCollector()

# 获取最新恐慌贪婪指数
fear_greed = collector.get_latest_fear_greed()
print(f"当前情绪: {fear_greed['emotion']}")

# 获取市场活跃度分析
activity = collector.get_market_activity_analysis()
print(f"市场情绪: {activity['emotion']}")

# 获取综合情绪分析
comprehensive = collector.get_comprehensive_sentiment()
print(f"综合评分: {comprehensive['comprehensive_score']}")

# 打印完整报告
collector.print_sentiment_report()
```

---

**最后更新**: 2025-12-23
