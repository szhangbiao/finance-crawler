import sys
import os
import pandas as pd
from datetime import datetime

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors import CalendarCollector

def test_calendar_collector():
    print("=== Testing CalendarCollector ===")
    collector = CalendarCollector()
    
    # 1. Economic Calendar
    print("\n[1] Fetching Economic Calendar for Dec 29, 2025...")
    df_econ = collector.get_economic_calendar("20251229")
    if not df_econ.empty:
        print(f"✅ Success: {len(df_econ)} events fetched")
        print(df_econ[['时间', '地区', '事件', '重要性']].iloc[:5])
    else:
        print("❌ Failed or empty")
    
    # 2. Upcoming Major Events
    print("\n[2] Fetching Upcoming Major Events (Next 3 Days)...")
    df_upcoming = collector.get_upcoming_major_events(days=3)
    if not df_upcoming.empty:
        print(f"✅ Success: Found {len(df_upcoming)} major events")
        # 显示部分关键词命中的事件
        print(df_upcoming[['日期', '地区', '事件']].iloc[:5])
    else:
        print("❌ No major events found in the next 3 days")
        
    # 3. Futures Delivery Dates
    print("\n[3] Calculating A-share Index Futures Delivery Dates...")
    df_delivery = collector.get_futures_delivery_dates(count=3)
    if not df_delivery.empty:
        print(f"✅ Success: Next 3 months delivery dates")
        print(df_delivery)
    else:
        print("❌ Failed")
        
    # 4. Central Bank Rates
    print("\n[4] Fetching Central Bank Rates...")
    df_rates = collector.get_central_bank_interest_rates()
    if not df_rates.empty:
        print(f"✅ Success: {len(df_rates)} banks fetched")
        print(df_rates)
    else:
        print("❌ Failed or empty")

if __name__ == "__main__":
    test_calendar_collector()
