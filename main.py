import uvicorn
from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from config import HOST_ADD, HOST_PORT
from oauth_fastapi.db.database import get_async_session

app = FastAPI()
router = APIRouter()


@app.get('/')
async def index(
        session: AsyncSession = Depends(get_async_session),
):
    return {'ping': 'pong'}


if __name__ == '__main__':

    app.include_router(router)

    uvicorn.run(
        "__main__:app",
        host=HOST_ADD,
        port=int(HOST_PORT),
        reload=True
        )
