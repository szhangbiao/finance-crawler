# AKShare 股市情绪指数调查报告

## 📋 调查总结

经过全面调查和测试,AKShare 确实提供了股市情绪指数相关的数据接口。以下是详细的调查结果:

---

## ✅ 可用的情绪指数接口

### 1. 50ETF期权波动率指数 (恐慌指数) ⭐⭐⭐⭐⭐

**接口名称**: `index_option_50etf_qvix`

**数据来源**: 上海证券交易所

**功能说明**:
- 中国版的恐慌指数,类似美国 VIX
- 反映市场对未来 30 天波动率的预期
- 历史数据丰富 (2015年至今,2600+条记录)

**返回字段**:
```python
['date', 'open', 'high', 'low', 'close']
```

**情绪解读标准**:
- **QVIX > 40**: 极度恐慌 - 市场非理性恐慌,可能短期反弹
- **QVIX 30-40**: 恐慌 - 市场情绪悲观,波动较大  
- **QVIX 20-30**: 正常偏恐慌 - 市场略有担忧
- **QVIX 15-20**: 正常 - 市场情绪健康
- **QVIX < 15**: 极度贪婪 - 市场过度乐观,警惕回调

**实测数据** (2025-12-22):
- QVIX 值: 13.89
- 情绪判断: 极度贪婪 ⚠️
- 市场解读: 市场情绪过热,需警惕回调风险

**使用示例**:
```python
import akshare as ak

# 获取历史数据
df = ak.index_option_50etf_qvix()

# 获取最新恐慌指数
latest_qvix = df.iloc[-1]['close']
print(f"当前恐慌指数: {latest_qvix}")
```

---

### 2. 市场活跃度指数 ⭐⭐⭐⭐⭐

**接口名称**: `stock_market_activity_legu`

**数据来源**: 乐咕 (Legu)

**功能说明**:
- 提供当日股市整体活跃度数据
- 包含涨跌家数、涨跌停统计、活跃度百分比
- 实时更新 (交易日 15:00 更新)

**返回字段**:
```python
['item', 'value']
```

**包含指标**:
- 上涨/下跌股票数
- 涨停/跌停股票数
- 真实涨停/跌停 (剔除 ST)
- ST 涨停/跌停数
- 平盘股票数
- 停牌股票数
- **市场活跃度** (百分比)
- 统计日期

**实测数据** (2025-12-23):
```
总股票数: 5163
上涨: 1476 (28.59%)
下跌: 3603 (69.79%)
涨停: 68 | 跌停: 16
活跃度: 28.51% (低)
市场情绪: 强烈看跌
```

**使用示例**:
```python
import akshare as ak

# 获取当日市场活跃度
df = ak.stock_market_activity_legu()

# 转换为字典便于查询
data_dict = dict(zip(df['item'], df['value']))
rise_count = data_dict['上涨']
fall_count = data_dict['下跌']
activity = data_dict['活跃度']

print(f"上涨: {rise_count}, 下跌: {fall_count}, 活跃度: {activity}")
```

---

### 3. A股新闻情绪指数 ⚠️

**接口名称**: `index_news_sentiment_scope`

**数据来源**: 数库科技 (ChinaScope) × J.P. Morgan

**功能说明**:
- 基于 NLP 分析每日数十万篇财经新闻
- 构建市场情绪指数
- 提供近一年的历史数据

**返回字段**:
```python
['日期', '市场情绪指数', '沪深300指数']
```

**当前状态**: ⚠️ **数据源不稳定**
- 测试时出现数据解析错误
- 可能是临时维护或接口变更
- 建议定期检查可用性

**使用示例**:
```python
import akshare as ak

try:
    df = ak.index_news_sentiment_scope()
    if df is not None:
        print(df.tail())
except Exception as e:
    print(f"接口暂时不可用: {e}")
```

---

## 📊 综合应用方案

### 方案 1: 双指标综合判断

结合恐慌指数 + 市场活跃度,构建综合情绪评分系统:

```python
from src.collectors.sentiment_index_collector import SentimentIndexCollector

collector = SentimentIndexCollector()

# 获取综合情绪分析
result = collector.get_comprehensive_sentiment()

if result['success']:
    print(f"综合评分: {result['comprehensive_score']}/100")
    print(f"综合情绪: {result['comprehensive_emotion']}")
    print(f"操作建议: {result['suggestion']}")
```

**评分算法**:
- 恐慌指数贡献: 60% 权重
- 市场活跃度贡献: 40% 权重
- 综合得分范围: 0-100 (0=极度悲观, 100=极度乐观)

