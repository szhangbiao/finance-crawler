from typing import Dict, Optional
import pandas as pd
from datetime import datetime
from src.processors.volatility import VolatilityProcessor
from src.collectors.sentiment import SentimentIndexCollector

class TradingSignalProcessor:
    """
    交易信号生成处理器.
    结合 HAR 波动率预测与市场情绪指标，生成多维度交易决策建议.
    """

    def __init__(self):
        self.vol_processor = VolatilityProcessor()
        self.sentiment_collector = SentimentIndexCollector()

    def generate_signal(self, daily_rv: pd.DataFrame) -> Dict:
        """
        结合波动率和情绪生成综合信号.
        
        Args:
            daily_rv: 每日已实现波动率数据.
            
        Returns:
            Dict: 包含短、中、长期信号和建议的字典.
        """
        # 1. 获取波动率预测
        vol_result = self.vol_processor.predict_next_day(daily_rv)
        if "error" in vol_result:
            return {"success": False, "error": f"Volatility calculation failed: {vol_result['error']}"}

        # 2. 获取市场情绪
        sentiment_result = self.sentiment_collector.get_comprehensive_sentiment()
        if not sentiment_result.get('success'):
            # 如果综合数据失败，尝试只取恐慌指数
            sentiment_result = self.sentiment_collector.get_latest_fear_greed()
            if not sentiment_result.get('success'):
                return {"success": False, "error": "Sentiment data collection failed."}

        # 3. 提取关键指标
        pred_rv = vol_result['predicted_rv']
        # 简单将 RV 转换为波动率百分比 (按 242 交易日年化)
        ann_vol = (pred_rv * 242) ** 0.5 * 100
        
        sentiment_score = sentiment_result.get('comprehensive_score', 50)
        emotion = sentiment_result.get('comprehensive_emotion', sentiment_result.get('emotion', '未知'))
        
        # 4. 生成多维度建议
        signals = {
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "market_status": {
                "predicted_volatility_level": "高" if ann_vol > 25 else "中" if ann_vol > 15 else "低",
                "sentiment_emotion": emotion,
                "ann_vol_estimate": f"{ann_vol:.2f}%"
            },
            "signals": {}
        }

        # --- 短期视角 (1-3天): 风险控制与仓位 ---
        if ann_vol > 20:
            if sentiment_score < 30:
                short_signal = "反弹博弈 (Buy on Dip)"
                short_adv = "市场极度悲观且波动剧烈，适合轻仓分批布局超跌反弹，务必设好止损。"
            elif sentiment_score > 70:
                short_signal = "风险规避 (Sell/Close)"
                short_adv = "市场极度贪婪且波动加大，暗示见顶风险，建议收紧止损或逢高减仓。"
            else:
                short_signal = "观望 (Wait)"
                short_adv = "波动率较高但情绪不明，短期易出现来回洗盘，建议等待方向明确。"
        else:
            short_signal = "持有/加仓 (Hold/Add)"
            short_adv = "当前波动率较低，市场情绪平稳，可维持现有头寸或寻找补涨机会。"

        signals["signals"]["short_term"] = {
            "label": short_signal,
            "advice": short_adv
        }

        # --- 中期视角 (1-4周): 趋势与网格 ---
        # 参考 HAR 的周系数
        coeffs = vol_result.get('coefficients', {})
        rv_w_weight = coeffs.get('RV_w', 0)
        
        if rv_w_weight > 0:
            mid_signal = "趋势跟踪 (Trend Following)"
            mid_adv = "中期波动率贡献为正，说明趋势具有持续性，可跟随当前市场主趋势操作。"
        else:
            mid_signal = "均值回归 (Mean Reversion)"
            mid_adv = "中期波动率呈现负向反馈，市场可能陷入宽幅震荡，适合使用网格交易策略。"

        signals["signals"]["medium_term"] = {
            "label": mid_signal,
            "advice": mid_adv
        }

        # --- 长期视角 (1-6月): 配置权重 ---
        if ann_vol > 30:
            long_signal = "防守配置 (Defensive)"
            long_adv = "长期波动率预测进入极高区间，系统性风险加大，建议配置黄金、低波红利或债基。"
        elif ann_vol < 12:
            long_signal = "进攻配置 (Aggressive)"
            long_adv = "市场处于典型的“低波宁静期”，是布局优质权益资产的黄金时间。"
        else:
            long_signal = "均衡配置 (Balanced)"
            long_adv = "波动率处于正常范围，建议保持股债平衡比例。"

        signals["signals"]["long_term"] = {
            "label": long_signal,
            "advice": long_adv
        }

        return signals
