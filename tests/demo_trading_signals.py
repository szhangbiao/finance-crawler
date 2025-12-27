import sys
import os
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import IntradayCollector
from src.processors.volatility import VolatilityProcessor
from src.processors.signals import TradingSignalProcessor

def main():
    print("=" * 60)
    print("金融决策信号生成器 (HAR 波动率 + 市场情绪)".center(60))
    print("=" * 60)
    
    # 1. 采集数据
    collector = IntradayCollector()
    symbol = "000300" # 沪深300
    print(f"\n[Step 1] 正在采集 {symbol} 的日内高频数据...")
    df_min = collector.get_index_intraday(symbol=symbol, period="5")
    
    if df_min.empty:
        print("❌ 数据采集失败")
        return
        
    # 2. 计算 RV
    vol_processor = VolatilityProcessor()
    daily_rv = vol_processor.calculate_rv(df_min)
    
    # 3. 生成信号
    print("[Step 2] 正在分析波动率分布并结合情绪指标...")
    signal_processor = TradingSignalProcessor()
    result = signal_processor.generate_signal(daily_rv)
    
    if "error" in result:
        print(f"❌ 信号分析失败: {result['error']}")
        return

    # 4. 打印报告
    status = result['market_status']
    print("\n" + "-" * 60)
    print(f"【当前市场状态】")
    print(f" 预测波动率等级: {status['predicted_volatility_level']}")
    print(f" 估算年化波动率: {status['ann_vol_estimate']}")
    print(f" 市场情绪背景: {status['sentiment_emotion']}")
    print("-" * 60)

    for term, data in result['signals'].items():
        term_name = "短期 (1-3天)" if term == "short_term" else "中期 (1-4周)" if term == "medium_term" else "长期 (1-6月)"
        print(f"\n➤ {term_name} 决策建议:")
        print(f"   【信号】: {data['label']}")
        print(f"   【操作】: {data['advice']}")

    print("\n" + "=" * 60)
    print("风险提示: 量化模型预测仅供参考，不构成直接投资建议。".center(60))
    print("=" * 60)

if __name__ == "__main__":
    main()
