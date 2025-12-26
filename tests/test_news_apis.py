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

    # 10. 国际机构中国消息
    collector = ak.stock_info_global_cls
    # 由于我们需要测试的是 NewsCollector 的方法，这里需要实例化 collector 对象或者模拟
    # 为了保持原有 test_api 的风格，我们稍微变通一下，这里实际上我们应该引入 NewsCollector 来测试
    # 但现有文件结构是从 ak 直接调用的。让我们先简单测试 ak 接口，
    # 而 get_major_institution_news 是我们自定义在 NewsCollector 里的。
    # 所以我们需要实例化 NewsCollector。
    
    print(f"\n{'='*80}")
    print("测试自定义方法: get_major_institution_news")
    print(f"{'='*80}")
    try:
        from src.collectors.news import NewsCollector
        nc = NewsCollector()
        df = nc.get_major_institution_news()
        if isinstance(df, pd.DataFrame):
            print(f"✅ 方法调用成功，返回结果条数: {len(df)}")
            if not df.empty:
                print(f"列名: {df.columns.tolist()}")
                print(f"前3条数据:\n{df.head(3)}")
            else:
                print("⚠️  无匹配数据 (当前可能无相关新闻)")
            results['get_major_institution_news'] = True
        else:
            print("❌ 返回类型错误")
            results['get_major_institution_news'] = False
    except ImportError:
        # 为了兼容如果在某些环境下跑路径问题，尝试动态添加路径
        import sys, os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from src.collectors.news import NewsCollector
        nc = NewsCollector()
        df = nc.get_major_institution_news()
        print(f"✅ 方法调用成功 (fix import)，返回结果条数: {len(df)}")
        results['get_major_institution_news'] = True
    except Exception as e:
        print(f"❌ 错误: {e}")
        results['get_major_institution_news'] = False
    
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
