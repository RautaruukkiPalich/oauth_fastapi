import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routes import auth_router
from config import HOST_ADD, HOST_PORT
from users.routes import user_router

origins = [
    'http://localhost:5500',
    'http://localhost:8080',
    'http://127.0.0.1:5500',
    'http://127.0.0.1:8080',
]

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET", "POST",
        "PATCH", "PUT",
        "DELETE", "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


if __name__ == '__main__':
    uvicorn.run(
        "__main__:app",
        host=HOST_ADD,
        port=int(HOST_PORT),
        reload=True
    )
