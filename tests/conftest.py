import pytest

from scrappers.bancolombia import BancolombiaScrapper
from scrappers.base import ScrapperExecutor, ScrapperTask


@pytest.fixture(name="mock_scrapper_executor")
def fixture_scrapper_executor():
    return ScrapperExecutor()


@pytest.fixture(name="mock_scrapper_task")
def fixture_scrapper_task():
    class SampleTask(ScrapperTask):

        def scrap(self, *args, **kwargs) -> None:
            pass

        def clean_data(self, data: dict) -> dict:
            pass

        def save(self, *args, **kwargs):
            pass

    return SampleTask()


@pytest.fixture(name="bancolombia_scrapper")
def fixture_bancolombia_scrapper():
    return BancolombiaScrapper()
