import requests
from langchain_core.tools import tool
from .config import ALPHA_VANTAGE_API_KEY

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform numeric calculations.
    operation: add, sub, mul, div
    """
    ops = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
        "div": lambda a, b: a / b if b != 0 else "Division by zero",
    }

    if operation not in ops:
        return {"error": f"Invalid operation '{operation}'"}

    try:
        return {"result": ops[operation](first_num, second_num)}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """Fetch latest stock price."""
    if not ALPHA_VANTAGE_API_KEY:
        return {"error": "Alpha Vantage API key missing"}

    try:
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": ALPHA_VANTAGE_API_KEY,
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("Global Quote", {"error": "No stock data found"})
    except Exception as e:
        return {"error": str(e)}
