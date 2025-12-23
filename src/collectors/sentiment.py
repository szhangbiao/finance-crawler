#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
股市情绪指数数据采集器

提供以下情绪指数数据:
1. 50ETF期权波动率指数(恐慌指数)
2. 市场活跃度指数
"""

import akshare as ak
import pandas as pd
from datetime import datetime
from typing import Dict, Optional


class SentimentIndexCollector:
    """股市情绪指数数据采集器"""
    
    def __init__(self):
        """初始化采集器"""
        self.name = "sentiment_index_collector"
    
    def get_fear_greed_index(self) -> Optional[pd.DataFrame]:
        """
        获取恐慌贪婪指数 (50ETF期权波动率指数)
        
        Returns:
            DataFrame: 包含日期和QVIX指数数据
            None: 如果获取失败
        """
        try:
            df = ak.index_option_50etf_qvix()
            if df is not None and len(df) > 0:
                # 保持原始列名
                return df
            return None
        except Exception as e:
            print(f"获取恐慌指数失败: {e}")
            return None
    
    def get_latest_fear_greed(self) -> Dict:
        """
        获取最新的恐慌贪婪指数及其解读
        
        Returns:
            dict: 包含指数值、情绪描述、建议等信息
        """
        df = self.get_fear_greed_index()
        if df is None or len(df) == 0:
            return {
                "success": False,
                "error": "无法获取数据"
            }
        
        latest = df.iloc[-1]
        qvix = latest['close']
        
        # 情绪判断
        if qvix > 40:
            emotion = "极度恐慌"
            level = "danger"
            description = "市场出现非理性恐慌,短期内可能出现反弹机会"
            suggestion = "关注超跌股票,但需注意风险控制"
        elif qvix > 30:
            emotion = "恐慌"
            level = "warning"
            description = "市场情绪偏悲观,波动较大"
            suggestion = "保持谨慎,适当降低仓位"
        elif qvix > 20:
            emotion = "正常偏恐慌"
            level = "normal"
            description = "市场情绪正常,略有担忧"
            suggestion = "正常交易,注意风险管理"
        elif qvix > 15:
            emotion = "正常"
            level = "normal"
            description = "市场情绪健康,波动在合理范围"
            suggestion = "正常交易策略"
        else:
            emotion = "极度贪婪"
            level = "danger"
            description = "市场出现非理性繁荣,可能伴随回调风险"
            suggestion = "注意获利了结,警惕高位风险"
        
        return {
            "success": True,
            "date": latest['date'],
            "qvix": round(qvix, 2),
            "open": round(latest['open'], 2),
            "high": round(latest['high'], 2),
            "low": round(latest['low'], 2),
            "emotion": emotion,
            "level": level,
            "description": description,
            "suggestion": suggestion,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_market_activity(self) -> Optional[pd.DataFrame]:
        """
        获取市场活跃度数据
        
        Returns:
            DataFrame: 包含市场活跃度各项指标
            None: 如果获取失败
        """
        try:
            df = ak.stock_market_activity_legu()
            if df is not None and len(df) > 0:
                return df
            return None
        except Exception as e:
            print(f"获取市场活跃度失败: {e}")
            return None
    
    def get_market_activity_analysis(self) -> Dict:
        """
        获取市场活跃度分析
        
        Returns:
            dict: 包含活跃度、涨跌统计、情绪分析等
        """
        df = self.get_market_activity()
        if df is None or len(df) == 0:
            return {
                "success": False,
                "error": "无法获取数据"
            }
        
        # 转换为字典便于查询
        data_dict = dict(zip(df['item'], df['value']))
        
        # 提取关键指标
        rise_count = int(data_dict.get('上涨', 0))
        fall_count = int(data_dict.get('下跌', 0))
        limit_up = int(data_dict.get('涨停', 0))
        limit_down = int(data_dict.get('跌停', 0))
        flat_count = int(data_dict.get('平盘', 0))
        activity_str = str(data_dict.get('活跃度', '0%'))
        stat_date = data_dict.get('统计日期', '')
        
        # 计算总数
        total = rise_count + fall_count + flat_count
        
        # 计算涨跌比例
        if total > 0:
            rise_ratio = round(rise_count / total * 100, 2)
            fall_ratio = round(fall_count / total * 100, 2)
        else:
            rise_ratio = 0
            fall_ratio = 0
        
        # 情绪判断
        if rise_ratio > 70:
            emotion = "强烈看涨"
            level = "very_bullish"
        elif rise_ratio > 60:
            emotion = "看涨"
            level = "bullish"
        elif rise_ratio > 40:
            emotion = "中性"
            level = "neutral"
        elif rise_ratio > 30:
            emotion = "看跌"
            level = "bearish"
        else:
            emotion = "强烈看跌"
            level = "very_bearish"
        
        # 活跃度判断
        activity_value = float(activity_str.rstrip('%'))
        if activity_value > 50:
            activity_level = "高"
        elif activity_value > 30:
            activity_level = "中"
        else:
            activity_level = "低"
        
        return {
            "success": True,
            "stat_date": stat_date,
            "total_stocks": total,
            "rise_count": rise_count,
            "fall_count": fall_count,
            "flat_count": flat_count,
            "rise_ratio": rise_ratio,
            "fall_ratio": fall_ratio,
            "limit_up": limit_up,
            "limit_down": limit_down,
            "activity_rate": activity_str,
            "activity_level": activity_level,
            "emotion": emotion,
            "emotion_level": level,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_comprehensive_sentiment(self) -> Dict:
        """
        获取综合市场情绪分析
        
        结合恐慌指数和市场活跃度给出综合判断
        
        Returns:
            dict: 综合情绪分析结果
        """
        fear_greed = self.get_latest_fear_greed()
        activity = self.get_market_activity_analysis()
        
        if not fear_greed.get('success') or not activity.get('success'):
            return {
                "success": False,
                "error": "无法获取完整数据"
            }
        
        # 综合评分 (0-100, 0=极度恐慌, 100=极度贪婪)
        # QVIX指数: 值越低越贪婪,做反向映射
        qvix_score = max(0, min(100, (40 - fear_greed['qvix']) * 2.5))
        
        # 活跃度评分: 涨跌比例直接作为分数
        activity_score = activity['rise_ratio']
        
        # 综合得分 (恐慌指数权重60%, 涨跌比权重40%)
        comprehensive_score = round(qvix_score * 0.6 + activity_score * 0.4, 2)
        
        # 综合情绪判断
        if comprehensive_score >= 70:
            comprehensive_emotion = "极度乐观"
            suggestion = "市场情绪过热,建议保持谨慎,注意获利了结"
        elif comprehensive_score >= 60:
            comprehensive_emotion = "乐观"
            suggestion = "市场情绪偏好,可适当参与,但需控制仓位"
        elif comprehensive_score >= 40:
            comprehensive_emotion = "中性"
            suggestion = "市场情绪平稳,按既定策略操作"
        elif comprehensive_score >= 30:
            comprehensive_emotion = "悲观"
            suggestion = "市场情绪偏弱,建议减少仓位,观望为主"
        else:
            comprehensive_emotion = "极度悲观"
            suggestion = "市场情绪低迷,严格控制风险,关注超跌机会"
        
        return {
            "success": True,
            "comprehensive_score": comprehensive_score,
            "comprehensive_emotion": comprehensive_emotion,
            "suggestion": suggestion,
            "fear_greed_data": fear_greed,
            "market_activity_data": activity,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def print_sentiment_report(self):
        """打印市场情绪报告"""
        print("=" * 80)
        print("股市情绪指数报告".center(80))
        print("=" * 80)
        
        result = self.get_comprehensive_sentiment()
        
        if not result.get('success'):
            print(f"❌ 错误: {result.get('error')}")
            return
        
        print(f"\n生成时间: {result['update_time']}")
        print(f"\n【综合评分】: {result['comprehensive_score']} 分")
        print(f"【综合情绪】: {result['comprehensive_emotion']}")
        print(f"【操作建议】: {result['suggestion']}")
        
        fear_greed = result['fear_greed_data']
        print(f"\n" + "-" * 80)
        print("恐慌贪婪指数 (50ETF QVIX)")
        print("-" * 80)
        print(f"日期: {fear_greed['date']}")
        print(f"指数值: {fear_greed['qvix']} (开:{fear_greed['open']}, 高:{fear_greed['high']}, 低:{fear_greed['low']})")
        print(f"情绪: {fear_greed['emotion']} ({fear_greed['level']})")
        print(f"说明: {fear_greed['description']}")
        print(f"建议: {fear_greed['suggestion']}")
        
        activity = result['market_activity_data']
        print(f"\n" + "-" * 80)
        print("市场活跃度")
        print("-" * 80)
        print(f"统计时间: {activity['stat_date']}")
        print(f"总股票数: {activity['total_stocks']}")
        print(f"上涨: {activity['rise_count']} ({activity['rise_ratio']}%)")
        print(f"下跌: {activity['fall_count']} ({activity['fall_ratio']}%)")
        print(f"涨停: {activity['limit_up']} | 跌停: {activity['limit_down']}")
        print(f"活跃度: {activity['activity_rate']} ({activity['activity_level']})")
        print(f"市场情绪: {activity['emotion']} ({activity['emotion_level']})")
        
        print("\n" + "=" * 80)


if __name__ == "__main__":
    # 测试
    collector = SentimentIndexCollector()
    collector.print_sentiment_report()
