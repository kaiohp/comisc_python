from fastapi import FastAPI

from src.main.routes import allocate

app = FastAPI()
app.include_router(allocate.router)


@app.get('/')
async def root():
    return {'message': 'Running'}
