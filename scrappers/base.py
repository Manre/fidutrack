from abc import ABC, abstractmethod


class BaseScrapper(ABC):
    @abstractmethod
    def scrap(self, *args, **kwargs):
        pass

    @abstractmethod
    def clean_data(self, data: dict):
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    def remove_percentage(self, value) -> str:
        return value.replace("%", "")

    def replace_comma_with_period(self, value) -> str:
        return value.replace(",", ".")
