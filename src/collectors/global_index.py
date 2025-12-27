#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全球股指数据采集器

支持获取全球56+个国家和地区的股指数据,包括:
- 美国: 标普500, 道琼斯, 纳斯达克
- 日本: 日经225
- 印度: 孟买SENSEX
- 越南: 越南胡志明
- 香港: 恒生指数
- 以及其他50+个全球主要指数
"""

import akshare as ak
import pandas as pd
from typing import Optional, List, Dict


class GlobalIndexCollector:
    """
    全球股指数据采集器 (基于 AKShare)
    
    数据来源: 东方财富
    """
    
    def __init__(self):
        """初始化采集器"""
        self.name = "global_index_collector"
    
    def get_all_indices(self) -> pd.DataFrame:
        """
        获取全球所有指数实时行情 (56+个指数)
        
        Returns:
            DataFrame: 包含以下字段:
                - 序号: 序号
                - 代码: 指数代码
                - 名称: 指数名称
                - 最新价: 最新价格
                - 涨跌额: 涨跌金额
                - 涨跌幅: 涨跌百分比
                - 开盘价: 开盘价
                - 最高价: 最高价
                - 最低价: 最低价
                - 昨收价: 昨日收盘价
                - 振幅: 振幅百分比
                - 最新行情时间: 更新时间
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> df = collector.get_all_indices()
            >>> print(df.head())
        """
        try:
            return ak.index_global_spot_em()
        except Exception as e:
            print(f"Error fetching global indices: {e}")
            return pd.DataFrame()

    def get_historical_data(self, symbol: str) -> pd.DataFrame:
        """
        获取全球指数历史日线数据.
        注意: AKShare 的 index_global_hist_em 接口 symbol 参数应为指数名称 (如 '标普500').
        
        Args:
            symbol: 指数名称, 如 '标普500', '纳斯达克', '日经225', '越南胡志明'.
        """
        try:
            return ak.index_global_hist_em(symbol=symbol)
        except Exception as e:
            print(f"Error fetching global historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_index_name_table(self) -> pd.DataFrame:
        """
        获取全球指数名称表 (20+个主要指数)
        
        Returns:
            DataFrame: 包含以下字段:
                - 指数名称: 指数的中文名称
                - 代码: 指数代码
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> df = collector.get_index_name_table()
            >>> print(df)
        """
        try:
            return ak.index_global_name_table()
        except Exception as e:
            print(f"Error fetching index name table: {e}")
            return pd.DataFrame()
    
    def get_us_indices(self) -> pd.DataFrame:
        """
        获取美国主要指数实时行情
        
        包括: 标普500, 道琼斯, 纳斯达克
        
        Returns:
            DataFrame: 美国主要指数数据
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> us_data = collector.get_us_indices()
            >>> print(us_data[['名称', '最新价', '涨跌幅']])
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return pd.DataFrame()
            
            # 筛选美国指数
            us_indices = df[df['名称'].str.contains('标普|道琼斯|纳斯达克', na=False)]
            return us_indices
        except Exception as e:
            print(f"Error fetching US indices: {e}")
            return pd.DataFrame()
    
    def get_asian_indices(self) -> pd.DataFrame:
        """
        获取亚洲主要指数实时行情
        
        包括: 日经225, 恒生指数, 韩国综合, 印度孟买SENSEX, 越南胡志明等
        
        Returns:
            DataFrame: 亚洲主要指数数据
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> asia_data = collector.get_asian_indices()
            >>> print(asia_data[['名称', '最新价', '涨跌幅']])
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return pd.DataFrame()
            
            # 筛选亚洲指数
            asian_keywords = '日经|韩国|印度|越南|恒生|香港|新加坡|台湾|泰国|马来西亚|印尼'
            asian_indices = df[df['名称'].str.contains(asian_keywords, na=False)]
            return asian_indices
        except Exception as e:
            print(f"Error fetching Asian indices: {e}")
            return pd.DataFrame()
    
    def get_european_indices(self) -> pd.DataFrame:
        """
        获取欧洲主要指数实时行情
        
        包括: 富时100, DAX指数, CAC40, 意大利MIB等
        
        Returns:
            DataFrame: 欧洲主要指数数据
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> europe_data = collector.get_european_indices()
            >>> print(europe_data[['名称', '最新价', '涨跌幅']])
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return pd.DataFrame()
            
            # 筛选欧洲指数
            european_keywords = '富时|英国|德国|DAX|法|CAC|意大利|西班牙|荷兰|瑞士|俄罗斯|欧洲'
            european_indices = df[df['名称'].str.contains(european_keywords, na=False)]
            return european_indices
        except Exception as e:
            print(f"Error fetching European indices: {e}")
            return pd.DataFrame()
    
    def get_index_by_name(self, name: str) -> Optional[pd.Series]:
        """
        根据名称获取特定指数的数据
        
        Args:
            name: 指数名称关键词 (支持模糊匹配)
        
        Returns:
            Series: 指数数据,如果未找到返回 None
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> sp500 = collector.get_index_by_name('标普500')
            >>> if sp500 is not None:
            >>>     print(f"标普500: {sp500['最新价']}")
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return None
            
            # 模糊匹配
            matched = df[df['名称'].str.contains(name, na=False)]
            
            if len(matched) == 0:
                print(f"未找到包含 '{name}' 的指数")
                return None
            
            # 如果有多个匹配,返回第一个
            if len(matched) > 1:
                print(f"找到 {len(matched)} 个匹配的指数,返回第一个: {matched.iloc[0]['名称']}")
            
            return matched.iloc[0]
        except Exception as e:
            print(f"Error fetching index by name '{name}': {e}")
            return None
    
    def get_market_sentiment(self) -> Dict[str, any]:
        """
        分析全球市场整体情绪
        
        Returns:
            dict: 包含市场情绪分析数据:
                - total: 总指数数量
                - rising: 上涨数量
                - falling: 下跌数量
                - flat: 持平数量
                - rising_pct: 上涨百分比
                - sentiment: 市场情绪 (乐观/中性/悲观)
                - avg_change: 平均涨跌幅
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> sentiment = collector.get_market_sentiment()
            >>> print(f"全球市场情绪: {sentiment['sentiment']}")
            >>> print(f"上涨占比: {sentiment['rising_pct']:.2f}%")
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return {
                    'success': False,
                    'error': '无法获取数据'
                }
            
            total = len(df)
            rising = len(df[df['涨跌幅'] > 0])
            falling = len(df[df['涨跌幅'] < 0])
            flat = len(df[df['涨跌幅'] == 0])
            
            rising_pct = (rising / total * 100) if total > 0 else 0
            avg_change = df['涨跌幅'].mean()
            
            # 判断市场情绪
            if rising_pct > 60:
                sentiment = '乐观'
                level = 'bullish'
            elif rising_pct > 40:
                sentiment = '中性'
                level = 'neutral'
            else:
                sentiment = '悲观'
                level = 'bearish'
            
            return {
                'success': True,
                'total': total,
                'rising': rising,
                'falling': falling,
                'flat': flat,
                'rising_pct': round(rising_pct, 2),
                'falling_pct': round((falling / total * 100), 2),
                'avg_change': round(avg_change, 2),
                'sentiment': sentiment,
                'sentiment_level': level
            }
        except Exception as e:
            print(f"Error analyzing market sentiment: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_top_performers(self, n: int = 10) -> pd.DataFrame:
        """
        获取涨幅前N名的指数
        
        Args:
            n: 返回数量,默认10
        
        Returns:
            DataFrame: 涨幅最大的N个指数
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> top10 = collector.get_top_performers(10)
            >>> print(top10[['名称', '涨跌幅']])
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return pd.DataFrame()
            
            # 按涨跌幅降序排序
            top = df.nlargest(n, '涨跌幅')
            return top[['名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '昨收价']]
        except Exception as e:
            print(f"Error fetching top performers: {e}")
            return pd.DataFrame()
    
    def get_bottom_performers(self, n: int = 10) -> pd.DataFrame:
        """
        获取跌幅前N名的指数
        
        Args:
            n: 返回数量,默认10
        
        Returns:
            DataFrame: 跌幅最大的N个指数
        
        Example:
            >>> collector = GlobalIndexCollector()
            >>> bottom10 = collector.get_bottom_performers(10)
            >>> print(bottom10[['名称', '涨跌幅']])
        """
        try:
            df = self.get_all_indices()
            if df.empty:
                return pd.DataFrame()
            
            # 按涨跌幅升序排序
            bottom = df.nsmallest(n, '涨跌幅')
            return bottom[['名称', '最新价', '涨跌额', '涨跌幅', '开盘价', '昨收价']]
        except Exception as e:
            print(f"Error fetching bottom performers: {e}")
            return pd.DataFrame()
    
    def print_market_summary(self):
        """打印全球市场概况"""
        print("=" * 80)
        print("全球市场实时概况".center(80))
        print("=" * 80)
        
        # 市场情绪
        sentiment = self.get_market_sentiment()
        if sentiment.get('success'):
            print(f"\n【市场情绪】: {sentiment['sentiment']} ({sentiment['sentiment_level']})")
            print(f"总指数数: {sentiment['total']}")
            print(f"上涨: {sentiment['rising']} ({sentiment['rising_pct']}%)")
            print(f"下跌: {sentiment['falling']} ({sentiment['falling_pct']}%)")
            print(f"平均涨跌幅: {sentiment['avg_change']}%")
        
        # 美国市场
        print(f"\n" + "-" * 80)
        print("美国市场")
        print("-" * 80)
        us_data = self.get_us_indices()
        if not us_data.empty:
            print(us_data[['名称', '最新价', '涨跌额', '涨跌幅']].to_string(index=False))
        
        # 亚洲市场 (前5名)
        print(f"\n" + "-" * 80)
        print("亚洲主要市场")
        print("-" * 80)
        asia_data = self.get_asian_indices()
        if not asia_data.empty:
            print(asia_data.head(5)[['名称', '最新价', '涨跌额', '涨跌幅']].to_string(index=False))
        
        # 涨幅榜前5
        print(f"\n" + "-" * 80)
        print("全球涨幅榜 TOP5")
        print("-" * 80)
        top5 = self.get_top_performers(5)
        if not top5.empty:
            print(top5[['名称', '涨跌幅', '最新价']].to_string(index=False))
        
        # 跌幅榜前5
        print(f"\n" + "-" * 80)
        print("全球跌幅榜 TOP5")
        print("-" * 80)
        bottom5 = self.get_bottom_performers(5)
        if not bottom5.empty:
            print(bottom5[['名称', '涨跌幅', '最新价']].to_string(index=False))
        
        print("\n" + "=" * 80)


if __name__ == "__main__":
    # 测试
    collector = GlobalIndexCollector()
    collector.print_market_summary()
