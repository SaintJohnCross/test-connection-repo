from request_toolkit.main import categorical_data_scalper, check_datasource_api_key_and_return, check_datasource_url_and_return, fetch_financial_data
from src.config import get_datasource
import json
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "request_input_data"

company_data = pd.read_csv(DATA_DIR / "head_S&P_Companies.csv", encoding="utf-8")

print(company_data.head())

def main() -> None:
    ds = get_datasource()
    api_key = check_datasource_api_key_and_return(ds)
    base_url = check_datasource_url_and_return(ds)
    for index, row in company_data.iterrows():
        symbol = row["Symbol"]
        request = fetch_financial_data("income-statement", base_url, symbol, 1, "quarter", api_key)

        extracted_data = categorical_data_scalper(request, ["revenue", "ebitda", "ebit", "incomeTaxExpense"])
        print(extracted_data) 

if __name__ == "__main__":
    main()