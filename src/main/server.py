from fastapi import FastAPI

from src.infra.database import orm
from src.main.routes import add_batch, allocate, deallocate

orm.start_mappers()

app = FastAPI()
app.include_router(allocate.router)
app.include_router(deallocate.router)
app.include_router(add_batch.router)


@app.get('/')
async def root():
    return {'message': 'Running'}
