import requests
import json

def main() -> None:
    print("entrypoint active")

def fetch_financial_data(statement_type: str, symbol: str, limit: int, period: str, api_key: str) -> dict:
    url = f'https://financialmodelingprep.com/stable/{statement_type}?symbol={symbol}&limit={limit}&period={period}&apikey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    return response.json()

def categorical_data_scalper(financial_data: list[dict], category_list: list[str]) -> list[dict]:

    output_list = []

    if not financial_data: raise Exception("No financial data provided.")

    # check if categories in category_list exist in financial_data keys
    for category in category_list:
        if category not in financial_data[0]:
            raise Exception(f"Category '{category}' not found in financial data.")
        
    for records in financial_data:
        output_dict = {}
        for category in category_list:
            output_dict[category] = records.get(category)
        output_list.append(output_dict)



test_request = fetch_financial_data('income-statement', 'AAPL', 1, 'quarter', api_key)

print(json.dumps(test_request, indent=2, ensure_ascii=False))

print(categorical_data_scalper(test_request, ['revenue', 'ebitda', 'ebit', 'incomeTaxExpense']))