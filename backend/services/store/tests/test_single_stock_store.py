import json

import pandas as pd
import pytest

from backend.services.store.single_stock_store import (
    DatabaseSingleStockStorage,
    LocalCsvSingleStockStorage,
    SingleStockStore,
)


DATE = "20260512"
STOCK_CODE = "000001"


@pytest.fixture
def stock_info_df():
    return pd.DataFrame(
        {
            "item": [
                "最新",
                "股票代码",
                "股票简称",
                "总股本",
                "流通股",
                "总市值",
                "流通市值",
                "行业",
                "上市时间",
            ],
            "value": [
                12.34,
                STOCK_CODE,
                "平安银行",
                19405918198.0,
                19405918198.0,
                239469830963.32,
                239469830963.32,
                "银行",
                "19910403",
            ],
        }
    )


class TestLocalCsvSingleStockStorage:
    def test_writes_first_record_to_zero_csv(self, tmp_path, stock_info_df):
        storage = LocalCsvSingleStockStorage(storage_root=tmp_path)

        storage.save_stock_info(date=DATE, stock_code=STOCK_CODE, stock_info_df=stock_info_df)

        csv_path = tmp_path / STOCK_CODE / "0.csv"
        assert csv_path.exists()

        saved_df = pd.read_csv(csv_path, dtype={"date": str, "stock_code": str, "listed_date": str})
        assert saved_df.iloc[0].to_dict() == {
            "date": DATE,
            "stock_code": STOCK_CODE,
            "stock_name": "平安银行",
            "latest_price": 12.34,
            "total_share_capital": 19405918198.0,
            "circulating_share_capital": 19405918198.0,
            "total_market_value": 239469830963.32,
            "circulating_market_value": 239469830963.32,
            "industry": "银行",
            "listed_date": "19910403",
            "raw_items_json": json.dumps(
                {
                    "上市时间": "19910403",
                    "总市值": 239469830963.32,
                    "总股本": 19405918198.0,
                    "最新": 12.34,
                    "流通市值": 239469830963.32,
                    "流通股": 19405918198.0,
                    "股票代码": STOCK_CODE,
                    "股票简称": "平安银行",
                    "行业": "银行",
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
        }

    def test_rotates_to_next_csv_after_size_threshold(self, tmp_path, stock_info_df):
        storage = LocalCsvSingleStockStorage(storage_root=tmp_path, max_file_size_bytes=1)

        storage.save_stock_info(date=DATE, stock_code=STOCK_CODE, stock_info_df=stock_info_df)

        next_day_df = stock_info_df.copy()
        next_day_df.loc[next_day_df["item"] == "最新", "value"] = 12.56
        storage.save_stock_info(date="20260513", stock_code=STOCK_CODE, stock_info_df=next_day_df)

        assert (tmp_path / STOCK_CODE / "0.csv").exists()
        assert (tmp_path / STOCK_CODE / "1.csv").exists()

    def test_updates_existing_date_without_creating_new_file(self, tmp_path, stock_info_df):
        storage = LocalCsvSingleStockStorage(storage_root=tmp_path, max_file_size_bytes=1)

        storage.save_stock_info(date=DATE, stock_code=STOCK_CODE, stock_info_df=stock_info_df)

        updated_df = stock_info_df.copy()
        updated_df.loc[updated_df["item"] == "最新", "value"] = 13.01
        storage.save_stock_info(date=DATE, stock_code=STOCK_CODE, stock_info_df=updated_df)

        stock_dir = tmp_path / STOCK_CODE
        assert sorted(path.name for path in stock_dir.glob("*.csv")) == ["0.csv"]

        saved_df = pd.read_csv(stock_dir / "0.csv")
        assert saved_df.iloc[0]["latest_price"] == 13.01

    def test_loads_history_from_all_rotated_files(self, tmp_path, stock_info_df):
        storage = LocalCsvSingleStockStorage(storage_root=tmp_path, max_file_size_bytes=1)

        storage.save_stock_info(date=DATE, stock_code=STOCK_CODE, stock_info_df=stock_info_df)

        next_day_df = stock_info_df.copy()
        next_day_df.loc[next_day_df["item"] == "最新", "value"] = 12.56
        storage.save_stock_info(date="20260513", stock_code=STOCK_CODE, stock_info_df=next_day_df)

        history_df = storage.load_stock_info_history(stock_code=STOCK_CODE)

        assert history_df["date"].tolist() == [DATE, "20260513"]
        assert history_df["latest_price"].tolist() == [12.34, 12.56]

    def test_raises_for_invalid_dataframe_shape(self, tmp_path):
        storage = LocalCsvSingleStockStorage(storage_root=tmp_path)

        with pytest.raises(ValueError, match="must include 'item' and 'value' columns"):
            storage.save_stock_info(
                date=DATE,
                stock_code=STOCK_CODE,
                stock_info_df=pd.DataFrame({"name": ["最新"], "price": [1.0]}),
            )


class TestSingleStockStore:
    def test_uses_local_backend_when_configured(self, tmp_path, stock_info_df):
        store = SingleStockStore(storage_type="local", storage_root=tmp_path)

        store.save_stock_info(date=DATE, stock_code=STOCK_CODE, stock_info_df=stock_info_df)

        assert isinstance(store.backend, LocalCsvSingleStockStorage)
        assert (tmp_path / STOCK_CODE / "0.csv").exists()

    def test_uses_db_backend_when_configured(self):
        store = SingleStockStore(storage_type="db", connection_url="mysql://user:pass@host/db")

        assert isinstance(store.backend, DatabaseSingleStockStorage)

        with pytest.raises(NotImplementedError, match="Database storage is not implemented yet"):
            store.load_stock_info_history(stock_code=STOCK_CODE)

    def test_raises_for_unknown_storage_type(self):
        with pytest.raises(ValueError, match="storage_type must be either 'local' or 'db'"):
            SingleStockStore(storage_type="memory")
