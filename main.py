from fastapi import FastAPI
from services.place_order import PlaceOrder
from services.models.fyers_response_model import OrderDetails,TwinTowerDetails,OrderBankNiftyFutureDetails
import uvicorn

app =  FastAPI()

@app.get("/")
async def health_check():
    print("Health Check called !")
    return "The health check is Successfull !"

@app.post("/placeorder")
async def place_order(orderDetails:OrderDetails):
    print(f"Webhook Triggered | Placing orders with details : Symbol :  {orderDetails.symbol} , SL : {orderDetails.stop_loss}")
    resp = PlaceOrder().place_order(orderDetails)
    return resp

@app.get("/twintowersdaily")
async def generate_twin_towers():
    print("Twin Tower Generation Started !")
    idenitfied_symbols_pp = PlaceOrder().twinTowerGenerator("D",20)
    return idenitfied_symbols_pp

@app.post("/orderbankniftyfuture")
async def place_order_bank_nifty_future(orderBankNiftyFutureDetails:OrderBankNiftyFutureDetails):
    print("Request Received : Place order for BANK NIFTY FUTURES")
    res = PlaceOrder().place_order_bank_nifty_future(orderBankNiftyFutureDetails)
    return res

@app.get("/accountDetails")
async def getAccountDetails():
    print("Request Received : Get Account Details")
    res = PlaceOrder().get_account_details()
    return res

if __name__ == "__main__":
    uvicorn.run(app)