# 财经日历采集器文档 (CalendarCollector)

## 概述
`CalendarCollector` 是为 `finance-crawler` 开发的专门获取未来财经大事件、经济数据发布、央行议息会议及股指期货交割日的采集器。它整合了 AKShare 的宏观经济和新闻日历接口，并增加了自定义的衍生数据计算。

## 核心功能

### 1. 全球经济日历 (`get_economic_calendar`)
获取每日详细的经济指标发布计划。
- **数据源**: 百度财经实时数据。
- **字段**: 时间、地区、事件、预期值、前值、重要性等。

### 2. 重大事件摘要 (`get_upcoming_major_events`)
聚合未来指定天数（如 7 天）内的重大财经事件。
- **逻辑**: 自动过滤三星级（高重要性）事件，或包含“利率”、“议息”、“联储”、“非农”等关键词的事件。

### 3. A 股期指交割日 (`get_futures_delivery_dates`)
计算沪深 300 (IF)、上证 50 (IH)、中证 500 (IC) 和 中证 1000 (IM) 的交割日期。
- **逻辑**: 根据规则（每月第三个星期五）通过程序计算。
- **提示**: 实际交割日如遇法定节假日会顺延，本接口返回理论结算日。

### 4. 央行利率参考 (`get_central_bank_interest_rates`)
获取美联储、日本央行、欧洲央行等主要机构的最新利率水平和变动，作为日历背景参考。

## 使用代码示例

```python
from src.collectors import CalendarCollector

collector = CalendarCollector()

# 获取下周一的财经日历
df = collector.get_economic_calendar("20251229")
print(df.head())

# 获取未来 3 天的重大事件
major_events = collector.get_upcoming_major_events(days=3)
print(major_events[['日期', '事件', '重要性']])

# 获取未来半年的期指交割日
delivery = collector.get_futures_delivery_dates(count=6)
print(delivery)
```

## 注意事项
- **实时性**: 经济日历数据会随官方发布实时更新，建议定期抓取。
- **缺失值**: 部分未来事件的“预期值”在发布前可能为 `NaN`。
