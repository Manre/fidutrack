"""Tests for Bancolombia Scrapper"""
from scrappers.bancolombia import BancolombiaScrapper


class TestBancolombiaScrapper:

    def test_bancolombia_scrapper_initialization(self, bancolombia_scrapper):
        scrapper = BancolombiaScrapper()

        assert scrapper.google_sheets_client is not None
        assert scrapper.http_client is not None

    def test_bancolombia_scrapper_scrap(self, mocker, bancolombia_scrapper):
        scrap_single_fund_mock = mocker.Mock()
        bancolombia_scrapper.scrap_single_fund = scrap_single_fund_mock

        bancolombia_scrapper.scrap()

        assert scrap_single_fund_mock.call_count == 2
