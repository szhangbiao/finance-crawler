#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 AKShare 股市情绪指数相关接口

包括:
1. A股新闻情绪指数
2. 50ETF期权波动率指数(恐慌指数)
3. 市场活跃度指数
"""

import akshare as ak
import pandas as pd


def print_divider(title: str):
    """打印分隔线"""
    print("\n" + "=" * 80)
    print(f"测试接口: {title}")
    print("=" * 80)


def test_news_sentiment_index():
    """测试 A股新闻情绪指数"""
    print_divider("index_news_sentiment_scope - A股新闻情绪指数")
    
    try:
        # 获取数据
        df = ak.index_news_sentiment_scope()
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取 {len(df)} 条数据")
            print(f"列名: {df.columns.tolist()}")
            print(f"\n数据时间范围: {df['日期'].min()} 至 {df['日期'].max()}")
            print(f"\n前5条数据:")
            print(df.head())
            print(f"\n数据统计:")
            print(df.describe())
        else:
            print("❌ 未获取到数据")
            
    except Exception as e:
        print(f"❌ 错误: {e}")


def test_50etf_qvix():
    """测试 50ETF期权波动率指数(恐慌指数)"""
    print_divider("index_option_50etf_qvix - 50ETF期权波动率指数(恐慌指数)")
    
    try:
        # 获取数据
        df = ak.index_option_50etf_qvix()
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取 {len(df)} 条数据")
            print(f"列名: {df.columns.tolist()}")
            print(f"\n数据时间范围: {df['date'].min()} 至 {df['date'].max()}")
            print(f"\n前5条数据:")
            print(df.head())
            print(f"\n最近5条数据:")
            print(df.tail())
            print(f"\n当前恐慌指数: {df.iloc[-1]['close']:.2f}")
            
            # 判断市场情绪
            latest_qvix = df.iloc[-1]['close']
            if latest_qvix > 40:
                emotion = "极度恐慌 ⚠️"
            elif latest_qvix < 15:
                emotion = "极度贪婪 ⚠️"
            else:
                emotion = "正常 ✓"
            print(f"市场情绪: {emotion}")
            
            print(f"\n数据统计:")
            print(df[['open', 'high', 'low', 'close']].describe())
        else:
            print("❌ 未获取到数据")
            
    except Exception as e:
        print(f"❌ 错误: {e}")


def test_market_activity():
    """测试市场活跃度指数"""
    print_divider("stock_market_activity_legu - 乐咕市场活跃度")
    
    try:
        # 获取数据
        df = ak.stock_market_activity_legu()
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取 {len(df)} 条数据")
            print(f"列名: {df.columns.tolist()}")
            print(f"\n前5条数据:")
            print(df.head())
            print(f"\n最近5条数据:")
            print(df.tail())
        else:
            print("❌ 未获取到数据")
            
    except Exception as e:
        print(f"❌ 错误: {e}")


def main():
    """主函数"""
    print("=" * 80)
    print("AKShare 股市情绪指数接口测试")
    print("=" * 80)
    
    # 测试各个接口
    test_news_sentiment_index()      # A股新闻情绪指数(可能不可用)
    test_50etf_qvix()                # 50ETF恐慌指数 ✅
    test_market_activity()           # 市场活跃度 ✅
    
    # 总结
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    print("\n✅ 可用接口:")
    print("1. index_option_50etf_qvix - 50ETF期权波动率指数(恐慌指数)")
    print("   - 反映市场波动预期,类似VIX指数")
    print("   - 数值>40表示极度恐慌,<15表示极度贪婪")
    print("")
    print("2. stock_market_activity_legu - 乐咕市场活跃度")
    print("   - 提供当日涨跌家数、涨跌停统计")
    print("   - 可用于判断市场整体情绪和活跃程度")
    print("")
    print("⚠️ 部分可用:")
    print("3. index_news_sentiment_scope - A股新闻情绪指数")
    print("   - 基于财经新闻NLP分析")
    print("   - 当前数据源可能不稳定")



if __name__ == "__main__":
    main()
