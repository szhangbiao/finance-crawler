"""
Test script for IndexCollector
"""
import sys
import os
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import IndexCollector

def main():
    print("=== Testing IndexCollector ===")
    collector = IndexCollector()
    
    # 1. Key Indices
    print("\n[1] Fetching Key Indices (沪深重要指数)...")
    df = collector.get_key_indices()
    if not df.empty:
        print(f"✅ Success: {len(df)} items fetched")
        print(df[['代码', '名称', '最新价', '涨跌幅']].head())
    else:
        print("❌ Failed or empty")

    # 2. Daily Data for Shanghai Composite
    print("\n[2] Fetching History for SH000001 (上证指数)...")
    # Note: akshare usually uses symbols like 'sh000001' or just '000001' depending on the API.
    # For stock_zh_index_daily_em, it often takes 'sh000001' style or just code if unique?
    # Let's try 'csi300' implies 'sz399300' etc?
    # Actually for daily_em, it normally takes symbol like "sh000001".
    df_daily = collector.get_index_daily(symbol="sh000001")
    if not df_daily.empty:
        print(f"✅ Success: {len(df_daily)} days of data")
        print(df_daily.tail())
    else:
        print("❌ Failed or empty")

if __name__ == "__main__":
    main()
