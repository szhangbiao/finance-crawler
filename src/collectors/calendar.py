import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import calendar
from typing import List, Optional

class CalendarCollector:
    """
    财经日历采集器.
    用于采集未来财经大事件、经济数据发布、央行议息会议及股指期货交割日等.
    """
    
    def __init__(self):
        """
        初始化采集器.
        """
        self.name = "calendar"

    def get_economic_calendar(self, date_str: Optional[str] = None) -> pd.DataFrame:
        """
        获取指定日期的全球经济日历.
        
        Args:
            date_str (str, optional): 日期格式 YYYYMMDD. 默认为今天.
            
        Returns:
            pd.DataFrame: 包含日期、时间、地区、事件、重要性等字段.
            
        Example:
            >>> collector = CalendarCollector()
            >>> df = collector.get_economic_calendar("20251229")
        """
        try:
            if not date_str:
                date_str = datetime.now().strftime('%Y%m%d')
            df = ak.news_economic_baidu(date=date_str)
            if df is not None and not df.empty:
                return df
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching economic calendar for {date_str}: {e}")
            return pd.DataFrame()

    def get_upcoming_major_events(self, days: int = 7) -> pd.DataFrame:
        """
        获取未来指定天数内的重大财经大事件 (重要性较高或包含关键字的事件).
        
        Args:
            days (int): 未来天数, 默认为 7 天.
            
        Returns:
            pd.DataFrame: 过滤后的重大事件列表.
        """
        try:
            all_events = []
            current_date = datetime.now()
            
            for i in range(days):
                target_date = (current_date + timedelta(days=i)).strftime('%Y%m%d')
                df = self.get_economic_calendar(target_date)
                if not df.empty:
                    all_events.append(df)
            
            if not all_events:
                return pd.DataFrame()
                
            combined_df = pd.concat(all_events, ignore_index=True)
            
            # 过滤高重要性 (重要性通常为 1-3, 3 最高) 或 包含关键央行/会议词汇
            keywords = "利率|会议|议息|决议|联储|非农|CPI|GDP|失业率"
            mask = (combined_df['重要性'].astype(str).str.contains('3|高')) | \
                   (combined_df['事件'].str.contains(keywords, na=False, case=False))
            
            result_df = combined_df[mask].copy()
            return result_df
            
        except Exception as e:
            print(f"Error fetching upcoming major events: {e}")
            return pd.DataFrame()

    def get_futures_delivery_dates(self, start_year: int = None, count: int = 12) -> pd.DataFrame:
        """
        获取 A 股股指期货 (IF/IH/IC/IM) 的交割日.
        交割日规则: 合约到期月份的第三个星期五 (遇节假日顺延, 此处仅计算理论日期).
        
        Args:
            start_year (int): 开始年份.
            count (int): 获取未来多少个月份.
            
        Returns:
            pd.DataFrame: 包含年份、月份、交割日期的 DataFrame.
        """
        try:
            if not start_year:
                start_year = datetime.now().year
            
            current_month = datetime.now().month
            delivery_dates = []
            
            for i in range(count):
                month = (current_month + i - 1) % 12 + 1
                year = start_year + (current_month + i - 1) // 12
                
                # 计算每月第三个周五
                c = calendar.monthcalendar(year, month)
                fridays = []
                for week in c:
                    if week[calendar.FRIDAY] != 0:
                        fridays.append(week[calendar.FRIDAY])
                
                if len(fridays) >= 3:
                    third_friday = fridays[2]
                    date_obj = datetime(year, month, third_friday)
                    delivery_dates.append({
                        "年份": year,
                        "月份": month,
                        "交割日期": date_obj.strftime('%Y-%m-%d'),
                        "类型": "股指期货交割日 (IF/IH/IC/IM)"
                    })
            
            return pd.DataFrame(delivery_dates)
            
        except Exception as e:
            print(f"Error calculating delivery dates: {e}")
            return pd.DataFrame()

    def get_central_bank_interest_rates(self) -> pd.DataFrame:
        """
        获取主要央行当前利率及最近变动 (作为日历背景参考).
        支持: 美联储, 欧洲央行, 日本央行, 中国央行, 英国央行等.
        """
        try:
            data_list = []
            # 美联储
            try:
                fed_df = ak.macro_bank_usa_interest_rate()
                if not fed_df.empty:
                    last = fed_df.iloc[-1]
                    data_list.append({"机构": "美联储", "最新日期": last['日期'], "当前利率": last['今值'], "前值": last['前值']})
            except: pass
            
            # 日本央行
            try:
                boj_df = ak.macro_bank_japan_interest_rate()
                if not boj_df.empty:
                    last = boj_df.iloc[-1]
                    data_list.append({"机构": "日本央行", "最新日期": last['日期'], "当前利率": last['今值'], "前值": last['前值']})
            except: pass
            
            # 欧洲央行
            try:
                ecb_df = ak.macro_bank_euro_interest_rate()
                if not ecb_df.empty:
                    last = ecb_df.iloc[-1]
                    data_list.append({"机构": "欧洲央行", "最新日期": last['日期'], "当前利率": last['今值'], "前值": last['前值']})
            except: pass
            
            return pd.DataFrame(data_list)
        except Exception as e:
            print(f"Error fetching central bank rates: {e}")
            return pd.DataFrame()
