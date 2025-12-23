#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全球指数采集器使用示例

演示如何使用 GlobalIndexCollector 获取全球股指数据
"""

from src.collectors import GlobalIndexCollector


def example_1_get_all_indices():
    """示例1: 获取所有全球指数"""
    print("=" * 80)
    print("示例1: 获取所有全球指数")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    df = collector.get_all_indices()
    
    print(f"\n获取到 {len(df)} 个全球指数")
    print(f"\n前10个指数:")
    print(df.head(10)[['名称', '最新价', '涨跌幅']])


def example_2_get_us_indices():
    """示例2: 获取美国指数"""
    print("\n" + "=" * 80)
    print("示例2: 获取美国主要指数")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    us_data = collector.get_us_indices()
    
    print(f"\n美国指数数量: {len(us_data)}")
    print(us_data[['名称', '最新价', '涨跌额', '涨跌幅']])


def example_3_get_asian_indices():
    """示例3: 获取亚洲指数"""
    print("\n" + "=" * 80)
    print("示例3: 获取亚洲主要指数")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    asia_data = collector.get_asian_indices()
    
    print(f"\n亚洲指数数量: {len(asia_data)}")
    print(asia_data[['名称', '最新价', '涨跌额', '涨跌幅']])


def example_4_get_specific_index():
    """示例4: 获取特定指数"""
    print("\n" + "=" * 80)
    print("示例4: 获取特定指数")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    
    # 获取标普500
    sp500 = collector.get_index_by_name('标普500')
    if sp500 is not None:
        print(f"\n标普500:")
        print(f"  最新价: {sp500['最新价']}")
        print(f"  涨跌幅: {sp500['涨跌幅']}%")
        print(f"  开盘价: {sp500['开盘价']}")
        print(f"  昨收价: {sp500['昨收价']}")
    
    # 获取恒生指数
    hsi = collector.get_index_by_name('恒生')
    if hsi is not None:
        print(f"\n恒生指数:")
        print(f"  最新价: {hsi['最新价']}")
        print(f"  涨跌幅: {hsi['涨跌幅']}%")
    
    # 获取日经225
    nikkei = collector.get_index_by_name('日经225')
    if nikkei is not None:
        print(f"\n日经225:")
        print(f"  最新价: {nikkei['最新价']}")
        print(f"  涨跌幅: {nikkei['涨跌幅']}%")


def example_5_market_sentiment():
    """示例5: 全球市场情绪分析"""
    print("\n" + "=" * 80)
    print("示例5: 全球市场情绪分析")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    sentiment = collector.get_market_sentiment()
    
    if sentiment.get('success'):
        print(f"\n市场情绪: {sentiment['sentiment']}")
        print(f"总指数数: {sentiment['total']}")
        print(f"上涨: {sentiment['rising']} ({sentiment['rising_pct']}%)")
        print(f"下跌: {sentiment['falling']} ({sentiment['falling_pct']}%)")
        print(f"平均涨跌幅: {sentiment['avg_change']}%")


def example_6_top_performers():
    """示例6: 涨跌幅排行榜"""
    print("\n" + "=" * 80)
    print("示例6: 全球涨跌幅排行榜")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    
    # 涨幅榜
    print("\n涨幅榜 TOP10:")
    top10 = collector.get_top_performers(10)
    print(top10[['名称', '涨跌幅', '最新价']])
    
    # 跌幅榜
    print("\n跌幅榜 TOP10:")
    bottom10 = collector.get_bottom_performers(10)
    print(bottom10[['名称', '涨跌幅', '最新价']])


def example_7_full_summary():
    """示例7: 完整市场概况"""
    print("\n" + "=" * 80)
    print("示例7: 完整市场概况")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    collector.print_market_summary()


def example_8_custom_analysis():
    """示例8: 自定义分析"""
    print("\n" + "=" * 80)
    print("示例8: 自定义分析 - 大中华区指数对比")
    print("=" * 80)
    
    collector = GlobalIndexCollector()
    df = collector.get_all_indices()
    
    # 筛选大中华区指数
    china_keywords = '上证|深证|恒生|香港|台湾'
    china_indices = df[df['名称'].str.contains(china_keywords, na=False)]
    
    print(f"\n大中华区 {len(china_indices)} 个指数:")
    print(china_indices[['名称', '最新价', '涨跌额', '涨跌幅']])


def main():
    """运行所有示例"""
    print("🌍 全球指数采集器使用示例\n")
    
    # 运行所有示例
    example_1_get_all_indices()
    example_2_get_us_indices()
    example_3_get_asian_indices()
    example_4_get_specific_index()
    example_5_market_sentiment()
    example_6_top_performers()
    example_7_full_summary()
    example_8_custom_analysis()
    
    print("\n" + "=" * 80)
    print("所有示例运行完成!")
    print("=" * 80)


if __name__ == "__main__":
    # 可以选择运行单个示例或所有示例
    
    # 运行单个示例:
    # example_4_get_specific_index()
    
    # 运行所有示例:
    main()
