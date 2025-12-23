import sys
import os

# Ensure the 'src' directory is in the path so we can import modules correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from collectors import NewsCollector

def main():
    print("=== Finance Crawler Started ===")
    
    collector = NewsCollector()
    
    print("\n[1] Fetching Economic Calendar (百度财经日历)...")
    calendar_df = collector.get_economic_calendar()
    
    if not calendar_df.empty:
        print(f"Successfully fetched {len(calendar_df)} items.")
        print(f"Columns: {calendar_df.columns.tolist()}")
        # 显示前5条经济事件
        if '日期' in calendar_df.columns and '事件' in calendar_df.columns:
            print(calendar_df[['日期', '时间', '地区', '事件', '重要性']].head())
        else:
            print(calendar_df.head())
    else:
        print("No economic calendar data found or error occurred.")

    print("\n[2] Fetching CCTV News (央视新闻联播)...")
    cctv_df = collector.get_cctv_news()
    
    if not cctv_df.empty:
        print(f"Successfully fetched {len(cctv_df)} items.")
        print(f"Columns: {cctv_df.columns.tolist()}")
        # 显示前3条新闻标题
        if 'title' in cctv_df.columns:
            print(cctv_df[['date', 'title']].head(3))
        else:
            print(cctv_df.head(3))
    else:
        print("No CCTV news found or error occurred.")

    print("\n=== Task Completed ===")

if __name__ == "__main__":
    main()
