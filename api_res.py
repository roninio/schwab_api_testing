from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

app = FastAPI()


class AssetType(str, Enum):
    EQUITY = "EQUITY"
    OPTION = "OPTION"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"
    TRAILING_STOP = "TRAILING_STOP"
    NET_DEBIT = "NET_DEBIT"


class Session(str, Enum):
    NORMAL = "NORMAL"


class Duration(str, Enum):
    DAY = "DAY"
    GOOD_TILL_CANCEL = "GOOD_TILL_CANCEL"


class Instruction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    BUY_TO_OPEN = "BUY_TO_OPEN"
    BUY_TO_COVER = "BUY_TO_COVER"
    BUY_TO_CLOSE = "BUY_TO_CLOSE"
    SELL_TO_OPEN = "SELL_TO_OPEN"
    SELL_SHORT = "SELL_SHORT"
    SELL_TO_CLOSE = "SELL_TO_CLOSE"


class OrderStrategyType(str, Enum):
    SINGLE = "SINGLE"
    TRIGGER = "TRIGGER"
    OCO = "OCO"


class Instrument(BaseModel):
    symbol: str
    assetType: AssetType


class OrderLeg(BaseModel):
    instruction: Instruction
    quantity: int
    instrument: Instrument


class Order(BaseModel):
    orderType: OrderType
    session: Session
    duration: Duration
    orderStrategyType: OrderStrategyType
    orderLegCollection: List[OrderLeg]
    price: Optional[float] = None
    stopPrice: Optional[float] = None
    stopPriceLinkBasis: Optional[str] = None
    stopPriceLinkType: Optional[str] = None
    stopPriceOffset: Optional[float] = None
    complexOrderStrategyType: Optional[str] = None
    childOrderStrategies: Optional[List["Order"]] = None


Order.update_forward_refs()


@app.post("/order/market")
async def place_market_order(order: Order):
    # Implement order placement logic here
    return {"message": "Market order placed successfully", "order": order}


@app.post("/order/limit")
async def place_limit_order(order: Order):
    if order.price is None:
        raise HTTPException(status_code=400, detail="Limit price is required")
    # Implement order placement logic here
    return {"message": "Limit order placed successfully", "order": order}


@app.post("/order/option")
async def place_option_order(order: Order):
    if order.orderLegCollection[0].instrument.assetType != AssetType.OPTION:
        raise HTTPException(
            status_code=400, detail="Invalid asset type for option order"
        )
    # Implement option order placement logic here
    return {"message": "Option order placed successfully", "order": order}


@app.post("/order/vertical_spread")
async def place_vertical_spread_order(order: Order):
    if len(order.orderLegCollection) != 2:
        raise HTTPException(
            status_code=400, detail="Vertical spread must have exactly two legs"
        )
    # Implement vertical spread order placement logic here
    return {"message": "Vertical spread order placed successfully", "order": order}


@app.post("/order/conditional/one_triggers_another")
async def place_one_triggers_another_order(order: Order):
    if order.orderStrategyType != OrderStrategyType.TRIGGER:
        raise HTTPException(status_code=400, detail="Invalid order strategy type")
    # Implement one-triggers-another order placement logic here
    return {"message": "One-triggers-another order placed successfully", "order": order}


@app.post("/order/conditional/one_cancels_another")
async def place_one_cancels_another_order(order: Order):
    if order.orderStrategyType != OrderStrategyType.OCO:
        raise HTTPException(status_code=400, detail="Invalid order strategy type")
    # Implement one-cancels-another order placement logic here
    return {"message": "One-cancels-another order placed successfully", "order": order}


@app.post("/order/conditional/one_triggers_oco")
async def place_one_triggers_oco_order(order: Order):
    if (
        order.orderStrategyType != OrderStrategyType.TRIGGER
        or not order.childOrderStrategies
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid order strategy type or missing child strategies",
        )
    # Implement one-triggers-OCO order placement logic here
    return {"message": "One-triggers-OCO order placed successfully", "order": order}


@app.post("/order/trailing_stop")
async def place_trailing_stop_order(order: Order):
    if order.orderType != OrderType.TRAILING_STOP:
        raise HTTPException(
            status_code=400, detail="Invalid order type for trailing stop"
        )
    # Implement trailing stop order placement logic here
    return {"message": "Trailing stop order placed successfully", "order": order}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
