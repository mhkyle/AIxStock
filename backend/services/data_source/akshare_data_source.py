import akshare as ak

class AKShareDataService:
    def __init__(self, date: str, stock_code: str, timeout_by_seconds: int = 1):
        # date: 日期，格式为"YYYYMMDD", 例如"20240101"; 当前交易日的数据需要交易所收盘后统计
        self.date = date
        self.stock_code = stock_code
        self.timeout = timeout_by_seconds  # 设置超时时间，单位为秒
    
    def get_shanghai_stock_summary(self):
        # 获取上证指数的概况数据
        stock_sse_summary_df = ak.stock_sse_summary()
        return stock_sse_summary_df
    
    def get_shanghai_deal_daily(self):
        # 获取上海证券交易所-市场总貌-成交统计-日频数据
        return ak.stock_sse_deal_daily(date=self.date)
    
    def get_single_stock_info(self):
        # 分别尝试以下几种数据获取方式，前一种如果超时或返回空，立即进行下一种方式

        # 1. 东方财富-个股-股票信息
        try:
            result = ak.stock_individual_info_em(symbol=self.stock_code, timeout=self.timeout)
            if result is not None and not result.empty:
                return result
            print("东方财富数据为空，尝试备用数据源...")
        except Exception as e:
            print(f"东方财富数据获取失败: {e}")

        # 2. 个股信息查询-雪球（备用）
        try:
            print("尝试获取雪球数据...")
            # 雪球接口需要带交易所前缀，例如 "SH601127" 或 "SZ000001"
            xq_symbol = f"SH{self.stock_code}"
            result = ak.stock_individual_basic_info_xq(symbol=xq_symbol)
            if result is not None and not result.empty:
                return result
            print("雪球数据为空，所有数据源均无结果")
        except Exception as e:
            print(f"雪球数据获取失败: {e}")

        return None
        
    
    def get_stock_history(self):
        # 获取指定股票的历史数据
        stock_hist_df = ak.stock_zh_a_hist(symbol=self.stock_code, period="daily", start_date=self.date, end_date=self.date, adjust="")
        return stock_hist_df

if __name__ == "__main__":
    # 示例用法
    date = "20260513"
    stock_code = "000001"  # 替换为你需要查询的股票代码
    data_service = AKShareDataService(date, stock_code)
    
    shanghai_summary = data_service.get_shanghai_stock_summary()
    print("上海指数概况数据:")
    print(shanghai_summary)
    
    shanghai_deal_daily = data_service.get_shanghai_deal_daily()
    print("上海证券交易所-市场总貌-成交统计-日频数据:")
    print(shanghai_deal_daily)
    
    get_single_stock_info = data_service.get_single_stock_info()
    print(f"个股信息: date={data_service.date}, stock_code={data_service.stock_code}")
    print(get_single_stock_info)
    
    
    
    
