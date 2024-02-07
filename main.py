import uvicorn
from fastapi import FastAPI
from auth.routes import auth_router
from config import HOST_ADD, HOST_PORT
from users.routes import user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)


if __name__ == '__main__':
    uvicorn.run(
        "__main__:app",
        host=HOST_ADD,
        port=int(HOST_PORT),
        reload=True
    )
