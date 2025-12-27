import pandas as pd
import re
from typing import List, Dict

class NewsProcessor:
    """
    新闻数据处理器.
    负责过滤无用信息、按投资标的分级、去重以及格式化.
    """

    def __init__(self):
        self.name = "news_processor"
        
        # 定义核心投资标的关键词矩阵
        self.portfolio_keywords = {
            "domestic_equity": ["沪深", "A股", "上证", "中证", "创业板", "成交额", "非农", "降准", "降息", "中国央行"],
            "global_equity": ["美股", "标普", "纳斯达克", "美联储", "日经", "日本央行", "越南", "QDII", "跨境投资", "恒生"],
            "gold": ["黄金", "金价", "Au99", "避险", "现货金", "非农", "通胀", "CPI", "PPI"]
        }
        
        # 定义噪音关键词 (广告、个股调研、非相关国际政治等)
        self.noise_keywords = [
            "互动平台", "业绩预告", "调研", "招标", "股东大会", "合同", 
            "也门", "撤军", "导弹", "民用设施", "公司布局", "子公司"
        ]

    def clean_news(self, df_news: pd.DataFrame) -> pd.DataFrame:
        """
        核心清洗流程：去重、过滤、分级.
        """
        if df_news.empty:
            return df_news

        # 1. 基础清理：去重和空值
        df = df_news.drop_duplicates(subset=['title']).copy()
        
        # 2. 移除绝对噪音 (包含噪音词且重要性不高的消息)
        noise_pattern = "|".join(self.noise_keywords)
        df = df[~df['title'].str.contains(noise_pattern, na=False, case=False)]

        # 3. 核心标的相关性打分/过滤
        # 我们只保留与你投资标的（国内指数、黄金、美日越指数）相关的消息
        all_keywords = [item for sublist in self.portfolio_keywords.values() for item in sublist]
        portfolio_pattern = "|".join(all_keywords)
        
        # 只要标题中包含任何一个核心关键词，就保留
        def get_relevance(title):
            count = 0
            for label, kws in self.portfolio_keywords.items():
                if any(kw.lower() in title.lower() for kw in kws):
                    return label
            return "other"

        df['relevance_category'] = df['title'].apply(get_relevance)
        
        # 强力过滤：只保留与你投资类别相关的
        df = df[df['relevance_category'] != "other"]

        return df

    def format_news_for_ai(self, df_cleaned: pd.DataFrame) -> List[Dict]:
        """
        将清洗后的数据转为 AI 易读的精简列表.
        """
        if df_cleaned.empty:
            return []
            
        formatted = []
        # 按类别排序，让 AI 能更有条理地看到相关性
        df_sorted = df_cleaned.sort_values('relevance_category')
        
        for _, row in df_sorted.iterrows():
            category_zh = {
                "domestic_equity": "国内股市/宏观",
                "global_equity": "全球股市/QDII",
                "gold": "黄金/避险"
            }.get(row['relevance_category'], "通用")
            
            # 精简内容：只给 AI 标题和摘要
            formatted.append({
                "category": category_zh,
                "title": row['title'],
                "summary": row.get('summary', '无摘要')[:150] # 限制长度节省 Token
            })
            
        return formatted
