import sys
import os
import pandas as pd
import numpy as np

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import IntradayCollector

def test_har_data_preparation():
    print("=== HAR Model Data Preparation Test ===")
    collector = IntradayCollector()
    
    # 1. 获取沪深 300 的 5 分钟数据
    symbol = "000300"
    print(f"\n[1] Fetching 5-min data for Index: {symbol}...")
    df = collector.get_index_intraday(symbol=symbol, period="5")
    
    if df.empty:
        print("❌ Failed to fetch data")
        return

    print(f"✅ Success: Fetched {len(df)} rows of 5-min data")
    
    # 2. 演示如何计算每日已实现波动率 (RV)
    # 计算对数收益率
    df['log_return'] = np.log(df['收盘'] / df['收盘'].shift(1))
    
    # 按天分组并计算平方收益率之和 (RV)
    # 注意：AKShare 分钟线的时间戳通常包含日期
    df['date'] = df['时间'].dt.date
    daily_rv = df.groupby('date')['log_return'].apply(lambda x: np.sum(x**2)).reset_index()
    daily_rv.columns = ['date', 'RV']
    
    print("\n[2] Calculated Daily Realized Volatility (RV):")
    print(daily_rv.tail(5))
    
    # 3. 演示 HAR 滞后分量 (Day, Week, Month)
    if len(daily_rv) >= 22:
        daily_rv['RV_day'] = daily_rv['RV'].shift(1)
        daily_rv['RV_week'] = daily_rv['RV'].shift(1).rolling(5).mean()
        daily_rv['RV_month'] = daily_rv['RV'].shift(1).rolling(22).mean()
        
        print("\n[3] HAR Model Features (Lags):")
        print(daily_rv[['date', 'RV', 'RV_day', 'RV_week', 'RV_month']].tail(5))
    else:
        print("\n[3] Note: Not enough days to compute Monthly lag (need 22+ days)")

if __name__ == "__main__":
    test_har_data_preparation()
