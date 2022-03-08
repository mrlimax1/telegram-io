import uvicorn


def start():
    uvicorn.run("src.api.app:app", reload=True)
