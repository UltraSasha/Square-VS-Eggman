from fastapi import FastAPI
import goods
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

def go():
    global app
    app = FastAPI()

    # CORS middleware - РЕШАЕТ ВАШУ ПРОБЛЕМУ
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Для разработки. В продакшене укажите конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/items")
    def post_items():
        return goods.toJSON(goods.GOODS)
    
    uvicorn.run(app, host="192.168.1.68", port=8000)