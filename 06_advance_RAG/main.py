from fastapi import FastAPI
from route.routes import user as route_app


app = FastAPI()
app.include_router(route_app)
