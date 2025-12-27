from typing import Dict, List
import pandas as pd
from src.collectors.shishixinwen import ShishixinwenCollector
from src.processors.news_processor import NewsProcessor
from src.processors.domestic_advisor import DomesticAdvisorProcessor
from src.processors.international_advisor import InternationalAdvisorProcessor

class StrategyAdvisorProcessor:
    """
    策略分析中枢处理器.
    协调国内和国际板块的顾问处理器，生成最终的 AI 决策建议.
    """

    def __init__(self):
        self.name = "strategy_advisor_processor"
        self.news_collector = ShishixinwenCollector()
        self.news_processor = NewsProcessor()
        
        # 初始化子处理器
        self.domestic_advisor = DomesticAdvisorProcessor(self.news_processor)
        self.international_advisor = InternationalAdvisorProcessor(self.news_processor)

    def get_full_report_data(self) -> Dict:
        """
        聚合所有板块的数据.
        """
        # 1. 获取各个板块的数据
        domestic_data = self.domestic_advisor.get_domestic_report()
        international_data = self.international_advisor.get_international_report()
        
        # 2. 获取并清洗新闻
        news_data = []
        try:
            raw_news = self.news_collector.get_news(page_size=50)
            if not raw_news.empty:
                cleaned_news = self.news_processor.clean_news(raw_news)
                news_data = self.news_processor.format_news_for_ai(cleaned_news)
        except Exception as e:
            print(f"News collection error: {e}")

        return {
            "domestic": domestic_data,
            "international": international_data,
            "news": news_data
        }

    def generate_ai_prompt(self) -> str:
        """
        生成结构精细的 AI 投资策略 Prompt.
        """
        data = self.get_full_report_data()
        
        prompt = "# 全球资产配置 AI 决策报告\n\n"
        prompt += "你现在是一位顶级的量化宏观对冲基金经理。请基于以下采集的国内（中短期）与国际（中长期）多维数据，为投资者提供最终的资金调度及仓位建议。\n\n"

        # --- 国内部分 ---
        prompt += "## 一、国内板块分析 (策略：中短期 | 标的：沪深300、黄金)\n"
        dom = data['domestic']
        
        # 实时与历史
        if "sh300" in dom.get("spot", {}):
            sh = dom["spot"]["sh300"]
            prompt += f"### 1. 沪深300 行情\n- 最新价: {sh['最新价']} (涨跌幅: {sh['涨跌幅']}%)\n"
            if "sh300" in dom.get("history_30d", {}):
                hist = dom["history_30d"]["sh300"]
                prompt += f"- 30日价格趋势: { [float(h['close']) for h in hist[-5:]] } (最近5日收盘)\n"
        
        if "gold" in dom.get("spot", {}):
            prompt += f"- 现货黄金 (SGE): {dom['spot']['gold']}\n"

        # HAR 波动率
        vol = dom.get("volatility_forecast", {})
        if vol and "predicted_rv" in vol:
            prompt += f"\n### 2. 波动率预警 (HAR 模型)\n"
            prompt += f"- 预测明日波动率 (RV): {vol['predicted_rv']:.8f}\n"
            prompt += f"- 模型 R-平方: {vol['r_squared']:.4f}\n"
            prompt += f"- 模型建议: {'波动率处于低位，适合持筹' if vol['predicted_rv'] < 0.00005 else '波动率激增，需警惕下行回撤'}\n"

        # 情绪
        sent = dom.get("sentiment", {})
        if sent and "comprehensive_score" in sent:
            prompt += f"\n### 3. 市场情绪指标\n- 综合评分: {sent['comprehensive_score']}/100 ({sent['comprehensive_emotion']})\n"
            prompt += f"- 建议: {sent['suggestion']}\n"

        # --- 国际部分 ---
        prompt += "\n## 二、国际板块分析 (策略：中长期 | 标的：美国、日本、越南 QDII)\n"
        intl = data['international']
        
        if intl.get("spot"):
            prompt += "### 1. 实时指数详情\n"
            for item in intl["spot"]:
                prompt += f"- {item['名称']}: {item['最新价']} ({item['涨跌幅']}%)\n"
        
        if intl.get("history_trends"):
            prompt += "\n### 2. 核心市场30日趋势对比 (收盘价序列)\n"
            for name, trend in intl["history_trends"].items():
                last_5 = [float(t['最新价']) for t in trend[-5:]]
                prompt += f"- {name}: {last_5}\n"

        # --- 新闻资讯 ---
        prompt += "\n## 三、精选核心快讯 (按标的相关性排序)\n"
        if data['news']:
            for item in data['news']:
                prompt += f"- **[{item['category']}]** {item['title']}\n"
        else:
            prompt += "- 暂无相关性命中的核心新闻。\n"

        prompt += "\n---\n"
        prompt += "## AI 决策要求：\n"
        prompt += "1. **跨市场调度**：根据 HAR 模型预测的国内波动率风险，判断是否需要将资金抽离国内转入相对稳定的国际板块（或反之）。\n"
        prompt += "2. **仓位细节**：具体到美国、日本、越南、国内 300、黄金的加减仓百分比。\n"
        prompt += "3. **宏观解读**：结合资讯中的跨境投资政策，给出 QDII 的中长期持有建议。\n"
        
        return prompt
