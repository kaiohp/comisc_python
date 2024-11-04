from fastapi import FastAPI

from src.infra.database import orm
from src.main.routes import allocate

orm.start_mappers()

app = FastAPI()
app.include_router(allocate.router)


@app.get("/")
async def root():
    return {"message": "Running"}
