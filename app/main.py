import sys
sys.path.append('..')
sys.path.append('../interpreter')

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from interpreter.code_entities import CodeInternal
from pydantic import BaseModel

app: FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> FileResponse:
    return FileResponse("index.html")

class RunModel(BaseModel):
    code: str
    input: str
    limits: dict[str, int | None]

@app.post("/")
def run(data: RunModel) -> JSONResponse:
    return JSONResponse({
        'output': CodeInternal(data.code, data.input, data.limits).run()
    })