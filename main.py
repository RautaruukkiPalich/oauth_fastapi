from fastapi import Depends, FastAPI, HTTPException, status


app = FastAPI()


async def main():
    return {"message": "Hello World"}


if __name__ == '__main__':
    root()
