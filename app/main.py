# import dependencies
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from contextlib import asynccontextmanager
import json 
from starlette.config import Config

config = Config(".env")

# create app instance
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.requests_client = httpx.AsyncClient()
    yield
    await app.requests_client.aclose()


# create app instance
app = FastAPI(lifespan=lifespan)
# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the index.html page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    serverTime: datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "serverTime" : serverTime})

@app.get("/advice", response_class=HTMLResponse)
async def advice(request: Request):
    
    # Define a request_client instance
    requests_client = request.app.requests_client

    # Connect to the API URL and await the response
    response = await requests_client.get(config("ADVICE_URL"))

    # Send the json data from the response in the TemplateResponse data parameter 
    return templates.TemplateResponse("advice.html", {"request": request, "data": response.json() })

@app.get("/apod", response_class=HTMLResponse)
async def advice(request: Request):
    
    # Define a request_client instance
    requests_client = request.app.requests_client

    # Connect to the API URL and await the response
    response = await requests_client.get(config("NASA_APOD_URL"))

    # Send the json data from the response in the TemplateResponse data parameter 
    return templates.TemplateResponse("apod.html", {"request": request, "data": response.json() })

@app.get("/params", response_class=HTMLResponse)
async def index(request: Request, name: str | None = ""):
    return templates.TemplateResponse("params.html", {"request": request, "name" : name})

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)