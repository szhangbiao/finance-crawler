import akshare as ak
import pandas as pd

class NewsCollector:
    """
    Financial News Collector using AKShare.
    """



    def get_cctv_news(self) -> pd.DataFrame:
        """
        获取央视新闻联播文字稿.
        返回字段：date（日期）、title（标题）、content（内容）
        """
        try:
            return ak.news_cctv()
        except Exception as e:
            print(f"Error fetching CCTV news: {e}")
            return pd.DataFrame()
    

    
    def get_futures_news(self) -> pd.DataFrame:
        """
        获取上海金属网期货新闻（实时更新）.
        返回字段：发布时间、内容
        """
        try:
            return ak.futures_news_shmet()
        except Exception as e:
            print(f"Error fetching futures news: {e}")
            return pd.DataFrame()
    
    def get_research_reports(self) -> pd.DataFrame:
        """
        获取东方财富研究报告.
        返回字段：序号、股票代码、股票简称、报告名称、东财评级、机构、
                 近一月个股研报数、盈利预测、行业、日期、报告PDF链接
        """
        try:
            return ak.stock_research_report_em()
        except Exception as e:
            print(f"Error fetching research reports: {e}")
            return pd.DataFrame()
    
    def get_suspension_notice(self) -> pd.DataFrame:
        """
        获取百度股票停牌提示.
        返回字段：股票代码、股票简称、交易所代码、停牌时间、复牌时间、
                 停牌事项说明、市值、公告日期、公告时间、证券类型、市场类型
        """
        try:
            return ak.news_trade_notify_suspend_baidu()
        except Exception as e:
            print(f"Error fetching suspension notice: {e}")
            return pd.DataFrame()
    
    def get_dividend_notice(self) -> pd.DataFrame:
        """
        获取百度股票分红提示.
        返回字段：股票代码、除权日、分红、送股、转增、实物、交易所、股票简称、报告期
        """
        try:
            return ak.news_trade_notify_dividend_baidu()
        except Exception as e:
            print(f"Error fetching dividend notice: {e}")
            return pd.DataFrame()
    
    def get_earnings_calendar(self) -> pd.DataFrame:
        """
        获取百度财报时间表.
        返回字段：股票代码、股票简称、交易所、财报类型、发布时间、市值、发布日期
        """
        try:
            return ak.news_report_time_baidu()
        except Exception as e:
            print(f"Error fetching earnings calendar: {e}")
            return pd.DataFrame()

    def get_international_news(self) -> pd.DataFrame:
        """
        获取财联社-国际财经新闻 (实时更新).
        返回字段：发布时间、标题、内容、来源等
        """
        try:
            return ak.stock_info_global_cls()
        except Exception as e:
            print(f"Error fetching international news: {e}")
            return pd.DataFrame()

    def get_cpi_data(self) -> pd.DataFrame:
        """
        获取中国CPI年度数据 (替代不稳定的日历接口).
        返回字段：日期、今值、预测值、前值
        """
        try:
            return ak.macro_china_cpi_yearly()
        except Exception as e:
            print(f"Error fetching CPI data: {e}")
            return pd.DataFrame()

    def get_stock_info(self, symbol: str = "000001") -> pd.DataFrame:
        """
        获取个股基本信息 (替代不稳定的个股新闻接口).
        返回字段：item, value
        """
        try:
            return ak.stock_individual_info_em(symbol=symbol)
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            return pd.DataFrame()

    def get_major_institution_news(self) -> pd.DataFrame:
        """
        获取主要国际机构（高盛、摩根大通、路透）关于中国的消息.
        基于 get_international_news 进行关键词筛选.
        
        关键词逻辑: (机构名) AND (中国相关)
        机构: 高盛, 摩根, 路透, Goldman, JPMorgan, Reuters
        话题: 中国, 华, CN, China
        
        Returns:
            DataFrame: 包含筛选后的新闻
        """
        try:
            df = self.get_international_news()
            if df.empty:
                return df
                
            # 定义关键词
            sources = ["高盛", "摩根", "路透", "Goldman", "JPMorgan", "Reuters"]
            topics = ["中国", "华", "CN", "China"]
            
            # 构造筛选掩码
            # 将标题和内容列转为字符串并拼接，方便统一搜索 (如果只有标题则只搜标题)
            # 注意：get_international_news 返回字段可能有 '标题', '内容'
            search_text = pd.Series("", index=df.index)
            if '标题' in df.columns:
                search_text = search_text + df['标题'].astype(str)
            if '内容' in df.columns:
                search_text = search_text + " " + df['内容'].astype(str)
                
            # source_mask: 包含任一机构关键词
            source_mask = search_text.str.contains('|'.join(sources), case=False, na=False)
            
            # topic_mask: 包含任一话题关键词
            topic_mask = search_text.str.contains('|'.join(topics), case=False, na=False)
            
            # 最终筛选
            filtered_df = df[source_mask & topic_mask].copy()
            return filtered_df
            
        except Exception as e:
            print(f"Error fetching major institution news: {e}")
            return pd.DataFrame()
