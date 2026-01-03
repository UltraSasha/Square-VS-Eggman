from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import goods
import uvicorn

goodsDict = goods.GOODS

uvicorn_server = None

def go():
    global app, uvicorn_server
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/items")
    def post_items():
        return goods.toJSON(goodsDict)
    
    class PurchaseRequest(BaseModel):
        id: str
        count: int

    class ResponseFormat(BaseModel):
        status: str
        errType: None | str = None
        errMessage: None | str = None

    @app.put("/purchase/", response_model=ResponseFormat)
    def get_purch_item(data: PurchaseRequest):
        try:
            id = data.id
            count = data.count
            goodsDict[id]["count"] += count
            return {
                "status": "success"
            }
        except Exception as e:
            return {
                "status": "error",
                "errType": type(e).__name__,
                "errMessage": str(e)
            }
        
    @app.delete("/purchase/", response_model=ResponseFormat)
    def del_purch_item(data: PurchaseRequest):
        try:
            id = data.id
            count = data.count
            goodsDict[id]["count"] -= count
            return {
                "status": "success"
            }
        except Exception as e:
            return {
                "status": "error",
                "errType": type(e).__name__,
                "errMessage": str(e)
            }
    
    config = uvicorn.Config(app, host="192.168.1.68", port=8000)
    uvicorn_server = uvicorn.Server(config)
    uvicorn_server.run()