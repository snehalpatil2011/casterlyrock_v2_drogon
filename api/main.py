from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

import uvicorn

app =  FastAPI()


@app.get("/")
async def health_check():
    return "The health check is Successfull !"


if __name__ == "__main__":
    uvicorn.run(app, port=80)