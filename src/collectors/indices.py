import akshare as ak
import pandas as pd

class IndexCollector:
    """
    Stock Indices Collector using AKShare.
    """

    def get_key_indices(self) -> pd.DataFrame:
        """
        获取沪深重要指数实时行情.
        返回字段：序号、代码、名称、最新价、涨跌幅、涨跌额、成交量、成交额、...
        """
        try:
            return ak.stock_zh_index_spot_em(symbol="沪深重要指数")
        except Exception as e:
            print(f"Error fetching key indices: {e}")
            return pd.DataFrame()

    def get_sh_indices(self) -> pd.DataFrame:
        """
        获取上证系列指数实时行情.
        """
        try:
            return ak.stock_zh_index_spot_em(symbol="上证系列指数")
        except Exception as e:
            print(f"Error fetching SH indices: {e}")
            return pd.DataFrame()

    def get_sz_indices(self) -> pd.DataFrame:
        """
        获取深证系列指数实时行情.
        """
        try:
            return ak.stock_zh_index_spot_em(symbol="深证系列指数")
        except Exception as e:
            print(f"Error fetching SZ indices: {e}")
            return pd.DataFrame()

    def get_cs_indices(self) -> pd.DataFrame:
        """
        获取中证系列指数实时行情.
        """
        try:
            return ak.stock_zh_index_spot_em(symbol="中证系列指数")
        except Exception as e:
            print(f"Error fetching CS indices: {e}")
            return pd.DataFrame()
    
    def get_index_daily(self, symbol: str) -> pd.DataFrame:
        """
        获取指数历史行情数据 (日K).
        
        Args:
            symbol: 指数代码，如 "sh000001" (上证指数), "sz399001" (深证成指)
        """
        try:
            return ak.stock_zh_index_daily_em(symbol=symbol)
        except Exception as e:
            print(f"Error fetching index daily for {symbol}: {e}")
            return pd.DataFrame()
