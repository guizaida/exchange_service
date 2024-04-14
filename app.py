from fastapi import FastAPI, Depends, HTTPException, Query
import decimal
import uvicorn

app = FastAPI()

class CurrencyExchangeService:
    exchange_rates = {
        "USD": {"TWD": 30.444, "JPY": 111.801, "USD": 1},
        "JPY": {"TWD": 0.26956, "JPY": 1, "USD": 0.00885},
        "TWD": {"TWD": 1, "JPY": 3.669, "USD": 0.03281},
    }

    def convert(self, source: str, target: str, amount: decimal.Decimal) -> decimal.Decimal:
        if source not in self.exchange_rates or target not in self.exchange_rates[source]:
            raise ValueError("Currency not supported.")
        rate = self.exchange_rates[source][target]
        result = amount * decimal.Decimal(rate)
        return result.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)

def get_currency_service():
    return CurrencyExchangeService()

@app.get("/convert")
def convert_currency(
    source: str = Query(..., description="Source currency code"),
    target: str = Query(..., description="Target currency code"),
    amount: str = Query(..., description="Amount to be converted, can include commas"),
    service: CurrencyExchangeService = Depends(get_currency_service)
):
    try:
        amount_decimal = decimal.Decimal(amount.replace(',', ''))
    except decimal.InvalidOperation:
        raise HTTPException(status_code=400, detail="Invalid amount format.")

    try:
        result = service.convert(source, target, amount_decimal)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result_formatted = f"{result:,.2f}"

    return {"msg": "success", "amount": result_formatted}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
