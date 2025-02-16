from pydantic import BaseModel
from typing import List

class FyersFundLimitResponse_(BaseModel):
    id : int
    title: str
    equityAmount : float
    commodityAmount : float

class FyersFundsResponse(BaseModel):
    code: int
    message : str
    s : str
    fund_limit: List[FyersFundLimitResponse_]

class OrderDetails(BaseModel):
    symbol: str
    stop_loss: int

class TwinTowerDetails(BaseModel):
    startDate : str
    endDate : str

class OrderPlacerInputPayload(BaseModel):
    symbol: str
    signalType: str
    broker: str
    offlineOrder:bool = False
    exchange:str = "NSE"
    numberOfLots:int = 1