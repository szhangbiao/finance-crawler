"""
测试 AKShare 中所有可用的新闻相关接口
"""
import akshare as ak
import pandas as pd

def test_api(name, func, *args, **kwargs):
    """测试单个 API 接口"""
    print(f"\n{'='*80}")
    print(f"测试接口: {name}")
    print(f"{'='*80}")
    try:
        df = func(*args, **kwargs)
        if isinstance(df, pd.DataFrame) and not df.empty:
            print(f"✅ 成功获取 {len(df)} 条数据")
            print(f"列名: {df.columns.tolist()}")
            print(f"\n前3条数据:")
            print(df.head(3))
            return True
        else:
            print(f"⚠️  返回空数据")
            return False
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    print("开始测试 AKShare 新闻相关接口...")
    
    results = {}
    
    # 1. 中国CPI数据 (替代 百度财经日历)
    results['macro_china_cpi_yearly'] = test_api(
        'macro_china_cpi_yearly - 中国CPI数据',
        ak.macro_china_cpi_yearly
    )
    
    # 2. 央视新闻联播
    results['news_cctv'] = test_api(
        'news_cctv - 央视新闻联播',
        ak.news_cctv
    )
    
    # 3. 期货新闻 (上海金属网)
    results['futures_news_shmet'] = test_api(
        'futures_news_shmet - 上海金属网期货新闻',
        ak.futures_news_shmet
    )
    
    # 4. 个股基本信息 (替代 东方财富个股新闻)
    results['stock_individual_info_em'] = test_api(
        'stock_individual_info_em - 东方财富个股信息',
        ak.stock_individual_info_em,
        symbol="000001"
    )
    
    # 5. 研究报告
    results['stock_research_report_em'] = test_api(
        'stock_research_report_em - 东方财富研究报告',
        ak.stock_research_report_em
    )
    
    # 6. 停牌提示
    results['news_trade_notify_suspend_baidu'] = test_api(
        'news_trade_notify_suspend_baidu - 百度停牌提示',
        ak.news_trade_notify_suspend_baidu
    )
    
    # 7. 分红提示
    results['news_trade_notify_dividend_baidu'] = test_api(
        'news_trade_notify_dividend_baidu - 百度分红提示',
        ak.news_trade_notify_dividend_baidu
    )
    
    # 8. 财报时间表
    results['news_report_time_baidu'] = test_api(
        'news_report_time_baidu - 百度财报时间表',
        ak.news_report_time_baidu
    )

    # 9. 国际财经新闻
    results['stock_info_global_cls'] = test_api(
        'stock_info_global_cls - 财联社国际财经新闻',
        ak.stock_info_global_cls
    )
    
    # 总结
    print(f"\n\n{'='*80}")
    print("测试总结")
    print(f"{'='*80}")
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    print(f"\n成功: {success_count}/{total_count}")
    print("\n可用接口:")
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {name}")

if __name__ == "__main__":
    main()
