import sys
import os
import pandas as pd

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collectors.shishixinwen import ShishixinwenCollector

def test_shishixinwen_news():
    """测试获取实事新闻快讯"""
    collector = ShishixinwenCollector()
    
    print("Testing get_news()...")
    df = collector.get_news(page=1, page_size=10)
    
    if not df.empty:
        print(f"Successfully fetched {len(df)} news items.")
        print("Columns:", df.columns.tolist())
        print("\nFirst news sample:")
        display_cols = ['title', 'source', 'createdAt']
        available_cols = [c for c in display_cols if c in df.columns]
        if available_cols:
            print(df[available_cols].iloc[0])
        else:
            print(df.iloc[0])
    else:
        print("Fetched empty DataFrame.")
    
    return df

def test_shishixinwen_search():
    """测试搜索功能"""
    collector = ShishixinwenCollector()
    print("\nTesting search for '人民币'...")
    df = collector.get_news(q="人民币", page_size=5)
    
    if not df.empty:
        print(f"Found {len(df)} items related to '人民币'.")
    else:
        print("No results found for '人民币'.")

if __name__ == "__main__":
    df = test_shishixinwen_news()
    test_shishixinwen_search()
