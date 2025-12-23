"""
Test script for MetalsCollector
"""
import sys
import os
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import MetalsCollector

def main():
    print("=== Testing MetalsCollector ===")
    collector = MetalsCollector()
    
    # 1. Real-time Quotations
    print("\n[1] Fetching Real-time SGE Quotations (上海黄金交易所)...")
    df = collector.get_spot_quotations()
    if not df.empty:
        print(f"✅ Success: {len(df)} items fetched")
        print(df[['品种', '现价', '更新时间']].head())
    else:
        print("❌ Failed or empty")

    # 2. Spot Price for Au99.99
    print("\n[2] Fetching Spot Price for 'Au99.99'...")
    price = collector.get_spot_price("Au99.99")
    if price is not None:
        print(f"✅ Success: Au99.99 Price = {price}")
    else:
        print("❌ Failed to get price")

    # 3. Historical Data for Au99.99
    print("\n[3] Fetching History for 'Au99.99'...")
    df_hist = collector.get_daily_hist("Au99.99")
    if not df_hist.empty:
        print(f"✅ Success: {len(df_hist)} days of data")
        print(df_hist[['date', 'open', 'close', 'high', 'low']].tail())
    else:
        print("❌ Failed or empty")

if __name__ == "__main__":
    main()
