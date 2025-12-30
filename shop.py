from fastapi import FastAPI
import uvicorn

def go():
    global app
    app = FastAPI()

    @app.get("/items")
    def post_items():
        return {
            "block": 80,
            "time": 110,
            "limit_turbo": 130,
            "x2_moneys": 200
                }
    uvicorn.run(app, host="192.168.1.68", port=8000)