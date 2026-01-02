# contains all tools required for making requests to financial data APIs

from __future__ import annotations
import os
import requests
import json
from src.config import get_datasource
from typing import Any, Dict, List

DEFAULT_PERIOD = "quarter"
DEFAULT_LIMIT = 1

def categorical_data_scalper(financial_data: List[Dict[str, Any]], category_list: List[str]) -> List[Dict[str, Any]]:
    if not financial_data:
        raise ValueError("No financial data provided.")

    # check if categories in category_list exist in financial_data keys
    for category in category_list:
        if category not in financial_data[0]:
            raise Exception(f"Category '{category}' not found in financial data.")
        
    output_list: List[Dict[str, Any]] = []
    for records in financial_data:
        output_list.append({category: records.get(category) for category in category_list})
    return output_list

def check_datasource_api_key_and_return(ds: Dict[str, Any]) -> str:
    """
    Validate that the datasource dict has an api_key set.
    """
    api_key_in_env = ds.get("api_key_in_env")
    if not api_key_in_env:
        raise RuntimeError("Datasource is missing required 'api_key' value")
    api_key = os.getenv(api_key_in_env)
    if not api_key:
        raise RuntimeError(f"Datasource api_key_in_env '{api_key_in_env}' not found in environment variables")
    
def check_datasource_url_and_return(ds: Dict[str, Any]) -> str:
    """
    Validate that the datasource dict has a base_url set.
    """
    base_url = ds.get("base_url")
    if not base_url:
        raise RuntimeError("Datasource is missing required 'base_url' value")
    return base_url

def fetch_financial_data(statement_type: str, 
                         base_url: str, 
                         symbol: str, 
                         limit: int, 
                         period: str, 
                         api_key: str) -> List[Dict[str, Any]]:
    url = f'{base_url}/{statement_type}?symbol={symbol}&limit={limit}&period={period}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    return response.json()

def main() -> None:
    ds = get_datasource()
    api_key = check_datasource_api_key_and_return(ds)
    base_url = check_datasource_url_and_return(ds)

    test_request = fetch_financial_data("income-statement", base_url, "AAPL", 1, "quarter", api_key)
    print(json.dumps(test_request, indent=2, ensure_ascii=False))

    extracted = categorical_data_scalper(test_request, ["revenue", "ebitda", "ebit", "incomeTaxExpense"])
    print(extracted)

if __name__ == "__main__":
    main()