from fastapi import FastAPI
app = FastAPI(
    title="Core service API",
    version="0.1.0",
)
@app.get("/health")
async def check_status():
    return {"status": "ok"}