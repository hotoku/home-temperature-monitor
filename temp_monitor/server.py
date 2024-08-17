from fastapi import FastAPI

from . import db

app = FastAPI()


@app.get("/")
async def get_root():
    ret = db.read_record()
    return ret
