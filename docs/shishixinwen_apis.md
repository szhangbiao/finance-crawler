# 实事新闻 (shishixinwen.news) 采集器文档

## 概述
`ShishixinwenCollector` 是一个专门用于采集 `shishixinwen.news` 实事新闻快讯的采集器。该源聚合了金十数据、华尔街见闻、东方财富等多家主流财经媒体的快讯，并提供 AI 深度解析、投资观点和标签化分类。

## API 参考

### `get_news(page=1, page_size=50, q=None, source=None)`
获取单页快讯数据。

**参数:**
- `page` (int): 要获取的页码，起始为 1。
- `page_size` (int): 每页条数（建议最高不超过 100）。
- `q` (str, 可选): 搜索关键词。
- `source` (str, 可选): 过滤来源，如 "金十数据"、"华尔街见闻"。

**返回:**
- `pd.DataFrame`: 包含以下核心字段：
    - `title`: 标题
    - `content`: 详细内容
    - `source`: 数据来源
    - `createdAt`: 发布时间
    - `summary`: AI 生成的摘要
    - `investment_perspective`: AI 提示的投资观点
    - `tags`: 标签列表

### `get_all_news(max_pages=5)`
批量获取多页历史快讯。

**参数:**
- `max_pages` (int): 最大抓取页数。

**返回:**
- `pd.DataFrame`: 合并后的快讯数据。

## 使用示例

```python
from src.collectors import ShishixinwenCollector

collector = ShishixinwenCollector()

# 1. 获取最新 20 条快讯
df = collector.get_news(page_size=20)
print(df[['title', 'source', 'createdAt']].head())

# 2. 搜索关于 "非农" 的 AI 解析
df_search = collector.get_news(q="非农")
if not df_search.empty:
    print(df_search[['title', 'investment_perspective']].head())

# 3. 获取来自 "华尔街见闻" 的快讯
df_ws = collector.get_news(source="华尔街见闻")
```

## 注意事项
1. **数据归属**：该数据源为第三方聚合，请遵循其版权规定。
2. **AI 解析**：`investment_perspective` 和 `detailed_analysis` 为 AI 生成，仅供参考，不构成投资建议。
3. **接口稳定性**：由于使用的是 Next.js 内部接口，结构可能随网站更新而变化。
