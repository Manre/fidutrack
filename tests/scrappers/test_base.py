"""Tests for base from Scrappers"""


class TestScrapperExecutor:

    def test_add_task(self, mock_scrapper_executor, mock_scrapper_task):
        mock_scrapper_executor.add_task(mock_scrapper_task)

        assert len(mock_scrapper_executor.tasks) == 1
        assert mock_scrapper_executor.tasks[0] == mock_scrapper_task

    def test_execute_all(self, mocker, mock_scrapper_executor, mock_scrapper_task):
        mock_task1 = mocker.Mock(spec=mock_scrapper_task)
        mock_scrapper_executor.add_task(mock_task1)

        mock_scrapper_executor.execute_all()

        mock_task1.scrap.assert_called_once()
