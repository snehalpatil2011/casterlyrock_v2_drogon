from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import uvicorn

app =  FastAPI()

class Message(BaseModel):
    message:str

@app.get("/")
async def health_check():
    print("Health Check called !")
    return "The health check is Successfull !"

@app.post("/placeorder/")
async def place_order(message:Message):
    print(f"Webhook Triggered: Order Placer | {message.message}")
    return message

if __name__ == "__main__":
    uvicorn.run(app)