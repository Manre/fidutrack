from datetime import datetime

from clients.google_sheets import GoogleSheets
from clients.http import HTTPClient
from models import Fund, FundProfitability, ProcessedResponse
from scrappers.base import ScrapperTask

FIDUCUENTA_FUND_NAME = "Fiducuenta"
PLAN_SEMILLA_FUND_NAME = "Plan Semilla"


class BancolombiaScrapper(ScrapperTask):

    def __init__(self):
        self.google_sheets_client = GoogleSheets(spreadsheet_id="1bgrEkDuB6LBeELjVgGOqpUZ0aJuNLOVu1zUcA64bucI")
        self.http_client = HTTPClient()
        # Obtained from https://www.bancolombia.com/consultarFondosInversion/rest/servicio/consultarListaFondos
        self.available_funds = {
            FIDUCUENTA_FUND_NAME: "800180687",
            PLAN_SEMILLA_FUND_NAME: "800227622",
        }
        self.bancolombia_url = (
            "https://www.bancolombia.com/consultarFondosInversion/rest/servicio/buscarInformacionFondo/{fund_id}"
        )

    def scrap_single_fund(self, url: str, fund_name: str):
        _, json_response = self.http_client.get(url=url)

        processed_response = self.process_response(response=json_response)

        self.save(sheet_name=fund_name, processed_response=processed_response)

    def scrap(self):
        for fund_name in self.available_funds.keys():
            fund_identification = self.available_funds[fund_name]
            url = self.bancolombia_url.format(fund_id=fund_identification)

            self.scrap_single_fund(url=url, fund_name=fund_name)

    def clean_data(self, data: dict) -> dict:
        data = {**data['dias'], **data['anios']}
        for key, value in data.items():
            value = self.remove_percentage(value=value)
            value = self.replace_comma_with_period(value=value)
            data[key] = value

        return data

    def save(self, sheet_name: str, processed_response: ProcessedResponse):
        fund_profitability = processed_response.fund_profitability
        fund = processed_response.fund

        values = [
            datetime.utcnow().isoformat(),
            fund.closing_date,
            fund_profitability.weekly_profitability,
            fund_profitability.monthly_profitability,
            fund_profitability.semesterly_profitability,
            fund_profitability.year_to_date_profitability,
            fund_profitability.last_year_profitability,
            fund_profitability.last_two_years_profitability,
            fund_profitability.last_three_years_profitability,
        ]

        self.google_sheets_client.add(sheet_name=sheet_name, values=values)

    def process_response(self, response) -> ProcessedResponse:
        fund = Fund(
            nit=response["nit"],
            name=response["nombre"],
            rating=response["calificacion"],
            term=response["plazo"],
            unit_value=response["valorDeUnidad"],
            value_in_pesos=response["valorEnPesos"],
            closing_date=response["fechaCierre"],
            managing_company=response["sociedadAdministradora"],
        )

        profitability_information = response["rentabilidad"]
        profitability_information = self.clean_data(data=profitability_information)

        fund_profitability = FundProfitability(
            weekly_profitability=profitability_information["semanal"],
            monthly_profitability=profitability_information["mensual"],
            semesterly_profitability=profitability_information["semestral"],
            year_to_date_profitability=profitability_information["anioCorrido"],
            last_year_profitability=profitability_information["ultimoAnio"],
            last_two_years_profitability=profitability_information["ultimos2Anios"],
            last_three_years_profitability=profitability_information["ultimos3Anios"],
        )

        return ProcessedResponse(fund=fund, fund_profitability=fund_profitability)
