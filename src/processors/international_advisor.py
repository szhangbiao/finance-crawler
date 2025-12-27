from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta
from src.collectors import GlobalIndexCollector
from src.processors.news_processor import NewsProcessor

class InternationalAdvisorProcessor:
    """
    国际投资顾问处理器.
    处理美国、日本、越南等国际指数行情及历史趋势.
    """

    def __init__(self, news_processor: NewsProcessor):
        self.global_indices = GlobalIndexCollector()
        self.news_processor = news_processor
        # 标的清单 (对应 AKShare 历史数据的 symbol 名称)
        self.targets = ["标普500", "纳斯达克", "日经225", "越南胡志明"]

    def get_international_report(self) -> Dict:
        """
        生成国际板块综合报告数据.
        """
        report = {
            "spot": [],
            "history_trends": {},
            "news": []
        }

        # 1. 实时行情
        try:
            spot_df = self.global_indices.get_all_indices()
            if not spot_df.empty:
                for name in self.targets:
                    match = spot_df[spot_df['名称'].str.contains(name, na=False)]
                    if not match.empty:
                        report["spot"].append(match[['名称', '最新价', '涨跌幅']].iloc[0].to_dict())
        except Exception as e:
            report["error_spot"] = str(e)

        # 2. 历史趋势 (最近 30 天)
        try:
            for name in self.targets:
                hist_df = self.global_indices.get_historical_data(symbol=name)
                if not hist_df.empty:
                    # 获取最近 30 行
                    report["history_trends"][name] = hist_df.tail(30)[['日期', '最新价']].to_dict(orient='records')
        except Exception as e:
            report["error_hist"] = str(e)

        return report
