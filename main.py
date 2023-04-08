from datetime import datetime

from clients.google_sheets import GoogleSheets
from clients.http import HTTPClient
from models import Fund, FundProfitability, ProcessedResponse

FIDUCUENTA_FUND_NAME = "Fiducuenta"
PLAN_SEMILLA_FUND_NAME = "Plan Semilla"

# Obtained from https://www.bancolombia.com/consultarFondosInversion/rest/servicio/consultarListaFondos
AVAILABLE_FUNDS = {
    FIDUCUENTA_FUND_NAME: "800180687",
    PLAN_SEMILLA_FUND_NAME: "800227622",
}
google_sheets_client = GoogleSheets(spreadsheet_id="1bgrEkDuB6LBeELjVgGOqpUZ0aJuNLOVu1zUcA64bucI")
http_client = HTTPClient()


def remove_percentage(value) -> str:
    return value.replace("%", "")


def replace_comma_with_period(value) -> str:
    return value.replace(",", ".")


def clean_data(data):
    data = {**data['dias'], **data['anios']}
    for key, value in data.items():
        value = remove_percentage(value=value)
        value = replace_comma_with_period(value=value)
        data[key] = value

    return data


def process_response(response) -> ProcessedResponse:
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
    profitability_information = clean_data(data=profitability_information)

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


def save_response(sheet_name: str, processed_response: ProcessedResponse):
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

    google_sheets_client.add(sheet_name=sheet_name, values=values)


def get_fund_profitability(fund_name: str):
    fund_identification = AVAILABLE_FUNDS[fund_name]

    url = (
        "https://www.bancolombia.com/consultarFondosInversion/rest/servicio/"
        f"buscarInformacionFondo/{fund_identification}"
    )

    _, json_response = http_client.get(url=url)

    processed_response = process_response(response=json_response)

    save_response(sheet_name=fund_name, processed_response=processed_response)


def main():
    for fund_name in AVAILABLE_FUNDS.keys():
        get_fund_profitability(fund_name=fund_name)


if __name__ == '__main__':
    main()
