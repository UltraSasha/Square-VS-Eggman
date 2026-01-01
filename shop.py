from fastapi import FastAPI
import goods
import uvicorn

def go():
    global app
    app = FastAPI()

    @app.get("/items")
    def post_items():
        return goods.toJSON(goods.GOODS)
    
    uvicorn.run(app, host="192.168.1.68", port=8000)