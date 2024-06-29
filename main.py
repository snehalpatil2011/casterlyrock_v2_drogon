from fastapi import FastAPI
from services.place_order import PlaceOrder
from services.models.fyers_response_model import OrderDetails 
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

if __name__ == "__main__":
    uvicorn.run(app)