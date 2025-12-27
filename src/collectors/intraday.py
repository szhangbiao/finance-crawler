import akshare as ak
import pandas as pd
from typing import Optional

class IntradayCollector:
    """
    日内高频数据采集器.
    为 HAR (Heterogeneous Autoregressive) 模型或其他高频/量化策略提供分钟级行情数据.
    """
    
    def __init__(self):
        """
        初始化采集器.
        """
        self.name = "intraday"

    def get_index_intraday(self, symbol: str = "000300", period: str = "5") -> pd.DataFrame:
        """
        获取 A 股指数的分钟级数据.
        
        Args:
            symbol (str): 指数代码, 如 '000300' (沪深300), '000001' (上证指数), '399006' (创业板指).
            period (str): 周期, 可选 {'1', '5', '15', '30', '60'}, 默认为 '5'.
            
        Returns:
            pd.DataFrame: 包含时间、开盘、收盘、最高、最低、成交量、成交额等.
            
        Example:
            >>> collector = IntradayCollector()
            >>> df = collector.get_index_intraday(symbol="000300", period="5")
        """
        try:
            # 使用东财接口获取指数分钟线
            df = ak.index_zh_a_hist_min_em(symbol=symbol, period=period)
            if df is not None and not df.empty:
                # 转换时间列为 datetime 格式以便后续计算
                if '时间' in df.columns:
                    df['时间'] = pd.to_datetime(df['时间'])
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Error in get_index_intraday for {symbol}: {e}")
            return pd.DataFrame()

    def get_stock_intraday(self, symbol: str = "600519", period: str = "5", adjust: str = "") -> pd.DataFrame:
        """
        获取 A 股个股的分钟级数据.
        
        Args:
            symbol (str): 股票代码, 如 '600519'.
            period (str): 周期, 可选 {'1', '5', '15', '30', '60'}, 默认为 '5'.
            adjust (str): 复权方式, 可选 {'', 'qfq', 'hfq'}, 默认为空(不复权).
            
        Returns:
            pd.DataFrame: 个股分钟行情.
        """
        try:
            df = ak.stock_zh_a_hist_min_em(symbol=symbol, period=period, adjust=adjust)
            if df is not None and not df.empty:
                if '时间' in df.columns:
                    df['时间'] = pd.to_datetime(df['时间'])
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Error in get_stock_intraday for {symbol}: {e}")
            return pd.DataFrame()
