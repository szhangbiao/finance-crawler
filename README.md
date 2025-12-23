# finance-crawler

Finance crawler 基于`AKShare`库来爬取金融消息，沪深指数和黄金价格等数据。

## 功能特性

当前支持的数据源：

### 📰 新闻资讯

1. **百度财经日历** (`news_economic_baidu`)
   - 获取全球经济事件、数据发布时间表
   - 包含：日期、时间、地区、事件、公布值、预期值、前值、重要性等级

2. **央视新闻联播** (`news_cctv`)
   - 获取央视新闻联播文字稿
   - 包含：日期、标题、内容

3. **期货新闻** (`futures_news_shmet`)
   - 获取上海金属网实时期货新闻
   - 包含：发布时间、内容

### 📊 研究与报告

4. **东方财富研究报告** (`stock_research_report_em`)
   - 获取最新股票研究报告
   - 包含：股票代码、报告名称、评级、机构、盈利预测、报告PDF链接

### 📈 交易提示

5. **停牌提示** (`news_trade_notify_suspend_baidu`)
   - 获取股票停牌复牌信息
   - 包含：股票代码、停牌时间、复牌时间、停牌事项说明、市值

6. **分红提示** (`news_trade_notify_dividend_baidu`)
   - 获取股票分红送股信息
   - 包含：股票代码、除权日、分红、送股、转增

7. **财报时间表** (`news_report_time_baidu`)
   - 获取上市公司财报发布时间表
   - 包含：股票代码、财报类型、发布时间、市值

### 🔍 个股信息

8. **东方财富个股新闻** (`stock_news_em`)
   - 获取指定股票的最新新闻资讯
   - 包含：关键词、新闻标题、新闻内容、发布时间、文章来源、新闻链接

### 🥇 贵金属数据

9. **上海黄金交易所行情** (`spot_quotations_sge`, `spot_hist_sge`)
   - 获取实时行情和历史数据
   - 支持品种：Au99.99, Ag(T+D) 等


## 使用 uv 进行开发

本项目使用 [uv](https://github.com/astral-sh/uv) 进行包管理。

### 安装依赖

```bash
uv sync
```

### 运行程序

```bash
uv run src/main.py
```

### 添加新依赖

```bash
uv add <package_name>
```

