from requests import head
from request_toolkit.main import categorical_data_scalper, check_datasource_api_key_and_return, check_datasource_url_and_return, fetch_financial_data
from src.config import get_datasource
import json
import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_INPUT_DIR = BASE_DIR / "data" / "request_input_data"
DATA_OUTPUT_DIR = BASE_DIR / "data" / "request_output_data"

company_data = pd.read_csv(DATA_INPUT_DIR / "head_S&P_Companies.csv", encoding="utf-8")

def main() -> None:
    ds = get_datasource()
    api_key = check_datasource_api_key_and_return(ds)
    base_url = check_datasource_url_and_return(ds)

    header_list = ["symbol", 
                   "revenue", 
                   "ebitda", 
                   "ebit", 
                   "incomeTaxExpense",
                   "eps"]
    
    document_type = "income-statement"

    # writing the data first into rows, and then putting it out to output_df
    output_rows = []

    for index, row in company_data.iterrows():
        symbol = row["Symbol"]
        request = fetch_financial_data(document_type, base_url, symbol, 1, "quarter", api_key)

        extracted_data = categorical_data_scalper(request, header_list)
        output_rows.append(extracted_data[0])
    
    df = pd.DataFrame(output_rows, columns=header_list)
    print(df.head())

    df.to_csv(DATA_OUTPUT_DIR / f"{document_type}.csv", index=False)

if __name__ == "__main__":
    main()