### 方案 2: 情绪报告生成

使用已创建的采集器自动生成市场情绪报告:

```bash
# 运行情绪报告生成器
uv run python src/collectors/sentiment_index_collector.py
```

输出示例:
```
================================================================================
                                股市情绪指数报告
================================================================================

生成时间: 2025-12-23 20:29:11

【综合评分】: 50.6 分
【综合情绪】: 中性
【操作建议】: 市场情绪平稳,按既定策略操作

--------------------------------------------------------------------------------
恐慌贪婪指数 (50ETF QVIX)
--------------------------------------------------------------------------------
日期: 2025-12-22
指数值: 13.89 (开:14.31, 高:14.31, 低:13.72)
情绪: 极度贪婪 (danger)
说明: 市场出现非理性繁荣,可能伴随回调风险
建议: 注意获利了结,警惕高位风险
...
```

### 方案 3: 定时监控与预警

可以基于这些指标构建自动化监控系统:

```python
def sentiment_alert():
    """情绪指标预警"""
    collector = SentimentIndexCollector()
    
    # 恐慌指数预警
    fear_greed = collector.get_latest_fear_greed()
    if fear_greed['qvix'] > 40:
        send_alert("⚠️ 市场极度恐慌,关注反弹机会")
    elif fear_greed['qvix'] < 15:
        send_alert("⚠️ 市场极度贪婪,注意回调风险")
    
    # 活跃度预警
    activity = collector.get_market_activity_analysis()
    if activity['rise_ratio'] > 80:
        send_alert("📈 市场普涨,情绪火热")
    elif activity['fall_ratio'] > 80:
        send_alert("📉 市场普跌,情绪低迷")
```

---

## 🎯 应用场景

### 1. 短线交易择时
- **极度恐慌时** (QVIX > 40): 关注超跌反弹机会
- **极度贪婪时** (QVIX < 15): 警惕高位回调,适当减仓
- **市场普涨** (涨幅 > 70%): 追涨需谨慎
- **市场普跌** (跌幅 > 70%): 寻找优质标的逢低布局

### 2. 风险管理
- 根据恐慌指数调整仓位
- QVIX 高位: 降低仓位,控制风险
- QVIX 低位: 适度提高仓位

### 3. 量化策略过滤
- 作为量化策略的市场环境过滤器
- 在极端情绪下调整策略参数
- 避免在不利环境下开仓

### 4. 情绪背离交易
- 当恐慌指数和市场走势出现背离时,可能是转折信号
- 例如: 指数创新高但 QVIX 居高不下 → 警惕见顶

---

## 🔧 已创建的工具

### 1. 测试脚本
📁 `tests/test_sentiment_index.py`
- 测试所有情绪指数接口
- 显示数据示例和统计信息
- 运行: `uv run python tests/test_sentiment_index.py`

### 2. 采集器模块
📁 `src/collectors/sentiment_index_collector.py`
- 封装好的数据采集类
- 提供数据获取、分析、报告生成功能
- 运行: `uv run python src/collectors/sentiment_index_collector.py`

### 3. 文档
📁 `docs/sentiment_index_apis.md`
- 详细的接口文档
- 包含使用方法和应用场景

---

## 📚 参考资源

- [AKShare 官方文档](https://akfamily.xyz/)
- [数库科技 - A股新闻情绪指数](https://www.chinascope.com/)
- [上海证券交易所 - 期权数据](http://www.sse.com.cn/assortment/options/price/)

---

## 💡 建议

### 优先使用
1. ✅ `index_option_50etf_qvix` - 数据稳定,历史丰富
2. ✅ `stock_market_activity_legu` - 实时更新,信息全面

### 辅助参考
3. ⚠️ `index_news_sentiment_scope` - 定期检查可用性

### 进阶应用
- 结合成交量、换手率等传统指标
- 构建多维度的市场情绪模型
- 开发自动化预警系统

---

## 🎉 总结

AKShare 提供了**2个稳定可用**的股市情绪指数接口:

1. **恐慌贪婪指数** (50ETF QVIX) - 反映市场波动预期
2. **市场活跃度** - 反映当日市场整体情绪

这两个指标可以有效帮助你:
- ✅ 判断市场情绪极端状态
- ✅ 识别潜在的交易机会
- ✅ 优化风险管理策略
- ✅ 提升量化策略效果

建议将这些指标整合到你的交易系统中,作为重要的市场环境参考!
