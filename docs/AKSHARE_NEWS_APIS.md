# AKShare 财经新闻接口完整清单

## ✅ 已实现的接口（7个）

### 📰 新闻资讯类

| 接口名称 | 方法名 | 数据源 | 更新频率 | 主要字段 |
|---------|--------|--------|----------|---------|
| `news_economic_baidu` | `get_economic_calendar()` | 百度财经 | 实时 | 日期、时间、地区、事件、公布、预期、前值、重要性 |
| `news_cctv` | `get_cctv_news()` | 央视新闻 | 每日 | 日期、标题、内容 |
| `futures_news_shmet` | `get_futures_news()` | 上海金属网 | 实时 | 发布时间、内容 |

### 📊 研究报告类

| 接口名称 | 方法名 | 数据源 | 更新频率 | 主要字段 |
|---------|--------|--------|----------|---------|
| `stock_research_report_em` | `get_research_reports()` | 东方财富 | 实时 | 股票代码、报告名称、评级、机构、盈利预测、PDF链接 |

### 📈 交易提示类

| 接口名称 | 方法名 | 数据源 | 更新频率 | 主要字段 |
|---------|--------|--------|----------|---------|
| `news_trade_notify_suspend_baidu` | `get_suspension_notice()` | 百度 | 实时 | 股票代码、停牌时间、复牌时间、停牌事项 |
| `news_trade_notify_dividend_baidu` | `get_dividend_notice()` | 百度 | 实时 | 股票代码、除权日、分红、送股、转增 |
| `news_report_time_baidu` | `get_earnings_calendar()` | 百度 | 实时 | 股票代码、财报类型、发布时间、市值 |

## ❌ 不可用的接口（2个）

| 接口名称 | 原因 |
|---------|------|
| `stock_news_em` | API 返回 JSON 解析错误 |
| `index_news_sentiment_scope` | API 返回 JSON 解析错误 |
| `stock_news_main_cx` | API 404 错误（财新接口已失效） |

## 📋 其他相关接口（未实现）

这些接口主要是公司公告和财务报表类，不属于新闻资讯范畴：

- `fund_announcement_*` - 基金公告系列
- `stock_balance_sheet_by_report_*` - 资产负债表
- `stock_cash_flow_sheet_by_report_*` - 现金流量表
- `stock_profit_sheet_by_report_*` - 利润表
- `stock_financial_*_report_*` - 财务报告系列
- `stock_report_*` - 报告披露系列
- `stock_notice_report` - 公告报告
- `crypto_bitcoin_hold_report` - 比特币持仓报告
- `macro_china_au_report` - 宏观经济报告

## 🎯 使用建议

### 实时新闻监控
推荐使用：
- `futures_news_shmet` - 期货市场实时新闻
- `news_economic_baidu` - 全球经济事件日历

### 投资研究
推荐使用：
- `stock_research_report_em` - 券商研究报告
- `news_cctv` - 政策新闻（央视新闻联播）

### 交易决策辅助
推荐使用：
- `news_trade_notify_suspend_baidu` - 停牌信息
- `news_trade_notify_dividend_baidu` - 分红信息
- `news_report_time_baidu` - 财报发布时间

## 📚 参考资料

- AKShare 官方文档: https://akshare.akfamily.xyz/
- GitHub 仓库: https://github.com/akfamily/akshare
