"""
演示所有可用的财经新闻采集功能
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.collectors import NewsCollector

def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")

def main():
    print("=== 财经新闻采集器 - 完整功能演示 ===")
    
    collector = NewsCollector()
    
    # 1. 百度财经日历
    print_section("📅 1. 百度财经日历（全球经济事件）")
    calendar_df = collector.get_economic_calendar()
    if not calendar_df.empty:
        print(f"✅ 获取 {len(calendar_df)} 条经济事件")
        print(calendar_df[['日期', '时间', '地区', '事件', '重要性']].head(3))
    
    # 2. 央视新闻联播
    print_section("📺 2. 央视新闻联播")
    cctv_df = collector.get_cctv_news()
    if not cctv_df.empty:
        print(f"✅ 获取 {len(cctv_df)} 条新闻")
        print(cctv_df[['date', 'title']].head(3))
    
    # 3. 期货新闻（实时）
    print_section("📊 3. 上海金属网期货新闻（实时）")
    futures_df = collector.get_futures_news()
    if not futures_df.empty:
        print(f"✅ 获取 {len(futures_df)} 条期货新闻")
        print(futures_df.head(5))
    
    # 4. 研究报告
    print_section("📈 4. 东方财富研究报告")
    reports_df = collector.get_research_reports()
    if not reports_df.empty:
        print(f"✅ 获取 {len(reports_df)} 份研究报告")
        if '股票代码' in reports_df.columns and '报告名称' in reports_df.columns:
            print(reports_df[['股票代码', '股票简称', '报告名称', '机构', '日期']].head(3))
    
    # 5. 停牌提示
    print_section("⏸️  5. 股票停牌提示")
    suspension_df = collector.get_suspension_notice()
    if not suspension_df.empty:
        print(f"✅ 获取 {len(suspension_df)} 条停牌信息")
        if '股票代码' in suspension_df.columns:
            print(suspension_df[['股票代码', '股票简称', '停牌时间', '停牌事项说明']].head(3))
    
    # 6. 分红提示
    print_section("💰 6. 股票分红提示")
    dividend_df = collector.get_dividend_notice()
    if not dividend_df.empty:
        print(f"✅ 获取 {len(dividend_df)} 条分红信息")
        print(dividend_df[['股票代码', '股票简称', '除权日', '分红', '送股', '转增']].head(3))
    
    # 7. 财报时间表
    print_section("📋 7. 财报发布时间表")
    earnings_df = collector.get_earnings_calendar()
    if not earnings_df.empty:
        print(f"✅ 获取 {len(earnings_df)} 条财报时间")
        print(earnings_df[['股票代码', '股票简称', '财报类型', '发布时间']].head(3))
    
    print_section("✨ 演示完成")
    print("所有功能已展示完毕！")
    print("\n提示：部分接口可能因为当前时间段没有数据而返回空结果。")

if __name__ == "__main__":
    main()
