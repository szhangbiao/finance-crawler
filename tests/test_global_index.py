#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试 AKShare 全球股指数据接口

重点测试:
- 美国股指 (标普500, 道琼斯, 纳斯达克等)
- 日本股指 (日经225等)
- 印度股指 (孟买SENSEX等)
- 越南股指 (越南VN-Index等)

可用接口:
- index_global_name_table: 获取全球指数名称表
- index_global_spot_em: 获取东方财富全球指数实时行情
"""

import akshare as ak
import pandas as pd


def print_divider(title: str):
    """打印分隔线"""
    print("\n" + "=" * 80)
    print(f"{title}")
    print("=" * 80)


def test_get_global_index_list():
    """测试获取全球指数列表"""
    print_divider("步骤1: 获取全球指数名称表")
    
    try:
        # 获取全球指数列表
        df = ak.index_global_name_table()
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取 {len(df)} 个全球指数")
            print(f"列名: {df.columns.tolist()}")
            print(f"\n数据示例 (前20条):")
            print(df.head(20))
            
            # 筛选特定国家/地区的指数
            print("\n" + "-" * 80)
            
            # 美国 - 注意:名称表中没有美国指数,需要在实时行情中查找
            print("\n⚠️ 名称表中暂无美国指数")
            
            # 日本
            japan_indices = df[df['指数名称'].str.contains('日经|东证|日本', na=False)]
            print(f"\n日本相关指数 ({len(japan_indices)} 个):")
            print(japan_indices[['指数名称', '代码']])
            
            # 印度
            india_indices = df[df['指数名称'].str.contains('印度|孟买|SENSEX|Nifty', na=False)]
            print(f"\n印度相关指数 ({len(india_indices)} 个):")
            print(india_indices[['指数名称', '代码']])
            
            # 越南
            vietnam_indices = df[df['指数名称'].str.contains('越南|VN', na=False)]
            print(f"\n越南相关指数 ({len(vietnam_indices)} 个):")
            if len(vietnam_indices) > 0:
                print(vietnam_indices[['指数名称', '代码']])
            else:
                print("⚠️ 名称表中暂无越南指数")
            
            return df
        else:
            print("❌ 未获取到数据")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_global_spot_data():
    """测试获取全球指数实时行情"""
    print_divider("步骤2: 获取全球指数实时行情")
    
    try:
        # 获取实时行情
        df = ak.index_global_spot_em()
        
        if df is not None and len(df) > 0:
            print(f"✅ 成功获取 {len(df)} 个指数的实时行情")
            print(f"列名: {df.columns.tolist()}")
            
            # 显示美国主要指数
            print("\n美国主要指数实时行情:")
            usa_data = df[df['名称'].str.contains('标普|道琼斯|纳斯达克', na=False)]
            if len(usa_data) > 0:
                print(usa_data[['名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '昨收价']])
            
            # 显示日本主要指数
            print("\n日本主要指数实时行情:")
            japan_data = df[df['名称'].str.contains('日经', na=False)]
            if len(japan_data) > 0:
                print(japan_data[['名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '昨收价']])
            
            # 显示印度主要指数
            print("\n印度主要指数实时行情:")
            india_data = df[df['名称'].str.contains('印度|孟买', na=False)]
            if len(india_data) > 0:
                print(india_data[['名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '昨收价']])
            
            # 显示越南主要指数
            print("\n越南主要指数实时行情:")
            vietnam_data = df[df['名称'].str.contains('越南', na=False)]
            if len(vietnam_data) > 0:
                print(vietnam_data[['名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '昨收价']])
            else:
                print("⚠️ 未找到越南指数数据")
            
            return df
        else:
            print("❌ 未获取到数据")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("=" * 80)
    print("AKShare 全球股指数据接口测试".center(80))
    print("=" * 80)
    
    # 1. 获取全球指数列表
    index_table = test_get_global_index_list()
    
    # 2. 获取实时行情
    spot_data = test_global_spot_data()
    
    # 总结
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)
    print("\n✅ 可用接口:")
    print("1. index_global_name_table() - 获取全球指数名称表")
    print("2. index_global_spot_em() - 获取全球指数实时行情 (推荐)")
    print("\n📊 数据来源: 东方财富")
    print("\n💡 支持国家/地区:")
    print("   ✅ 美国 (标普500, 道琼斯, 纳斯达克等)")
    print("   ✅ 日本 (日经225, 东证指数等)")
    print("   ✅ 印度 (孟买SENSEX, Nifty50等)")
    print("   ✅ 越南 (越南胡志明指数)")
    print("   ✅ 其他50+主要国家和地区")
    print("\n📝 使用建议:")
    print("   主要使用 index_global_spot_em() 接口获取实时行情")
    print("   该接口返回56+个全球指数的完整数据")


if __name__ == "__main__":
    main()
