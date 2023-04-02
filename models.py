from dataclasses import dataclass


@dataclass
class Fund:
    nit: str
    name: str
    rating: str
    term: str
    unit_value: str
    value_in_pesos: str
    closing_date: str
    managing_company: str


@dataclass
class FundProfitability:
    weekly_profitability: str
    monthly_profitability: str
    semesterly_profitability: str

    year_to_date_profitability: str
    last_year_profitability: str
    last_two_years_profitability: str
    last_three_years_profitability: str
