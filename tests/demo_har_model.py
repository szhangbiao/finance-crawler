import sys
import os
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import IntradayCollector
from src.processors.volatility import VolatilityProcessor

def main():
    print("=== HAR Model Volatility Prediction Demo ===")
    
    # 1. 采集历史 5 分钟线
    collector = IntradayCollector()
    symbol = "000300" # 沪深300
    print(f"\n[1] Collecting 5-min data for {symbol}...")
    df_min = collector.get_index_intraday(symbol=symbol, period="5")
    
    if df_min.empty:
        print("❌ Data collection failed.")
        return
        
    # 2. 计算每日 RV
    processor = VolatilityProcessor()
    print("[2] Calculating daily realized volatility (RV)...")
    daily_rv = processor.calculate_rv(df_min)
    print(f"    Available days: {len(daily_rv)}")
    
    # 3. 运行 HAR 预测
    print("[3] Fitting HAR model and predicting next day...")
    result = processor.predict_next_day(daily_rv)
    
    if "error" in result:
        print(f"❌ Prediction failed: {result['error']}")
    else:
        print(f"\n✅ Prediction for next trading day after {result['last_date']}:")
        print(f"    Predicted RV: {result['predicted_rv']:.8f}")
        print(f"    Model R-Squared: {result['r_squared']:.4f}")
        
        print("\nModel Coefficients:")
        for name, val in result['coefficients'].items():
            print(f"    {name}: {val:.6f}")
            
        print("\nWhat this means:")
        print(f"    The model weights 昨日波动率 (RV_d) at {result['coefficients']['RV_d']:.2f}")
        print(f"    The model weights 本周平均 (RV_w) at {result['coefficients']['RV_w']:.2f}")

if __name__ == "__main__":
    main()
