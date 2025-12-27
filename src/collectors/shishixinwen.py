import pandas as pd
import requests
from typing import Optional

class ShishixinwenCollector:
    """
    实事新闻 (shishixinwen.news) 数据采集器.
    基于 Next.js 内部接口实现的快讯聚合爬虫.
    """
    
    def __init__(self):
        """
        初始化采集器.
        """
        self.name = "shishixinwen"
        self.base_url = "https://shishixinwen.news/api/news"

    def get_news(self, page: int = 1, page_size: int = 50, q: Optional[str] = None, source: Optional[str] = None) -> pd.DataFrame:
        """
        获取全球快讯及 AI 深度解析.
        
        Args:
            page (int): 页码, 默认为 1.
            page_size (int): 每页条数, 默认为 50.
            q (str, optional): 搜索关键词.
            source (str, optional): 过滤特定数据源, 如 '金十数据', '华尔街见闻', '东方财富'.
            
        Returns:
            pd.DataFrame: 包含快讯标题、内容、来源、AI解析等的 DataFrame.
            
        Example:
            >>> collector = ShishixinwenCollector()
            >>> df = collector.get_news(page=1, q="非农")
        """
        try:
            params = {
                "page": page,
                "pageSize": page_size
            }
            if q:
                params["q"] = q
            if source:
                params["source"] = source
                
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://shishixinwen.news/news"
            }
            
            response = requests.get(self.base_url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            
            json_data = response.json()
            
            # API 返回格式通常为 {"data": [...], "total": 23200}
            if "data" in json_data and isinstance(json_data["data"], list):
                if not json_data["data"]:
                    return pd.DataFrame()
                
                df = pd.DataFrame(json_data["data"])
                
                # 转换日期格式 (如果是 Unix 时间戳)
                if 'createdAt' in df.columns:
                    try:
                        df['createdAt'] = pd.to_datetime(df['createdAt'])
                    except:
                        pass
                
                return df
            
            return pd.DataFrame()
            
        except Exception as e:
            print(f"Error fetching data from shishixinwen: {e}")
            return pd.DataFrame()

    def get_all_news(self, max_pages: int = 5) -> pd.DataFrame:
        """
        获取多页连续的历史快讯.
        
        Args:
            max_pages (int): 最大获取页数, 默认为 5.
            
        Returns:
            pd.DataFrame: 合并后的多页新闻数据.
        """
        all_dfs = []
        for p in range(1, max_pages + 1):
            df = self.get_news(page=p)
            if df.empty:
                break
            all_dfs.append(df)
            
        if not all_dfs:
            return pd.DataFrame()
            
        return pd.concat(all_dfs, ignore_index=True)
