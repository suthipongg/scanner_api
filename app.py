from fastapi import FastAPI
import uvicorn

import os, datetime
from dotenv import load_dotenv
load_dotenv('configs/.env')
env = os.environ

from configs.logging import configure_logging
from routes import extract_routes


app = FastAPI(
    title="PROJECT COSMEMET:  EXTRACTOR API (2023)", 
    description=f"TNT Media and Network Co., Ltd. \n Started at {datetime.datetime.now().strftime('%c')}",
    docs_url="/",
    version="1.0.0",
    # swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
    )

if int(env["LOGGING"]):
    configure_logging()
    
app.include_router(extract_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", 
                host=env["HOST"], 
                port=int(env["PORT"]), 
                log_level="info", 
                reload=True
                )