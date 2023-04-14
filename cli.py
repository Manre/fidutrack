from scrappers.bancolombia import BancolombiaScrapper
from scrappers.base import ScrapperExecutor


def execute():
    executor = ScrapperExecutor()
    executor.add_task(BancolombiaScrapper())
    executor.execute_all()


if __name__ == '__main__':
    execute()
