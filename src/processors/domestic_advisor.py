from typing import Dict, List
import pandas as pd
from datetime import datetime, timedelta
from src.collectors import (
    IndexCollector, 
    MetalsCollector, 
    IntradayCollector,
    SentimentIndexCollector
)
from src.processors.volatility import VolatilityProcessor
from src.processors.news_processor import NewsProcessor

class DomesticAdvisorProcessor:
    """
    国内投资顾问处理器.
    处理沪深指数、黄金、HAR 波动率预测及相关新闻.
    """

    def __init__(self, news_processor: NewsProcessor):
        self.indices = IndexCollector()
        self.metals = MetalsCollector()
        self.intraday = IntradayCollector()
        self.vol_processor = VolatilityProcessor()
        self.sentiment = SentimentIndexCollector()
        self.news_processor = news_processor

    def get_domestic_report(self) -> Dict:
        """
        生成国内板块综合报告数据.
        """
        report = {
            "spot": {},
            "history_30d": {},
            "volatility_forecast": {},
            "sentiment": {},
            "news": []
        }

        # 1. 实时行情与30天历史
        try:
            # 沪深300 (sh000300)
            target_symbol = "sh000300"
            spot_df = self.indices.get_key_indices()
            if not spot_df.empty:
                sh300_spot = spot_df[spot_df['名称'] == "沪深300"]
                if not sh300_spot.empty:
                    report["spot"]["sh300"] = sh300_spot[['最新价', '涨跌幅']].iloc[0].to_dict()

            # 30天历史
            hist_df = self.indices.get_index_daily(symbol=target_symbol)
            if not hist_df.empty:
                # 获取最近30个交易日
                report["history_30d"]["sh300"] = hist_df.tail(30)[['date', 'close']].to_dict(orient='records')
            
            # 黄金
            gold_price = self.metals.get_spot_price("Au99.99")
            report["spot"]["gold"] = gold_price
        except Exception as e:
            report["error_spot"] = str(e)

        # 2. HAR 波动率预测 (基于沪深300 5分钟线)
        try:
            df_min = self.intraday.get_index_intraday(symbol="000300", period="5")
            if not df_min.empty:
                daily_rv = self.vol_processor.calculate_rv(df_min)
                vol_pred = self.vol_processor.predict_next_day(daily_rv)
                report["volatility_forecast"] = vol_pred
        except Exception as e:
            report["error_vol"] = str(e)

        # 3. 市场情绪
        try:
            sent = self.sentiment.get_comprehensive_sentiment()
            if sent.get('success'):
                report["sentiment"] = sent
        except Exception as e:
            report["error_sent"] = str(e)

        return report
