import requests

from models import Fund, FundProfitability

FIDUCUENTA_FUND_NAME = "Fiducuenta"
PLAN_SEMILLA_FUND_NAME = "Plan Semilla"

# Obtained from https://www.bancolombia.com/consultarFondosInversion/rest/servicio/consultarListaFondos
AVAILABLE_FUNDS = {
    FIDUCUENTA_FUND_NAME: "800180687",
    PLAN_SEMILLA_FUND_NAME: "800227622",
}


def call_endpoint(url) -> str:
    response = requests.get(url)

    return response


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


def process_response(response):
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

    print(fund)
    print(fund_profitability)


def get_fund_profitability(fund_identification):
    url = (
        "https://www.bancolombia.com/consultarFondosInversion/rest/servicio/"
        f"buscarInformacionFondo/{fund_identification}"
    )

    response = call_endpoint(url=url)

    json_response = response.json()

    process_response(response=json_response)


def main():
    get_fund_profitability(fund_identification=AVAILABLE_FUNDS[FIDUCUENTA_FUND_NAME])


if __name__ == '__main__':
    main()
