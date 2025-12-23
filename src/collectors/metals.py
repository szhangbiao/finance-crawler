import akshare as ak
import pandas as pd

class MetalsCollector:
    """
    Precious Metals Collector using AKShare.
    Focuses on Shanghai Gold Exchange (SGE) data.
    """

    def get_spot_quotations(self) -> pd.DataFrame:
        """
        获取上海黄金交易所实时行情.
        返回字段：品种、时间、现价、更新时间
        """
        try:
            return ak.spot_quotations_sge()
        except Exception as e:
            print(f"Error fetching metals quotations: {e}")
            return pd.DataFrame()

    def get_spot_price(self, symbol: str = "Au99.99") -> float:
        """
        获取指定品种的最新现价.
        
        Args:
            symbol: 品种名称，如 "Au99.99", "Ag(T+D)"
            
        Returns:
            float: 最新价格，如果在行情中未找到则返回 None
        """
        try:
            df = self.get_spot_quotations()
            if df.empty:
                return None
            
            # 过滤指定品种
            row = df[df['品种'] == symbol]
            if not row.empty:
                return float(row.iloc[0]['现价'])
            return None
        except Exception as e:
            print(f"Error getting spot price for {symbol}: {e}")
            return None

    def get_daily_hist(self, symbol: str = "Au99.99") -> pd.DataFrame:
        """
        获取上海黄金交易所历史行情数据.
        
        Args:
            symbol: 品种名称，如 "Au99.99"
            
        Returns:
            pd.DataFrame: 包含 date, open, close, high, low 等字段
        """
        try:
            # ak.spot_hist_sge(symbol="Au99.99") usually returns:
            # date, open, high, low, close, ...
            return ak.spot_hist_sge(symbol=symbol)
        except Exception as e:
            print(f"Error fetching metals history for {symbol}: {e}")
            return pd.DataFrame()
