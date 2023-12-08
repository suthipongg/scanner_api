from fastapi import FastAPI
import uvicorn

import os
from dotenv import load_dotenv
load_dotenv('settings/.env')
env = os.environ

from utils.logging import configure_logging
from routes import image_routes

app = FastAPI(title=env["TITLE"])

if int(env["LOGGING"]):
    configure_logging()
    
app.include_router(image_routes.router)
# app.include_router(test.router)

if __name__ == "__main__":
    uvicorn.run("main:app", 
                host=env["HOST"], 
                port=int(env["PORT"]), 
                log_level="info", 
                reload=True
                )