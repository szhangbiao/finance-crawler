import pandas as pd
import numpy as np
import statsmodels.api as sm
from typing import Dict, Tuple, Optional

class VolatilityProcessor:
    """
    波动率分析处理器.
    实现 HAR (Heterogeneous Autoregressive) 模型及其变体, 用于预测已实现波动率 (RV).
    """

    def __init__(self):
        self.name = "volatility_processor"

    def calculate_rv(self, df_min: pd.DataFrame) -> pd.DataFrame:
        """
        从分钟数据计算每日已实现波动率 (RV).
        
        Args:
            df_min: 包含 '时间' 和 '收盘' 列的分钟线 DataFrame.
            
        Returns:
            pd.DataFrame: 包含 'date' 和 'RV' 的每日数据.
        """
        try:
            temp_df = df_min.copy()
            temp_df['时间'] = pd.to_datetime(temp_df['时间'])
            temp_df = temp_df.sort_values('时间')
            
            # 计算对数收益率
            # 注意: 最好是按天计算收益率, 避免隔夜跳空影响 (除非模型需要包含隔夜)
            temp_df['date'] = temp_df['时间'].dt.date
            temp_df['log_ret'] = temp_df.groupby('date')['收盘'].transform(lambda x: np.log(x / x.shift(1)))
            
            # 计算每日 RV (收益率平方和)
            daily_rv = temp_df.groupby('date')['log_ret'].apply(lambda x: np.sum(x**2)).reset_index()
            daily_rv.columns = ['date', 'RV']
            
            # 过滤掉 RV 为 0 的数据 (可能是非交易日或异常)
            daily_rv = daily_rv[daily_rv['RV'] > 0]
            
            return daily_rv
        except Exception as e:
            print(f"Error in calculate_rv: {e}")
            return pd.DataFrame()

    def prepare_har_features(self, daily_rv: pd.DataFrame) -> pd.DataFrame:
        """
        构建 HAR 模型的分量 (Day, Week, Month).
        
        Args:
            daily_rv: 包含 'RV' 的每日波动率 DataFrame.
            
        Returns:
            pd.DataFrame: 增加滞后分量后的数据.
        """
        try:
            df = daily_rv.copy()
            # HAR 模型的经典分量: 1天, 5天(周), 22天(月)
            df['RV_d'] = df['RV'].shift(1)
            df['RV_w'] = df['RV'].shift(1).rolling(5).mean()
            df['RV_m'] = df['RV'].shift(1).rolling(22).mean()
            
            # 删除含有空值的行 (前22天数据无法预测)
            df = df.dropna()
            return df
        except Exception as e:
            print(f"Error in prepare_har_features: {e}")
            return pd.DataFrame()

    def fit_har_model(self, df_har: pd.DataFrame) -> Tuple[Optional[sm.regression.linear_model.RegressionResults], str]:
        """
        拟合 HAR 模型 (OLS 回归).
        模型: RV_t+1 = beta0 + beta_d*RV_d + beta_w*RV_w + beta_m*RV_m
        """
        try:
            # 准备自变量 X 和 因变量 y
            y = df_har['RV']
            X = df_har[['RV_d', 'RV_w', 'RV_m']]
            X = sm.add_constant(X) # 添加常数项
            
            model = sm.OLS(y, X).fit()
            return model, model.summary().as_text()
        except Exception as e:
            return None, f"Error in fit_har: {e}"

    def predict_next_day(self, daily_rv: pd.DataFrame) -> Dict:
        """
        根据最新数据预测下一个交易日的波动率.
        """
        try:
            # 1. 准备特征
            df_har = self.prepare_har_features(daily_rv)
            if df_har.empty:
                return {"error": "Not enough data for prediction (need at least 23 days)"}
            
            # 2. 拟合模型
            model, summary = self.fit_har_model(df_har)
            if not model:
                return {"error": summary}
            
            # 3. 提取最新的分量用于预测明天
            # 注意: 预测明天的 RV 需要用到 *今天的* 实时 RV、周平均、月平均
            last_rv = daily_rv.iloc[-1]['RV']
            last_rv_w = daily_rv['RV'].tail(5).mean()
            last_rv_m = daily_rv['RV'].tail(22).mean()
            
            # 构造输入 [const, RV_d, RV_w, RV_m]
            # 这里的 RV_d 就是今天的 RV, 用于预测明天
            input_data = [1.0, last_rv, last_rv_w, last_rv_m]
            prediction = model.predict(input_data)[0]
            
            return {
                "last_date": str(daily_rv.iloc[-1]['date']),
                "predicted_rv": float(prediction),
                "model_summary": summary,
                "coefficients": model.params.to_dict(),
                "r_squared": float(model.rsquared)
            }
        except Exception as e:
            return {"error": str(e)}
