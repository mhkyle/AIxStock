import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from backend.services.data_source.akshare_data_source import AKShareDataService


DATE = "20260512"
STOCK_CODE = "601127"


@pytest.fixture
def service():
    return AKShareDataService(date=DATE, stock_code=STOCK_CODE)


@pytest.fixture
def service_custom_timeout():
    return AKShareDataService(date=DATE, stock_code=STOCK_CODE, timeout_by_seconds=5)


def make_df(data=None):
    """Return a non-empty DataFrame for use in mock return values."""
    return pd.DataFrame(data or {"col": [1, 2, 3]})


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------

class TestInit:
    def test_stores_date(self, service):
        assert service.date == DATE

    def test_stores_stock_code(self, service):
        assert service.stock_code == STOCK_CODE

    def test_default_timeout_is_one_second(self, service):
        assert service.timeout == 1

    def test_custom_timeout_is_stored(self, service_custom_timeout):
        assert service_custom_timeout.timeout == 5


# ---------------------------------------------------------------------------
# get_shanghai_stock_summary
# ---------------------------------------------------------------------------

class TestGetShanghaiStockSummary:
    @patch("backend.services.datas.akshare_input.ak.stock_sse_summary")
    def test_returns_dataframe_from_akshare(self, mock_summary, service):
        expected = make_df()
        mock_summary.return_value = expected

        result = service.get_shanghai_stock_summary()

        assert result is expected

    @patch("backend.services.datas.akshare_input.ak.stock_sse_summary")
    def test_calls_akshare_with_no_arguments(self, mock_summary, service):
        mock_summary.return_value = make_df()

        service.get_shanghai_stock_summary()

        mock_summary.assert_called_once_with()


# ---------------------------------------------------------------------------
# get_shanghai_deal_daily
# ---------------------------------------------------------------------------

class TestGetShanghaiDealDaily:
    @patch("backend.services.datas.akshare_input.ak.stock_sse_deal_daily")
    def test_returns_dataframe_from_akshare(self, mock_deal, service):
        expected = make_df()
        mock_deal.return_value = expected

        result = service.get_shanghai_deal_daily()

        assert result is expected

    @patch("backend.services.datas.akshare_input.ak.stock_sse_deal_daily")
    def test_passes_instance_date_to_akshare(self, mock_deal, service):
        mock_deal.return_value = make_df()

        service.get_shanghai_deal_daily()

        mock_deal.assert_called_once_with(date=DATE)


# ---------------------------------------------------------------------------
# get_single_stock_info
# ---------------------------------------------------------------------------

class TestGetSingleStockInfo:
    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_returns_em_data_when_primary_source_succeeds(self, mock_em, mock_xq, service):
        expected = make_df()
        mock_em.return_value = expected

        result = service.get_single_stock_info()

        assert result is expected
        mock_xq.assert_not_called()

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_passes_stock_code_and_timeout_to_em(self, mock_em, mock_xq, service):
        mock_em.return_value = make_df()

        service.get_single_stock_info()

        mock_em.assert_called_once_with(symbol=STOCK_CODE, timeout=1)

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_falls_back_to_xq_when_em_raises(self, mock_em, mock_xq, service):
        mock_em.side_effect = Exception("timeout")
        expected = make_df()
        mock_xq.return_value = expected

        result = service.get_single_stock_info()

        assert result is expected

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_falls_back_to_xq_when_em_returns_empty(self, mock_em, mock_xq, service):
        mock_em.return_value = pd.DataFrame()  # empty
        expected = make_df()
        mock_xq.return_value = expected

        result = service.get_single_stock_info()

        assert result is expected

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_xq_symbol_uses_sh_prefix_with_stock_code(self, mock_em, mock_xq, service):
        mock_em.side_effect = Exception("timeout")
        mock_xq.return_value = make_df()

        service.get_single_stock_info()

        mock_xq.assert_called_once_with(symbol=f"SH{STOCK_CODE}")

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_returns_none_when_both_sources_raise(self, mock_em, mock_xq, service):
        mock_em.side_effect = Exception("em error")
        mock_xq.side_effect = Exception("xq error")

        result = service.get_single_stock_info()

        assert result is None

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_returns_none_when_both_sources_return_empty(self, mock_em, mock_xq, service):
        mock_em.return_value = pd.DataFrame()
        mock_xq.return_value = pd.DataFrame()

        result = service.get_single_stock_info()

        assert result is None

    @patch("backend.services.datas.akshare_input.ak.stock_individual_basic_info_xq")
    @patch("backend.services.datas.akshare_input.ak.stock_individual_info_em")
    def test_returns_none_when_em_empty_and_xq_raises(self, mock_em, mock_xq, service):
        mock_em.return_value = pd.DataFrame()
        mock_xq.side_effect = Exception("xq error")

        result = service.get_single_stock_info()

        assert result is None


# ---------------------------------------------------------------------------
# get_stock_history
# ---------------------------------------------------------------------------

class TestGetStockHistory:
    @patch("backend.services.datas.akshare_input.ak.stock_zh_a_hist")
    def test_returns_dataframe_from_akshare(self, mock_hist, service):
        expected = make_df()
        mock_hist.return_value = expected

        result = service.get_stock_history()

        assert result is expected

    @patch("backend.services.datas.akshare_input.ak.stock_zh_a_hist")
    def test_passes_correct_arguments_to_akshare(self, mock_hist, service):
        mock_hist.return_value = make_df()

        service.get_stock_history()

        mock_hist.assert_called_once_with(
            symbol=STOCK_CODE,
            period="daily",
            start_date=DATE,
            end_date=DATE,
            adjust="",
        )
