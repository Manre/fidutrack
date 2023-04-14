from abc import ABC, abstractmethod


class ScrapperTask(ABC):
    @abstractmethod
    def scrap(self, *args, **kwargs) -> None:
        """Abstract method that defines the scraping functionality for a specific task."""
        pass

    @abstractmethod
    def clean_data(self, data: dict) -> dict:
        """Abstract method that defines the data cleaning functionality for a specific task.

        Args:
            data(dict): The raw data scraped by the task.
        """
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        """Abstract method that defines the data saving functionality for a specific task."""
        pass

    def remove_percentage(self, value: str) -> str:
        """Helper method that removes the percentage symbol from a string.

        Args:
            value(str): The string to be processed.

        Returns:
            A string without percentage

        """
        return value.replace("%", "")

    def replace_comma_with_period(self, value: str) -> str:
        """Helper method that replaces commas with periods in a string.

        Args:
            value(str): The string to be processed.

        Returns:
            A string with period instead of commas
        """
        return value.replace(",", ".")


class ScrapperExecutor:
    def __init__(self) -> None:
        self.tasks = []

    def add_task(self, task) -> None:
        """Adds a ScrapperTask to the list of tasks to be executed.

        Args:
            task(ScrapperTask): The ScrapperTask to be added.

        """
        self.tasks.append(task)

    def execute_all(self) -> None:
        """Executes all ScrapperTasks in the list of tasks."""
        for task in self.tasks:
            task.scrap()
